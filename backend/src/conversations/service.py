import os
import tempfile
import shutil
import logging
import uuid
from datetime import datetime
import traceback
from typing import List, Optional, Tuple

from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import selectinload
from sqlmodel import desc, select, delete 
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.db.models import Conversation, Message, User, Document

from src.errors import ConversationNotFound, ForbiddenAccess, MessageNotFound, DocumentNotFound
from .schemas import ConversationRenameModel, DocumentModel

from src.rag.chain import generate_contextual_rag_response, stream_contextual_rag_response
from langchain_core.documents import Document as LangchainDocument
from src.rag import vectorstore

from src.rag.loader import charger_documents, split_documents
from src.rag.vectorstore import add_documents_to_vectorstore
import aiofiles
from src.config import Config

logger = logging.getLogger(__name__)

class ConversationService:
    """
    Service de gestion des conversations avec intÃ©gration RAG sÃ©curisÃ©e.
    GÃ¨re les conversations, messages, documents et gÃ©nÃ©ration de rÃ©ponses contextuelle.
    """

    async def get_conversation_by_uid(
        self, conversation_uid: uuid.UUID, session: AsyncSession
    ) -> Optional[Conversation]:
        """RÃ©cupÃ¨re une conversation par son UID."""
        result = await session.exec(
            select(Conversation).where(Conversation.uid == conversation_uid)
        )
        return result.first()
    
    async def get_user_conversation(
        self, user_uid: uuid.UUID, conversation_uid: uuid.UUID, session: AsyncSession
    ) -> Optional[Conversation]:
        """RÃ©cupÃ¨re une conversation spÃ©cifique d'un utilisateur, en vÃ©rifiant l'appartenance."""
        result = await session.exec(
            select(Conversation).where(
                Conversation.uid == conversation_uid,
                Conversation.user_uid == user_uid
            )
        )
        return result.first()

    async def get_user_conversations(
        self, user_uid: uuid.UUID, session: AsyncSession
    ) -> List[Conversation]:
        """RÃ©cupÃ¨re toutes les conversations d'un utilisateur, triÃ©es par date de crÃ©ation."""
        statement = (
            select(Conversation)
            .where(Conversation.user_uid == user_uid)
            .order_by(desc(Conversation.created_at))
        )
        result = await session.exec(statement)
        return result.all()

    async def create_conversation(
        self,
        user: User,
        session: AsyncSession,
        title: Optional[str] = None
    ) -> Conversation:
        """CrÃ©e une nouvelle conversation pour un utilisateur."""
        if not title:
             title = f"Nouvelle discussion {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
        new_conversation = Conversation(title=title, user_uid=user.uid, user=user)
        session.add(new_conversation)
        await session.commit()
        await session.refresh(new_conversation)
        logger.info(f"Created conversation {new_conversation.uid} for user {user.uid}")
        return new_conversation
    
    async def get_formatted_history(self, conversation_uid: uuid.UUID, session: AsyncSession) -> List[Tuple[str, str]]:
        """
        RÃ©cupÃ¨re l'historique formatÃ© d'une conversation pour le contexte RAG.
        Retourne une liste de tuples (prompt, rÃ©ponse).
        """
        stmt = select(Message).where(Message.conversation_uid == conversation_uid).order_by(Message.created_at)
        results = await session.exec(stmt)
        messages = results.all()
        history = []
        for msg in messages:
             if msg.prompt and msg.response:
                   history.append((msg.prompt, msg.response))
        return history
    
    async def get_active_document_uids(
        self, 
        conversation_uid: uuid.UUID, 
        session: AsyncSession
    ) -> List[str]:
        """
        RÃ©cupÃ¨re les UIDs des documents actifs pour une conversation.
        CRITIQUE pour la sÃ©curitÃ© : seuls les documents actifs de cette conversation sont utilisÃ©s dans le RAG.
        """
        logger.info(f"RÃ©cupÃ©ration des documents actifs pour la conversation {conversation_uid}")
        
        try:
            statement = select(Document).where(
                Document.conversation_uid == conversation_uid,
                Document.is_active == True
            )
            result = await session.exec(statement)
            active_documents = result.all()
            
            active_uids = [str(doc.uid) for doc in active_documents]
            logger.info(f"TrouvÃ© {len(active_uids)} documents actifs pour la conversation {conversation_uid}")
            
            return active_uids
            
        except Exception as e:
            logger.error(f"Erreur lors de la rÃ©cupÃ©ration des documents actifs: {e}", exc_info=True)
            return []
    
    async def generate_rag_response(
        self, 
        prompt: str, 
        conversation_uid: uuid.UUID, 
        session: AsyncSession
    ) -> Tuple[str, Optional[List[LangchainDocument]]]:
        """
        GÃ©nÃ¨re une rÃ©ponse contextuelle sÃ©curisÃ©e utilisant uniquement les documents actifs.
        IntÃ¨gre l'historique de conversation et les documents pertinents.
        """
        logger.info(f"GÃ©nÃ©ration de rÃ©ponse RAG sÃ©curisÃ©e pour la conversation {conversation_uid}")
        try:
            # RÃ©cupÃ©ration de l'historique de conversation
            chat_history = await self.get_formatted_history(conversation_uid, session)
            
            # SÃ©curitÃ© : uniquement les documents actifs de cette conversation
            active_document_uids = await self.get_active_document_uids(conversation_uid, session)
            
            # GÃ©nÃ©ration de la rÃ©ponse avec contexte sÃ©curisÃ©
            ai_response_text, source_documents, doc_count = await generate_contextual_rag_response(
                question=prompt,
                active_document_uids=active_document_uids,
                chat_history=chat_history
            )
            
            logger.info(f"RÃ©ponse gÃ©nÃ©rÃ©e avec {doc_count} documents actifs")
            
            if source_documents:
                logger.info(f"Sources utilisÃ©es dans la rÃ©ponse: {len(source_documents)} documents")
            
            return ai_response_text, source_documents
            
        except Exception as e:
            logger.error(f"Erreur lors de la gÃ©nÃ©ration de la rÃ©ponse RAG: {e}", exc_info=True)
            return "DÃ©solÃ©, je n'ai pas pu traiter votre demande en raison d'une erreur interne.", None

    async def save_message_pair(
         self, *, conversation_uid: uuid.UUID, user_uid: uuid.UUID, 
         prompt: str, response: str, session: AsyncSession
     ) -> Message:
         """Sauvegarde une paire prompt/rÃ©ponse dans la base de donnÃ©es."""
         logger.info(f"Sauvegarde du prompt et de la rÃ©ponse RAG pour la conversation {conversation_uid}")
         conversation = await self.get_conversation_by_uid(conversation_uid, session)
         if not conversation:
             logger.error(f"Conversation {conversation_uid} non trouvÃ©e.")
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation non trouvÃ©e lors de la sauvegarde.")
         user = await session.get(User, user_uid)
         if not user:
              logger.error(f"Utilisateur {user_uid} non trouvÃ©.")
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvÃ© lors de la sauvegarde.")
         db_message = Message(
             conversation_uid=conversation_uid, user_uid=user_uid,
             prompt=prompt, response=response,
             conversation=conversation, user=user 
         )
         session.add(db_message)
         conversation.update_at = datetime.utcnow()
         session.add(conversation)
         await session.commit()
         await session.refresh(db_message)
         logger.info(f"Paire message/rÃ©ponse (ID: {db_message.uid}) sauvegardÃ©e pour la conversation {conversation_uid}")
         return db_message

    async def add_message_to_conversation(
        self, conversation_uid: uuid.UUID, user: User,
        prompt_text: str, session: AsyncSession,
    ) -> Message:
        """
        Ajoute un nouveau message Ã  une conversation avec gÃ©nÃ©ration automatique de rÃ©ponse RAG.
        VÃ©rifie les permissions utilisateur avant traitement.
        """
        conversation = await self.get_user_conversation(user.uid, conversation_uid, session)
        if not conversation:
            raise ConversationNotFound("Conversation non trouvÃ©e ou accÃ¨s interdit.")
        
        try:
            ai_response_text, _ = await self.generate_rag_response(
                prompt=prompt_text, conversation_uid=conversation_uid, session=session
            )
        except Exception as e:
            logger.error(f"Error calling RAG generation for conv {conversation_uid}: {e}", exc_info=True)
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service AI erreur.")

        new_message = Message(
            conversation_uid=conversation.uid, user_uid=user.uid,
            prompt=prompt_text, response=ai_response_text,
            conversation=conversation, user=user
        )
        session.add(new_message)
        conversation.update_at = datetime.utcnow()
        session.add(conversation)
        await session.commit()
        await session.refresh(new_message)
        logger.info(f"Added message {new_message.uid} to conversation {conversation_uid}")
        return new_message

    async def get_conversation_messages(
        self, conversation_uid: uuid.UUID, user_uid: uuid.UUID, session: AsyncSession
    ) -> List[Message]:
        """RÃ©cupÃ¨re tous les messages d'une conversation pour un utilisateur autorisÃ©."""
        conversation = await self.get_user_conversation(user_uid, conversation_uid, session)
        if not conversation:
            raise ConversationNotFound("Conversation non trouvÃ©e ou accÃ¨s interdit.")
        statement = (
            select(Message).where(Message.conversation_uid == conversation_uid).order_by(Message.created_at)
        )
        result = await session.exec(statement)
        return result.all()

    async def delete_conversation(
        self, conversation_uid: uuid.UUID, user_uid: uuid.UUID, session: AsyncSession
    ) -> None:
        """Supprime une conversation et tous ses messages associÃ©s."""
        conversation = await self.get_user_conversation(user_uid, conversation_uid, session)
        if not conversation:
            raise ConversationNotFound("Conversation non trouvÃ©e ou accÃ¨s interdit pour suppression.")
        await session.delete(conversation)
        await session.commit()
        logger.info(f"Deleted conversation {conversation_uid} for user {user_uid}")
        return None
    
    async def get_message_by_uid(self, message_uid: uuid.UUID, session: AsyncSession) -> Optional[Message]:
         """RÃ©cupÃ¨re un message par son UID."""
         result = await session.exec(select(Message).where(Message.uid == message_uid))
         return result.first()

    async def edit_message_and_regenerate(
        self, conversation_uid: uuid.UUID, message_to_edit_uid: uuid.UUID,
        user_uid: uuid.UUID, new_prompt_text: str, session: AsyncSession,
    ) -> List[Message]:
        """
        Modifie un message et rÃ©gÃ©nÃ¨re la rÃ©ponse ainsi que tous les messages suivants.
        Maintient la cohÃ©rence de l'historique en supprimant les messages ultÃ©rieurs.
        """
        conversation = await self.get_user_conversation(user_uid, conversation_uid, session)
        if not conversation: 
            raise ConversationNotFound("Conversation non trouvÃ©e ou accÃ¨s interdit.")
        message_to_edit = await self.get_message_by_uid(message_to_edit_uid, session)
        if not message_to_edit or message_to_edit.conversation_uid != conversation_uid or message_to_edit.user_uid != user_uid:
            raise MessageNotFound("Message non trouvÃ© ou accÃ¨s interdit.")
        if not message_to_edit.prompt:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Impossible de modifier une rÃ©ponse AI.")
        
        edit_message_timestamp = message_to_edit.created_at
        try:
            # Suppression des messages ultÃ©rieurs pour maintenir la cohÃ©rence
            await session.exec(delete(Message).where(
                Message.conversation_uid == conversation_uid, Message.created_at > edit_message_timestamp
            ))
            history_messages_result = await session.exec(
                select(Message).where(Message.conversation_uid == conversation_uid, Message.created_at < edit_message_timestamp).order_by(Message.created_at)
            )
            formatted_history = [(msg.prompt, msg.response) for msg in history_messages_result.all() if msg.prompt and msg.response]
            
            # RÃ©gÃ©nÃ©ration avec le nouveau prompt
            new_ai_response_text, _ = await self.generate_rag_response(
                prompt=new_prompt_text, 
                conversation_uid=conversation_uid, 
                session=session
            )
            
            message_to_edit.prompt = new_prompt_text
            message_to_edit.response = new_ai_response_text
            message_to_edit.update_at = datetime.utcnow()
            session.add(message_to_edit)
            conversation.update_at = datetime.utcnow()
            session.add(conversation)
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Error edit/regen message {message_to_edit_uid}: {e}", exc_info=True)
            detail_message = f"Erreur modification/regÃ©nÃ©ration: {e}"
            status_code_err = status.HTTP_503_SERVICE_UNAVAILABLE if "generate_rag_response" in traceback.format_exc() else status.HTTP_500_INTERNAL_SERVER_ERROR
            raise HTTPException(status_code=status_code_err, detail=detail_message)
        return await self.get_conversation_messages(conversation_uid, user_uid, session)
    
    async def rename_conversation(
            self, conversation_uid: uuid.UUID, user_uid: uuid.UUID,
            new_title: str, session: AsyncSession,
        ) -> Conversation:
            """Renomme une conversation existante."""
            conversation = await self.get_user_conversation(user_uid, conversation_uid, session)
            if not conversation: 
                raise ConversationNotFound("Conversation non trouvÃ©e ou accÃ¨s interdit.")
            conversation.title = new_title
            conversation.update_at = datetime.utcnow()
            session.add(conversation)
            await session.commit()
            await session.refresh(conversation)
            logger.info(f"Renamed conversation {conversation_uid} to '{new_title}' for user {user_uid}")
            return conversation
    
    async def get_documents_for_conversation(
        self, conversation_uid: uuid.UUID, user_uid: uuid.UUID, session: AsyncSession
    ) -> List[DocumentModel]:
        """RÃ©cupÃ¨re tous les documents associÃ©s Ã  une conversation."""
        if not await self.get_user_conversation(user_uid, conversation_uid, session):
            raise ForbiddenAccess("AccÃ¨s interdit Ã  cette conversation.")
        
        try:
            statement = select(Document).where(Document.conversation_uid == conversation_uid).order_by(desc(Document.upload_date))
            result = await session.exec(statement)
            db_documents = result.all()
            return [DocumentModel.from_orm(doc) for doc in db_documents]
        except Exception as e:
            logger.error(f"Error retrieving documents for conversation {conversation_uid}: {e}", exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve documents")

    async def get_active_documents_for_conversation(
        self, conversation_uid: uuid.UUID, user_uid: uuid.UUID, session: AsyncSession
    ) -> List[Document]:
        """
        RÃ©cupÃ¨re uniquement les documents actifs d'une conversation.
        """
        if not await self.get_user_conversation(user_uid, conversation_uid, session):
            raise ForbiddenAccess("AccÃ¨s interdit Ã  cette conversation.")
            
        statement = select(Document).where(
            Document.conversation_uid == conversation_uid,
            Document.is_active == True
        ).order_by(desc(Document.upload_date))
        result = await session.exec(statement)
        return result.all()
    

    async def remove_document_from_context(
        self,
        document_id: uuid.UUID,
        conversation_uid: uuid.UUID,
        user_uid: uuid.UUID,
        session: AsyncSession
    ) -> None:
        """
        Supprime un document de manière sécurisée : BDD, fichier physique et base vectorielle.
        """
        logger.info(f"Début de la suppression du document {document_id} pour la conversation {conversation_uid}")
        
        # 1. Vérifier les permissions
        conversation = await self.get_user_conversation(user_uid, conversation_uid, session)
        if not conversation:
            raise ForbiddenAccess("Accès interdit à cette conversation.")

        # 2. Récupérer le document
        doc_to_delete = await session.get(Document, document_id)
        if not doc_to_delete or doc_to_delete.conversation_uid != conversation_uid:
            raise DocumentNotFound("Document non trouvé ou n'appartient pas à la conversation.")

        # 3. Supprimer le fichier physique
        try:
            full_file_path = os.path.join(Config.UPLOAD_DIR, doc_to_delete.file_path)
            if os.path.exists(full_file_path):
                os.remove(full_file_path)
                logger.info(f"Fichier physique supprimé : {full_file_path}")
            else:
                logger.warning(f"Le fichier physique n'a pas été trouvé pour le document {document_id} au chemin : {full_file_path}")
        except Exception as e:
            logger.error(f"Erreur lors de la suppression du fichier physique {doc_to_delete.file_path}: {e}", exc_info=True)
            # On continue pour au moins nettoyer la BDD, mais on log l'erreur.

        # 4. Supprimer les vecteurs associés (CRUCIAL pour le RAG)
        try:
            vectorstore.delete_documents_from_vectorstore(document_uid=str(doc_to_delete.uid))
            logger.info(f"Vecteurs supprimés pour le document {doc_to_delete.uid}")
        except Exception as e:
            logger.error(f"Erreur lors de la suppression des vecteurs pour le document {doc_to_delete.uid}: {e}", exc_info=True)
            # Log l'erreur mais continuer pour que l'utilisateur voit le document disparaître
        
        # 5. Supprimer l'enregistrement de la base de données
        await session.delete(doc_to_delete)
        await session.commit()
        
        logger.info(f"Document {document_id} supprimé avec succès de la base de données.")
        return None
    
    async def process_and_index_files(
        self,
        files: List[UploadFile],
        conversation_uid: uuid.UUID,
        user_uid: uuid.UUID,
        session: AsyncSession
    ) -> dict:
        """
        Traite et indexe les fichiers uploadÃ©s pour une conversation.
        Traite chaque fichier individuellement pour Ã©viter les conflits de mÃ©tadonnÃ©es.
        """
        conversation = await self.get_user_conversation(user_uid, conversation_uid, session)
        if not conversation:
            raise ForbiddenAccess("AccÃ¨s interdit Ã  cette conversation.")

        saved_db_documents_info = []
        errors = []
        conversation_upload_path = os.path.join(Config.UPLOAD_DIR, str(conversation_uid))
        os.makedirs(conversation_upload_path, exist_ok=True)

        logger.info(f"Processing files for conversation {conversation_uid}. Saving to: {conversation_upload_path}")

        for file in files:
            temp_dir_for_rag = None
            try:
                # Nettoyage du nom de fichier pour la sÃ©curitÃ©
                safe_filename = "".join(c if c.isalnum() or c in ['.', '_', '-'] else '_' for c in file.filename)
                if not safe_filename:
                    safe_filename = f"upload_{uuid.uuid4().hex[:8]}{os.path.splitext(file.filename)[1]}"

                persistent_file_path = os.path.join(conversation_upload_path, safe_filename)
                
                # Lecture et sauvegarde du contenu
                file_content = await file.read()
                await file.seek(0)

                async with aiofiles.open(persistent_file_path, 'wb') as out_file:
                    await out_file.write(file_content)

                # Enregistrement des mÃ©tadonnÃ©es en base
                new_db_document = Document(
                    filename=safe_filename,
                    conversation_uid=conversation_uid,
                    file_path=os.path.relpath(persistent_file_path, Config.UPLOAD_DIR),
                    size=len(file_content),
                    mime_type=file.content_type or "application/octet-stream",
                    upload_date=datetime.utcnow(),
                    is_active=True
                )
                session.add(new_db_document)
                await session.flush()
                await session.refresh(new_db_document)

                temp_dir_for_rag = tempfile.mkdtemp()
                temp_file_path = os.path.join(temp_dir_for_rag, safe_filename)
                async with aiofiles.open(temp_file_path, 'wb') as temp_out_file:
                    await temp_out_file.write(file_content)

                # Traitement RAG du fichier individuel
                logger.info(f"Loading document for RAG from {temp_dir_for_rag}")
                rag_docs_loaded = charger_documents(temp_dir_for_rag)
                if rag_docs_loaded:
                    split_docs = split_documents(rag_docs_loaded)
                    if split_docs:
                        for doc in split_docs:
                            if not doc.metadata:
                                doc.metadata = {}
                            doc.metadata.update({
                                "document_uid": str(new_db_document.uid),
                                "conversation_uid": str(conversation_uid),
                                "source": new_db_document.filename
                            })
                        add_documents_to_vectorstore(split_docs, document_uid=str(new_db_document.uid))
                        logger.info(f"Document '{safe_filename}' (UID: {new_db_document.uid}) indexÃ© avec {len(split_docs)} chunks")

                saved_db_documents_info.append(DocumentModel.from_orm(new_db_document).model_dump(mode='json'))
                logger.info(f"Document '{new_db_document.filename}' processed (UID: {new_db_document.uid})")

            except Exception as e_file:
                errors.append({"filename": file.filename, "error": str(e_file)})
                logger.error(f"Error processing file {file.filename}: {e_file}", exc_info=True)
            finally:
                if temp_dir_for_rag:
                    try:
                        shutil.rmtree(temp_dir_for_rag)
                    except Exception as e_clean:
                        logger.error(f"Error cleaning temp dir for {file.filename}: {e_clean}")
                await file.close()

        try:
            await session.commit()
            logger.info(f"Committed {len(saved_db_documents_info)} documents to database")
        except Exception as e_commit:
            await session.rollback()
            logger.error(f"Error committing documents to database: {e_commit}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Server error during file processing"
            )

        return {
            "message": f"Processed {len(saved_db_documents_info)} document(s) successfully",
            "documents": saved_db_documents_info,
            "errors": errors
        }

    async def get_document_filepath(self, document_uid: uuid.UUID, conversation_uid: uuid.UUID, user_uid: uuid.UUID, session: AsyncSession) -> Optional[str]:
        """
        RÃ©cupÃ¨re le chemin sÃ©curisÃ© d'un document.
        VÃ©rifie les permissions utilisateur et la sÃ©curitÃ© du chemin.
        """
        conversation = await self.get_user_conversation(user_uid=user_uid, conversation_uid=conversation_uid, session=session)
        if not conversation:
            raise ForbiddenAccess("AccÃ¨s interdit Ã  cette conversation.")

        doc = await session.get(Document, document_uid)
        if not doc or doc.conversation_uid != conversation_uid:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document non trouvÃ© ou n'appartient pas Ã  la conversation.")
        
        if doc.file_path:
            base_upload_dir = os.path.abspath(Config.UPLOAD_DIR)
            full_file_path = os.path.abspath(os.path.join(base_upload_dir, doc.file_path))
            
            if os.path.commonpath([base_upload_dir]) == os.path.commonpath([base_upload_dir, full_file_path]):
                if os.path.exists(full_file_path):
                    return full_file_path
                else:
                    logger.error(f"File not found at stored path: {full_file_path}")
            else:
                logger.error(f"Invalid file path detected (potential traversal): {doc.file_path}")
        
        return None

    async def toggle_document_active_status(
        self, 
        document_uid: uuid.UUID, 
        conversation_uid: uuid.UUID, 
        user_uid: uuid.UUID,
        is_active: bool,
        session: AsyncSession
    ) -> DocumentModel:
        """
        Active ou dÃ©sactive un document pour le contexte RAG.
        Permet un contrÃ´le granulaire des documents utilisÃ©s dans les rÃ©ponses.
        """
        logger.info(f"Changement statut document {document_uid} -> actif: {is_active}")
        
        conversation = await self.get_user_conversation(user_uid, conversation_uid, session)
        if not conversation:
            raise ForbiddenAccess("AccÃ¨s interdit Ã  cette conversation.")
        
        doc = await session.get(Document, document_uid)
        if not doc or doc.conversation_uid != conversation_uid:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Document non trouvÃ© ou n'appartient pas Ã  cette conversation."
            )
        
        doc.is_active = is_active
        session.add(doc)
        await session.commit()
        await session.refresh(doc)
        
        logger.info(f"Document {document_uid} maintenant {'actif' if is_active else 'inactif'}")
        return DocumentModel.from_orm(doc)

    async def stream_rag_response_generator(
        self,
        prompt: str,
        conversation_uid: uuid.UUID,
        user: User,
        session: AsyncSession
    ):
        """
        Generator that produces RAG response in streaming and saves the message at the end.
        CORRECTED: Uses the same session throughout the process to maintain data consistency.
        """
        # Initial verification with existing session
        conversation = await self.get_user_conversation(user.uid, conversation_uid, session)
        if not conversation:
            yield "data: [ERROR] Conversation not found or access denied.\n\n"
            return

        # Prepare data for RAG processing
        try:
            chat_history = await self.get_formatted_history(conversation_uid, session)
            active_document_uids = await self.get_active_document_uids(conversation_uid, session)
        except Exception as e:
            logger.error(f"Error preparing RAG data: {e}", exc_info=True)
            yield "data: [ERROR] Error preparing conversation data.\n\n"
            return
        
        full_response_text = ""
        streaming_success = False
        
        try:
            # Stream RAG response
            async for chunk in stream_contextual_rag_response(
                question=prompt,
                active_document_uids=active_document_uids,
                chat_history=chat_history
            ):
                full_response_text += chunk
                # Format for Server-Sent Events (SSE)
                yield f"data: {chunk}\n\n"
            
            streaming_success = True
            
        except Exception as e:
            logger.error(f"RAG error during streaming: {e}", exc_info=True)
            yield "data: [ERROR] Sorry, an internal error occurred.\n\n"
            return 

        # Save message pair using the same session if streaming was successful
        if streaming_success and full_response_text:
            logger.info(f"Streaming completed for conv {conversation_uid}. Saving message...")
            
            try:
                # Use the existing session to maintain consistency
                await self.save_message_pair(
                    conversation_uid=conversation_uid,
                    user_uid=user.uid,
                    prompt=prompt,
                    response=full_response_text,
                    session=session
                )
                logger.info(f"Message pair saved successfully for conversation {conversation_uid}")
                    
            except Exception as save_error:
                logger.error(f"Error saving message after streaming: {save_error}", exc_info=True)
                # Yield error to client since save failed
                yield "data: [ERROR] Response generated but failed to save.\n\n"
                return
        
        # End of stream signal for client
        yield "data: [DONE]\n\n"

    
    
    async def stream_edit_response_generator(
        self,
        conversation_uid: uuid.UUID,
        message_uid: uuid.UUID,
        new_prompt: str,
        user: User,
        session: AsyncSession
    ):
        """
        Generator qui modifie un message et produit une réponse RAG en streaming.
        Supprime les messages ultérieurs et régénère avec le nouveau prompt.
        """
        # Vérifications initiales
        conversation = await self.get_user_conversation(user.uid, conversation_uid, session)
        if not conversation:
            yield "data: [ERROR] Conversation non trouvée ou accès interdit.\n\n"
            return
        
        message_to_edit = await self.get_message_by_uid(message_uid, session)
        if not message_to_edit or message_to_edit.conversation_uid != conversation_uid or message_to_edit.user_uid != user.uid:
            yield "data: [ERROR] Message non trouvé ou accès interdit.\n\n"
            return
            
        if not message_to_edit.prompt:
            yield "data: [ERROR] Impossible de modifier une réponse AI.\n\n"
            return

        edit_message_timestamp = message_to_edit.created_at
        
        try:
            # Suppression des messages ultérieurs pour maintenir la cohérence
            await session.exec(delete(Message).where(
                Message.conversation_uid == conversation_uid, 
                Message.created_at > edit_message_timestamp
            ))
            
            # Récupération de l'historique antérieur au message édité
            history_messages_result = await session.exec(
                select(Message).where(
                    Message.conversation_uid == conversation_uid, 
                    Message.created_at < edit_message_timestamp
                ).order_by(Message.created_at)
            )
            formatted_history = [
                (msg.prompt, msg.response) 
                for msg in history_messages_result.all() 
                if msg.prompt and msg.response
            ]
            
            # Récupération des documents actifs
            active_document_uids = await self.get_active_document_uids(conversation_uid, session)
            
        except Exception as e:
            logger.error(f"Erreur lors de la préparation de l'édition: {e}", exc_info=True)
            yield "data: [ERROR] Erreur lors de la préparation des données.\n\n"
            return
        
        full_response_text = ""
        streaming_success = False
        
        try:
            # Stream de la nouvelle réponse RAG
            async for chunk in stream_contextual_rag_response(
                question=new_prompt,
                active_document_uids=active_document_uids,
                chat_history=formatted_history
            ):
                full_response_text += chunk
                yield f"data: {chunk}\n\n"
            
            streaming_success = True
            
        except Exception as e:
            logger.error(f"Erreur RAG pendant le streaming d'édition: {e}", exc_info=True)
            yield "data: [ERROR] Désolé, une erreur interne est survenue.\n\n"
            return 

        # Sauvegarde du message modifié si le streaming s'est bien passé
        if streaming_success and full_response_text:
            logger.info(f"Streaming d'édition terminé pour conv {conversation_uid}. Sauvegarde...")
            
            try:
                # Mise à jour du message existant
                message_to_edit.prompt = new_prompt
                message_to_edit.response = full_response_text
                message_to_edit.update_at = datetime.utcnow()
                session.add(message_to_edit)
                
                # Mise à jour de la conversation
                conversation.update_at = datetime.utcnow()
                session.add(conversation)
                
                await session.commit()
                logger.info(f"Message modifié sauvegardé avec succès pour la conversation {conversation_uid}")
                    
            except Exception as save_error:
                logger.error(f"Erreur lors de la sauvegarde après streaming d'édition: {save_error}", exc_info=True)
                await session.rollback()
                yield "data: [ERROR] Réponse générée mais échec de la sauvegarde.\n\n"
                return
        
        # Signal de fin de stream
        yield "data: [DONE]\n\n"