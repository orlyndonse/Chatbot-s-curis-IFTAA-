# source code/backend/src/conversations/service.py
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

from src.db.models import Conversation, Message, User, Document
from src.errors import ConversationNotFound, ForbiddenAccess, MessageNotFound 
from .schemas import ConversationRenameModel, DocumentModel

# NOUVELLE IMPORTATION: Utiliser la nouvelle architecture RAG
from src.rag.chain import generate_contextual_rag_response
from langchain_core.documents import Document as LangchainDocument

from src.rag.loader import charger_documents, split_documents
from src.rag.vectorstore import add_documents_to_vectorstore
import aiofiles
from src.config import Config

logger = logging.getLogger(__name__)

class ConversationService:
    async def get_conversation_by_uid(
        self, conversation_uid: uuid.UUID, session: AsyncSession
    ) -> Optional[Conversation]:
        result = await session.exec(
            select(Conversation).where(Conversation.uid == conversation_uid)
        )
        return result.first()
    
    async def get_user_conversation(
        self, user_uid: uuid.UUID, conversation_uid: uuid.UUID, session: AsyncSession
    ) -> Optional[Conversation]:
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
        if not title:
             title = f"Nouvelle discussion {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
        new_conversation = Conversation(title=title, user_uid=user.uid, user=user)
        session.add(new_conversation)
        await session.commit()
        await session.refresh(new_conversation)
        logging.info(f"Created conversation {new_conversation.uid} for user {user.uid}")
        return new_conversation
    
    async def get_formatted_history(self, conversation_uid: uuid.UUID, session: AsyncSession) -> List[Tuple[str, str]]:
        stmt = select(Message).where(Message.conversation_uid == conversation_uid).order_by(Message.created_at)
        results = await session.exec(stmt)
        messages = results.all()
        history = []
        for msg in messages:
             if msg.prompt and msg.response:
                   history.append((msg.prompt, msg.response))
        return history
    
    # NOUVELLE FONCTION CRITIQUE: Obtenir les documents actifs
    async def get_active_document_uids(
        self, 
        conversation_uid: uuid.UUID, 
        session: AsyncSession
    ) -> List[str]:
        """
        Récupère les UIDs des documents actifs pour une conversation donnée.
        CETTE FONCTION EST CRITIQUE POUR LA SÉCURITÉ.
        """
        logger.info(f"Récupération des documents actifs pour la conversation {conversation_uid}")
        
        try:
            statement = select(Document).where(
                Document.conversation_uid == conversation_uid,
                Document.is_active == True  # Filtrer uniquement les documents actifs
            )
            result = await session.exec(statement)
            active_documents = result.all()
            
            active_uids = [str(doc.uid) for doc in active_documents]
            logger.info(f"Trouvé {len(active_uids)} documents actifs pour la conversation {conversation_uid}")
            
            # Log des documents pour debug (optionnel)
            for doc in active_documents:
                logger.debug(f"Document actif: {doc.uid} - {doc.filename}")
            
            return active_uids
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des documents actifs: {e}", exc_info=True)
            # En cas d'erreur, retourner une liste vide pour éviter les fuites
            return []
    
    # FONCTION MODIFIÉE: Utiliser la nouvelle architecture RAG
    async def generate_rag_response(
        self, 
        prompt: str, 
        conversation_uid: uuid.UUID, 
        session: AsyncSession
    ) -> Tuple[str, Optional[List[LangchainDocument]]]:
        logger.info(f"Génération de réponse RAG sécurisée pour la conversation {conversation_uid}")
        try:
            # 1. Récupérer l'historique de la conversation
            chat_history = await self.get_formatted_history(conversation_uid, session)
            
            # 2. CRUCIAL: Récupérer uniquement les documents actifs de cette conversation
            active_document_uids = await self.get_active_document_uids(conversation_uid, session)
            
            # 3. Générer la réponse avec le contexte sécurisé
            ai_response_text, source_documents, doc_count = await generate_contextual_rag_response(
                question=prompt,
                active_document_uids=active_document_uids,
                chat_history=chat_history
            )
            
            logger.info(f"Réponse générée avec {doc_count} documents actifs")
            
            # Log des sources utilisées (optionnel)
            if source_documents:
                logger.info(f"Sources utilisées dans la réponse: {len(source_documents)} documents")
                for i, doc in enumerate(source_documents):
                    source_info = doc.metadata.get('source', 'unknown')
                    doc_uid = doc.metadata.get('document_uid', 'unknown')
                    logger.debug(f"Source {i+1}: {source_info} (UID: {doc_uid})")
            
            return ai_response_text, source_documents
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération de la réponse RAG: {e}", exc_info=True)
            return "Désolé, je n'ai pas pu traiter votre demande en raison d'une erreur interne.", None


    async def save_message_pair(
         self, *, conversation_uid: uuid.UUID, user_uid: uuid.UUID, 
         prompt: str, response: str, session: AsyncSession
     ) -> Message:
         logger.info(f"Sauvegarde du prompt et de la réponse RAG pour la conversation {conversation_uid}")
         conversation = await self.get_conversation_by_uid(conversation_uid, session)
         if not conversation:
             logger.error(f"Conversation {conversation_uid} non trouvée.")
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation non trouvée lors de la sauvegarde.")
         user = await session.get(User, user_uid)
         if not user:
              logger.error(f"Utilisateur {user_uid} non trouvé.")
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé lors de la sauvegarde.")
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
         logger.info(f"Paire message/réponse (ID: {db_message.uid}) sauvegardée pour la conversation {conversation_uid}")
         return db_message

    async def add_message_to_conversation(
        self, conversation_uid: uuid.UUID, user: User,
        prompt_text: str, session: AsyncSession,
    ) -> Message:
        conversation = await self.get_user_conversation(user.uid, conversation_uid, session)
        if not conversation:
            raise ConversationNotFound("Conversation non trouvée ou accès interdit.")
        
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
        conversation = await self.get_user_conversation(user_uid, conversation_uid, session)
        if not conversation:
            raise ConversationNotFound("Conversation non trouvée ou accès interdit.")
        statement = (
            select(Message).where(Message.conversation_uid == conversation_uid).order_by(Message.created_at)
        )
        result = await session.exec(statement)
        return result.all()

    async def delete_conversation(
        self, conversation_uid: uuid.UUID, user_uid: uuid.UUID, session: AsyncSession
    ) -> None:
        conversation = await self.get_user_conversation(user_uid, conversation_uid, session)
        if not conversation:
            raise ConversationNotFound("Conversation non trouvée ou accès interdit pour suppression.")
        await session.delete(conversation)
        await session.commit()
        logging.info(f"Deleted conversation {conversation_uid} for user {user_uid}")
        return None
    
    async def get_message_by_uid(self, message_uid: uuid.UUID, session: AsyncSession) -> Optional[Message]:
         result = await session.exec(select(Message).where(Message.uid == message_uid))
         return result.first()

    async def edit_message_and_regenerate(
        self, conversation_uid: uuid.UUID, message_to_edit_uid: uuid.UUID,
        user_uid: uuid.UUID, new_prompt_text: str, session: AsyncSession,
    ) -> List[Message]:
        conversation = await self.get_user_conversation(user_uid, conversation_uid, session)
        if not conversation: 
            raise ConversationNotFound("Conversation non trouvée ou accès interdit.")
        message_to_edit = await self.get_message_by_uid(message_to_edit_uid, session)
        if not message_to_edit or message_to_edit.conversation_uid != conversation_uid or message_to_edit.user_uid != user_uid:
            raise MessageNotFound("Message non trouvé ou accès interdit.")
        if not message_to_edit.prompt:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Impossible de modifier une réponse AI.")
        
        edit_message_timestamp = message_to_edit.created_at
        try:
            await session.exec(delete(Message).where(
                Message.conversation_uid == conversation_uid, Message.created_at > edit_message_timestamp
            ))
            history_messages_result = await session.exec(
                select(Message).where(Message.conversation_uid == conversation_uid, Message.created_at < edit_message_timestamp).order_by(Message.created_at)
            )
            formatted_history = [(msg.prompt, msg.response) for msg in history_messages_result.all() if msg.prompt and msg.response]
            
            # MODIFICATION: Utiliser la nouvelle architecture RAG
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
            detail_message = f"Erreur modification/regénération: {e}"
            status_code_err = status.HTTP_503_SERVICE_UNAVAILABLE if "generate_rag_response" in traceback.format_exc() else status.HTTP_500_INTERNAL_SERVER_ERROR
            raise HTTPException(status_code=status_code_err, detail=detail_message)
        return await self.get_conversation_messages(conversation_uid, user_uid, session)
    
    async def rename_conversation(
            self, conversation_uid: uuid.UUID, user_uid: uuid.UUID,
            new_title: str, session: AsyncSession,
        ) -> Conversation:
            conversation = await self.get_user_conversation(user_uid, conversation_uid, session)
            if not conversation: 
                raise ConversationNotFound("Conversation non trouvée ou accès interdit.")
            conversation.title = new_title
            conversation.update_at = datetime.utcnow()
            session.add(conversation)
            await session.commit()
            await session.refresh(conversation)
            logging.info(f"Renamed conversation {conversation_uid} to '{new_title}' for user {user_uid}")
            return conversation
    
    async def get_documents_for_conversation(
        self, conversation_uid: uuid.UUID, session: AsyncSession
    ) -> List[DocumentModel]:
        """Gets all documents associated with a specific conversation."""
        try:
            statement = select(Document).where(Document.conversation_uid == conversation_uid).order_by(desc(Document.upload_date))
            result = await session.exec(statement)
            db_documents = result.all()
            return [DocumentModel.from_orm(doc) for doc in db_documents]
        except Exception as e:
            logger.error(f"Error retrieving documents for conversation {conversation_uid}: {e}", exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve documents")
    
    async def process_and_index_files(
        self, 
        files: List[UploadFile], 
        conversation_uid: uuid.UUID,
        session: AsyncSession
    ) -> dict:
        temp_dir_for_rag_processing = tempfile.mkdtemp()
        saved_db_documents_info = []
        errors = []
        
        # Ensure conversation-specific upload directory exists
        conversation_upload_path = os.path.join(Config.UPLOAD_DIR, str(conversation_uid))
        os.makedirs(conversation_upload_path, exist_ok=True)

        logger.info(f"Processing files for conversation {conversation_uid}. Saving to: {conversation_upload_path}")

        try:
            for file in files:
                try:
                    # Sanitize filename
                    safe_filename = "".join(c if c.isalnum() or c in ['.', '_', '-'] else '_' for c in file.filename)
                    if not safe_filename:
                        safe_filename = f"upload_{uuid.uuid4().hex[:8]}{os.path.splitext(file.filename)[1]}"

                    # Persistent file path
                    persistent_file_path = os.path.join(conversation_upload_path, safe_filename)
                    
                    # Read file content
                    file_content = await file.read()
                    await file.seek(0)

                    # Save to persistent location
                    async with aiofiles.open(persistent_file_path, 'wb') as out_file:
                        await out_file.write(file_content)

                    # Save Document metadata to SQL Database
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

                    # Save a copy to temp dir for RAG processing
                    temp_file_path = os.path.join(temp_dir_for_rag_processing, safe_filename)
                    async with aiofiles.open(temp_file_path, 'wb') as temp_out_file:
                        await temp_out_file.write(file_content)

                    saved_db_documents_info.append(DocumentModel.from_orm(new_db_document).model_dump(mode='json'))
                    logger.info(f"Document '{new_db_document.filename}' processed (UID: {new_db_document.uid})")

                except Exception as e_file:
                    errors.append({"filename": file.filename, "error": str(e_file)})
                    logger.error(f"Error processing file {file.filename}: {e_file}", exc_info=True)
                finally:
                    await file.close()

            # Process files with RAG
            if os.listdir(temp_dir_for_rag_processing):
                logger.info(f"Loading documents for RAG from {temp_dir_for_rag_processing}")
                rag_docs_loaded = charger_documents(temp_dir_for_rag_processing)
                if rag_docs_loaded:
                    split_docs = split_documents(rag_docs_loaded)
                    if split_docs:
                        # Enrich documents with metadata before indexing
                        for doc in split_docs:
                            if not doc.metadata:
                                doc.metadata = {}
                            doc.metadata.update({
                                "document_uid": str(new_db_document.uid),
                                "conversation_uid": str(conversation_uid),
                                "source": new_db_document.filename
                            })
                        add_documents_to_vectorstore(split_docs)
                        logger.info(f"Added {len(split_docs)} document chunks to vectorstore")

            await session.commit()
            logger.info(f"Committed {len(saved_db_documents_info)} documents to database")

        except Exception as e_global:
            await session.rollback()
            errors.append({"filename": "GlobalProcessingError", "error": str(e_global)})
            logger.error(f"Global error in process_and_index_files: {e_global}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Server error during file processing"
            )
        finally:
            try:
                shutil.rmtree(temp_dir_for_rag_processing)
            except Exception as e_clean:
                logger.error(f"Error cleaning temp dir: {e_clean}")

        return {
            "message": f"Processed {len(saved_db_documents_info)} document(s) successfully",
            "documents": saved_db_documents_info,
            "errors": errors
        }

    
    async def get_document_filepath(self, document_uid: uuid.UUID, conversation_uid: uuid.UUID, user_uid: uuid.UUID, session: AsyncSession) -> Optional[str]:
        # First ensure user has access to the conversation
        conversation = await self.get_user_conversation(user_uid=user_uid, conversation_uid=conversation_uid, session=session)
        if not conversation:
            raise ForbiddenAccess("Accès interdit à cette conversation.")

        doc = await session.get(Document, document_uid)
        if not doc or doc.conversation_uid != conversation_uid:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document non trouvé ou n'appartient pas à la conversation.")
        
        # Construct absolute path
        if doc.file_path:
            base_upload_dir = os.path.abspath(Config.UPLOAD_DIR)
            full_file_path = os.path.abspath(os.path.join(base_upload_dir, doc.file_path))
            
            # Security check: ensure the resolved path is still within the UPLOAD_DIR
            if os.path.commonpath([base_upload_dir]) == os.path.commonpath([base_upload_dir, full_file_path]):
                if os.path.exists(full_file_path):
                    return full_file_path
                else:
                    logger.error(f"File not found at stored path: {full_file_path}")
            else:
                logger.error(f"Invalid file path detected (potential traversal): {doc.file_path}")
        
        return None

    # NOUVELLE FONCTION: Activer/Désactiver un document
    async def toggle_document_active_status(
        self, 
        document_uid: uuid.UUID, 
        conversation_uid: uuid.UUID, 
        user_uid: uuid.UUID,
        is_active: bool,
        session: AsyncSession
    ) -> DocumentModel:
        """
        Active ou désactive un document pour une conversation.
        FONCTION CRITIQUE pour la gestion des documents contextuels.
        """
        logger.info(f"Changement statut document {document_uid} -> actif: {is_active}")
        
        # Vérifier l'accès à la conversation
        conversation = await self.get_user_conversation(user_uid, conversation_uid, session)
        if not conversation:
            raise ForbiddenAccess("Accès interdit à cette conversation.")
        
        # Récupérer le document
        doc = await session.get(Document, document_uid)
        if not doc or doc.conversation_uid != conversation_uid:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Document non trouvé ou n'appartient pas à cette conversation."
            )
        
        # Mettre à jour le statut
        doc.is_active = is_active
        session.add(doc)
        await session.commit()
        await session.refresh(doc)
        
        logger.info(f"Document {document_uid} maintenant {'actif' if is_active else 'inactif'}")
        return DocumentModel.from_orm(doc)

    async def remove_document_from_context(
        self, document_id: uuid.UUID, conversation_uid: uuid.UUID, session: AsyncSession
    ) -> None:
        logger.info(f"Tentative de suppression du document {document_id} de la conversation {conversation_uid}")
        statement = select(Document).where(Document.uid == document_id, Document.conversation_uid == conversation_uid)
        result = await session.exec(statement)
        doc_to_delete = result.first()
        if not doc_to_delete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document non trouvé ou n'appartient pas à cette conversation.")
        
        # TODO: Ajouter la logique pour supprimer du vector store si nécessaire
        # Cela nécessiterait une fonction pour supprimer par document_uid dans vectorstore.py
        
        await session.delete(doc_to_delete)
        await session.commit()
        logger.info(f"Document {document_id} supprimé de la base de données avec succès.")