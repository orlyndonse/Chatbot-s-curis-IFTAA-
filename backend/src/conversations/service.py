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

from src.db.models import Conversation, Message, User, Document, ConversationDocumentLink

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
        """Crée une nouvelle conversation pour un utilisateur et active tous les documents de sa bibliothèque."""
        if not title:
             title = f"Nouvelle discussion {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
        
        # Création de la conversation
        new_conversation = Conversation(title=title, user_uid=user.uid, user=user)
        session.add(new_conversation)
        await session.flush() # Pour obtenir l'UID de la nouvelle conversation

        # ---  Activer tous les documents de l'utilisateur pour cette nouvelle conversation ---
        try:
            user_docs_stmt = select(Document).where(Document.user_uid == user.uid)
            user_docs_result = await session.exec(user_docs_stmt)
            user_documents = user_docs_result.all()

            new_links = []
            for doc in user_documents:
                link = ConversationDocumentLink(
                    conversation_uid=new_conversation.uid,
                    document_uid=doc.uid,
                    is_active=True # Actif par défaut
                )
                new_links.append(link)
            
            if new_links:
                session.add_all(new_links)
            
            logger.info(f"Activé {len(new_links)} documents existants pour la nouvelle conversation {new_conversation.uid}")

        except Exception as e:
            logger.error(f"Erreur lors de l'activation des documents pour la nouvelle conversation: {e}", exc_info=True)
            # On ne bloque pas la création de la conversation, mais on log l'erreur
        
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
        Récupère les UIDs des documents qui sont explicitement actifs
        pour une conversation via la table de liaison.
        """
        logger.info(f"Récupération des documents actifs pour la conversation {conversation_uid}")
        
        try:
            # Jointure entre Document et ConversationDocumentLink
            statement = (
                select(Document.uid)
                .join(ConversationDocumentLink, Document.uid == ConversationDocumentLink.document_uid)
                .where(
                    ConversationDocumentLink.conversation_uid == conversation_uid,
                    ConversationDocumentLink.is_active == True
                )
            )
            result = await session.exec(statement)
            active_uids = [str(uid) for uid in result.all()]
            
            logger.info(f"Trouvé {len(active_uids)} documents actifs pour la conversation {conversation_uid}")
            return active_uids
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des documents actifs: {e}", exc_info=True)
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
            # Recupération de l'historique de conversation
            chat_history = await self.get_formatted_history(conversation_uid, session)
            
            # Sécurité : uniquement les documents actifs de cette conversation
            active_document_uids = await self.get_active_document_uids(conversation_uid, session)
            
            # Gérération de la réponse avec contexte sécurisé
            ai_response_text, source_documents, doc_count = await generate_contextual_rag_response(
                question=prompt,
                active_document_uids=active_document_uids,
                chat_history=chat_history
            )
            
            logger.info(f"réponse générée avec {doc_count} documents actifs")
            
            if source_documents:
                logger.info(f"Sources utilisées dans la réponse: {len(source_documents)} documents")
            
            return ai_response_text, source_documents
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération de la réponse RAG: {e}", exc_info=True)
            return "Désolé, je n'ai pas pu traiter votre demande en raison d'une erreur interne.", None

    async def save_message_pair(
         self, *, conversation_uid: uuid.UUID, user_uid: uuid.UUID, 
         prompt: str, response: str, session: AsyncSession
     ) -> Message:
         """Sauvegarde une paire prompt/réponse dans la base de données."""
         logger.info(f"Sauvegarde du prompt et de la réponse RAG pour la conversation {conversation_uid}")
         conversation = await self.get_conversation_by_uid(conversation_uid, session)
         if not conversation:
             logger.error(f"Conversation {conversation_uid} non trouvée.")
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation non trouvée lors de la sauvegarde.")
         user = await session.get(User, user_uid)
         if not user:
              logger.error(f"Utilisateur {user_uid} non trouvée.")
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvée lors de la sauvegarde.")
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
        """
        Ajoute un nouveau message Ã  une conversation avec gÃ©nÃ©ration automatique de réponse RAG.
        Vérifie les permissions utilisateur avant traitement.
        """
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
        """Récupére tous les messages d'une conversation pour un utilisateur autorisées."""
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
        """Supprime une conversation et tous ses messages associés."""
        conversation = await self.get_user_conversation(user_uid, conversation_uid, session)
        if not conversation:
            raise ConversationNotFound("Conversation non trouvée ou accès interdit pour suppression.")
        await session.delete(conversation)
        await session.commit()
        logger.info(f"Deleted conversation {conversation_uid} for user {user_uid}")
        return None
    
    async def get_message_by_uid(self, message_uid: uuid.UUID, session: AsyncSession) -> Optional[Message]:
         """récupère un message par son UID."""
         result = await session.exec(select(Message).where(Message.uid == message_uid))
         return result.first()

    async def edit_message_and_regenerate(
        self, conversation_uid: uuid.UUID, message_to_edit_uid: uuid.UUID,
        user_uid: uuid.UUID, new_prompt_text: str, session: AsyncSession,
    ) -> List[Message]:
        """
        Modifie un message et récupère la réponse ainsi que tous les messages suivants.
        Maintient la cohérence de l'historique en supprimant les messages ultérieurs.
        """
        conversation = await self.get_user_conversation(user_uid, conversation_uid, session)
        if not conversation: 
            raise ConversationNotFound("Conversation non trouvée ou accès interdit.")
        message_to_edit = await self.get_message_by_uid(message_to_edit_uid, session)
        if not message_to_edit or message_to_edit.conversation_uid != conversation_uid or message_to_edit.user_uid != user_uid:
            raise MessageNotFound("Message non trouvé ou accÃ¨s interdit.")
        if not message_to_edit.prompt:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Impossible de modifier une réponse AI.")
        
        edit_message_timestamp = message_to_edit.created_at
        try:
            # Suppression des messages ultérieurs pour maintenir la cohérence
            await session.exec(delete(Message).where(
                Message.conversation_uid == conversation_uid, Message.created_at > edit_message_timestamp
            ))
            history_messages_result = await session.exec(
                select(Message).where(Message.conversation_uid == conversation_uid, Message.created_at < edit_message_timestamp).order_by(Message.created_at)
            )
            formatted_history = [(msg.prompt, msg.response) for msg in history_messages_result.all() if msg.prompt and msg.response]
            
            # Régération avec le nouveau prompt
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
            """Renomme une conversation existante."""
            conversation = await self.get_user_conversation(user_uid, conversation_uid, session)
            if not conversation: 
                raise ConversationNotFound("Conversation non trouvée ou accès interdit.")
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
        """
        Récupère tous les documents de la bibliothèque de l'utilisateur et enrichit
        l'information avec leur statut (actif/inactif) pour la conversation actuelle.
        """
        if not await self.get_user_conversation(user_uid, conversation_uid, session):
            raise ForbiddenAccess("Accès interdit à cette conversation.")
        
        try:
            # Étape 1: Récupérer tous les documents de l'utilisateur
            user_docs_stmt = select(Document).where(Document.user_uid == user_uid).order_by(desc(Document.upload_date))
            user_docs_result = await session.exec(user_docs_stmt)
            all_user_documents = user_docs_result.all()

            # Étape 2: Récupérer les statuts d'activation pour CETTE conversation
            link_stmt = select(ConversationDocumentLink).where(
                ConversationDocumentLink.conversation_uid == conversation_uid
            )
            link_result = await session.exec(link_stmt)
            # Crée un dictionnaire pour un accès rapide: {doc_uid: is_active}
            active_statuses = {link.document_uid: link.is_active for link in link_result.all()}

            # Étape 3: Combiner les informations
            response_documents = []
            for doc in all_user_documents:
                doc_model = DocumentModel.from_orm(doc)
                # Le document est actif dans ce contexte si un lien existe et is_active=True
                doc_model.isActiveInContext = active_statuses.get(doc.uid, False)
                response_documents.append(doc_model)
                
            return response_documents
        except Exception as e:
            logger.error(f"Error retrieving documents for conversation {conversation_uid}: {e}", exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve documents")
    

    async def delete_document_permanently(
        self,
        document_id: uuid.UUID,
        user_uid: uuid.UUID,
        session: AsyncSession
    ) -> None:
        """
        Supprime un document de manière permanente : BDD, fichier physique et base vectorielle.
        Cette action est irréversible et affecte toutes les conversations.
        """
        logger.info(f"Début de la suppression permanente du document {document_id}")
        
        # 1. Récupérer le document et vérifier les permissions
        doc_to_delete = await session.get(Document, document_id)
        # Vérifier que le document appartient bien à l'utilisateur qui fait la demande
        if not doc_to_delete or doc_to_delete.user_uid != user_uid:
            raise DocumentNotFound("Document non trouvé ou accès interdit.")

        # 2. Supprimer le fichier physique
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

        # 3. Supprimer les vecteurs associés (CRUCIAL pour le RAG)
        try:
            vectorstore.delete_documents_from_vectorstore(document_uid=str(doc_to_delete.uid))
            logger.info(f"Vecteurs supprimés pour le document {doc_to_delete.uid}")
        except Exception as e:
            logger.error(f"Erreur lors de la suppression des vecteurs pour le document {doc_to_delete.uid}: {e}", exc_info=True)
            # Log l'erreur mais continuer pour que l'utilisateur voit le document disparaître
        
        # 4. Supprimer l'enregistrement de la base de données
        await session.delete(doc_to_delete)
        await session.commit()
        
        logger.info(f"Document {document_id} supprimé définitivement avec succès.")
        return None
    
    async def process_and_index_files(
        self,
        files: List[UploadFile],
        conversation_uid: uuid.UUID,
        user_uid: uuid.UUID,
        session: AsyncSession
    ) -> dict:
        """
        Traite et indexe les fichiers uploadés pour une conversation.
        """
        conversation = await self.get_user_conversation(user_uid, conversation_uid, session)
        if not conversation:
            raise ForbiddenAccess("Accès interdit à cette conversation.")

        saved_db_documents_info = []
        errors = []
        # Le chemin de sauvegarde est basé sur l'UID de l'utilisateur pour regrouper ses fichiers
        user_upload_path = os.path.join(Config.UPLOAD_DIR, str(user_uid))
        os.makedirs(user_upload_path, exist_ok=True)

        for file in files:
            temp_dir_for_rag = None
            try:
                safe_filename = "".join(c if c.isalnum() or c in ['.', '_', '-'] else '_' for c in file.filename)
                persistent_file_path = os.path.join(user_upload_path, safe_filename)
                
                file_content = await file.read()

                async with aiofiles.open(persistent_file_path, 'wb') as out_file:
                    await out_file.write(file_content)

                # Création de l'objet Document correct
                new_db_document = Document(
                    filename=safe_filename,
                    user_uid=user_uid,  # On lie à l'utilisateur
                    file_path=os.path.relpath(persistent_file_path, Config.UPLOAD_DIR),
                    size=len(file_content),
                    mime_type=file.content_type or "application/octet-stream",
                )
                session.add(new_db_document)
                await session.flush() # Pour obtenir le nouvel UID

                # Créer le lien d'activation pour la conversation courante
                link = ConversationDocumentLink(
                    conversation_uid=conversation_uid,
                    document_uid=new_db_document.uid,
                    is_active=True
                )
                session.add(link)

                # Logique RAG
                temp_dir_for_rag = tempfile.mkdtemp()
                temp_file_path = os.path.join(temp_dir_for_rag, safe_filename)
                async with aiofiles.open(temp_file_path, 'wb') as temp_out_file:
                    await temp_out_file.write(file_content)

                rag_docs_loaded = charger_documents(temp_dir_for_rag)
                if rag_docs_loaded:
                    split_docs = split_documents(rag_docs_loaded)
                    add_documents_to_vectorstore(split_docs, document_uid=str(new_db_document.uid))
                    logger.info(f"Document '{safe_filename}' (UID: {new_db_document.uid}) indexé avec {len(split_docs)} chunks")

                saved_db_documents_info.append(DocumentModel.from_orm(new_db_document).model_dump(mode='json'))

            except Exception as e_file:
                errors.append({"filename": file.filename, "error": str(e_file)})
            finally:
                if temp_dir_for_rag:
                    shutil.rmtree(temp_dir_for_rag)
                await file.close()
        
        await session.commit()
        return {
            "message": f"Processed {len(saved_db_documents_info)} document(s) successfully",
            "documents": saved_db_documents_info,
            "errors": errors
        }

    async def get_document_filepath(self, document_uid: uuid.UUID, conversation_uid: uuid.UUID, user_uid: uuid.UUID, session: AsyncSession) -> Optional[str]:
        """
        Récupère le chemin sécurisé d'un document sur le disque.
        """
        conversation = await self.get_user_conversation(user_uid=user_uid, conversation_uid=conversation_uid, session=session)
        if not conversation:
            raise ForbiddenAccess("Accès interdit à cette conversation.")

        doc = await session.get(Document, document_uid)
        if not doc or doc.user_uid != user_uid:
            raise DocumentNotFound("Document non trouvé ou accès interdit.")
        
        # Construire et retourner le chemin complet du fichier
        try:
            # On utilise le chemin relatif stocké en BDD et on le combine avec le dossier d'upload
            full_file_path = os.path.join(Config.UPLOAD_DIR, doc.file_path)
            
            # Vérification de sécurité : le fichier doit exister
            if not os.path.exists(full_file_path) or not os.path.isfile(full_file_path):
                logger.error(f"Le fichier physique est introuvable pour le document {document_uid} au chemin : {full_file_path}")
                return None
                
            return full_file_path

        except Exception as e:
            logger.error(f"Erreur lors de la construction du chemin pour le document {document_uid}: {e}", exc_info=True)
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
        Active ou désactive un document pour une conversation en créant/mettant à jour
        une entrée dans la table ConversationDocumentLink.
        """
        # 1. Vérifier que l'utilisateur a accès à la conversation et au document
        conversation = await self.get_user_conversation(user_uid, conversation_uid, session)
        if not conversation:
            raise ForbiddenAccess("Accès interdit à cette conversation.")
        
        doc = await session.get(Document, document_uid)
        if not doc or doc.user_uid != user_uid:
            raise DocumentNotFound("Document non trouvé ou n'appartient pas à cet utilisateur.")
        
        # 2. Chercher un lien existant
        link = await session.get(ConversationDocumentLink, (conversation_uid, document_uid))
        
        if link:
            # Mettre à jour le lien existant
            link.is_active = is_active
        else:
            # Créer un nouveau lien s'il n'existe pas
            link = ConversationDocumentLink(
                conversation_uid=conversation_uid,
                document_uid=document_uid,
                is_active=is_active
            )
        
        session.add(link)
        await session.commit()
        
        # 3. Retourner le modèle de document mis à jour pour le frontend
        doc_model = DocumentModel.from_orm(doc)
        doc_model.isActiveInContext = is_active
        return doc_model

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

    async def upload_documents_for_user(
        self,
        target_user_uid: uuid.UUID,
        files: List[UploadFile],
        session: AsyncSession
    ) -> dict:
        """
        Traite et indexe les fichiers uploadés par un admin pour un utilisateur cible.
        Les documents sont ajoutés à la "bibliothèque" de l'utilisateur et activés
        dans toutes ses conversations existantes.
        """
        target_user = await session.get(User, target_user_uid)
        if not target_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur cible non trouvé.")

        saved_docs_info = []
        errors = []
        user_upload_path = os.path.join(Config.UPLOAD_DIR, str(target_user_uid))
        os.makedirs(user_upload_path, exist_ok=True)

        user_conversations_stmt = select(Conversation).where(Conversation.user_uid == target_user_uid)
        user_conversations_result = await session.exec(user_conversations_stmt)
        user_conversations = user_conversations_result.all()
        logger.info(f"L'utilisateur {target_user_uid} a {len(user_conversations)} conversations existantes.")

        for file in files:
            temp_dir_for_rag = None
            try:
                # 1. Sauvegarder le fichier et créer l'entrée Document
                safe_filename = "".join(c if c.isalnum() or c in ['.', '_', '-'] else '_' for c in file.filename)
                persistent_file_path = os.path.join(user_upload_path, safe_filename)
                file_content = await file.read()

                async with aiofiles.open(persistent_file_path, 'wb') as out_file:
                    await out_file.write(file_content)

                # CRÉATION CORRECTE DE L'OBJET DOCUMENT
                new_document = Document(
                    filename=safe_filename,
                    user_uid=target_user_uid,  # Utilise user_uid
                    file_path=os.path.relpath(persistent_file_path, Config.UPLOAD_DIR),
                    size=len(file_content),
                    mime_type=file.content_type
                )
                session.add(new_document)
                await session.flush() # Pour obtenir l'UID du document

                # 2. Indexer le document dans la base vectorielle (logique ajoutée)
                temp_dir_for_rag = tempfile.mkdtemp()
                temp_file_path = os.path.join(temp_dir_for_rag, safe_filename)
                async with aiofiles.open(temp_file_path, 'wb') as temp_out_file:
                    await temp_out_file.write(file_content)
                
                rag_docs_loaded = charger_documents(temp_dir_for_rag)
                if rag_docs_loaded:
                    split_docs = split_documents(rag_docs_loaded)
                    # La fonction add_documents_to_vectorstore ajoute déjà le document_uid aux métadonnées
                    add_documents_to_vectorstore(split_docs, document_uid=str(new_document.uid))
                    logger.info(f"Document '{safe_filename}' (UID: {new_document.uid}) indexé avec {len(split_docs)} chunks")

                # 3. Activer le document pour toutes les conversations existantes
                new_links_for_this_doc = [
                    ConversationDocumentLink(
                        conversation_uid=conv.uid,
                        document_uid=new_document.uid,
                        is_active=True
                    ) for conv in user_conversations
                ]
                
                if new_links_for_this_doc:
                    session.add_all(new_links_for_this_doc)
                
                logger.info(f"Document {new_document.uid} activé pour {len(new_links_for_this_doc)} conversations.")
                
                saved_docs_info.append(DocumentModel.from_orm(new_document).model_dump(mode='json'))

            except Exception as e:
                errors.append({"filename": file.filename, "error": str(e)})
                logger.error(f"Erreur lors du traitement du fichier {file.filename}: {e}", exc_info=True)
            finally:
                if temp_dir_for_rag:
                    shutil.rmtree(temp_dir_for_rag)
                await file.close()
        
        await session.commit()
        return {"documents": saved_docs_info, "errors": errors}