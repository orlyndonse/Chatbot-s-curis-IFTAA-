# source code/backend/src/conversations/routes.py
from typing import List
import uuid
import logging

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Response
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select, desc


from src.auth.dependencies import RoleChecker, get_current_user
from src.db.main import get_session
from src.db.models import User, Document
from src.errors import ConversationNotFound, ForbiddenAccess, MessageNotFound

from .schemas import (
    ConversationCreateModel,
    ConversationDetailModel,
    ConversationModel,
    MessageCreateModel,
    MessageModel,
    MessageEditModel,
    ConversationRenameModel,
    DocumentModel,
)
from .service import ConversationService
from fastapi.responses import FileResponse

logger = logging.getLogger(__name__)
conversation_router = APIRouter()

def get_conversation_service() -> ConversationService:
    return ConversationService()

user_role_checker = Depends(RoleChecker(["user", "admin"]))

@conversation_router.get("/", response_model=List[ConversationModel], dependencies=[user_role_checker], summary="Get User's Conversations")
async def list_user_conversations(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(get_conversation_service),
):
    return await conv_service.get_user_conversations(user_uid=current_user.uid, session=session)

@conversation_router.post("/", response_model=ConversationModel, status_code=status.HTTP_201_CREATED, dependencies=[user_role_checker], summary="Create a New Conversation")
async def create_new_conversation(
    conversation_data: ConversationCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(get_conversation_service),
):
    return await conv_service.create_conversation(user=current_user, title=conversation_data.title, session=session)

@conversation_router.get("/{conversation_uid}/messages", response_model=List[MessageModel], dependencies=[user_role_checker], summary="Get Conversation Messages")
async def get_messages_for_conversation(
    conversation_uid: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(get_conversation_service),
):
    try:
        return await conv_service.get_conversation_messages(conversation_uid=conversation_uid, user_uid=current_user.uid, session=session)
    except ConversationNotFound: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation non trouvée.")
    except ForbiddenAccess as e: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@conversation_router.post("/{conversation_uid}/messages", response_model=MessageModel, status_code=status.HTTP_201_CREATED, dependencies=[user_role_checker], summary="Add a Message to Conversation and get RAG response")
async def add_message_to_conversation(
    conversation_uid: uuid.UUID, message_data: MessageCreateModel,
    current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(get_conversation_service),
):
    try:
        conversation = await conv_service.get_user_conversation(user_uid=current_user.uid, conversation_uid=conversation_uid, session=session)
        if not conversation: raise ConversationNotFound("Conversation non trouvée ou accès non autorisé.")
        ai_response_text, _ = await conv_service.generate_rag_response(prompt=message_data.prompt, conversation_uid=conversation_uid, session=session)
        return await conv_service.save_message_pair(conversation_uid=conversation_uid, user_uid=current_user.uid, prompt=message_data.prompt, response=ai_response_text, session=session)
    except (ConversationNotFound, ForbiddenAccess) as e:
        if isinstance(e, ConversationNotFound): raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except RuntimeError as e: raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
    except Exception as e: logger.error(f"Error adding message: {e}", exc_info=True); raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur interne.")

@conversation_router.delete("/{conversation_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[user_role_checker], summary="Delete a Conversation")
async def delete_conversation(
    conversation_uid: uuid.UUID, current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session), conv_service: ConversationService = Depends(get_conversation_service),
):
    try: await conv_service.delete_conversation(conversation_uid=conversation_uid, user_uid=current_user.uid, session=session); return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ConversationNotFound: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation non trouvée.")
    except ForbiddenAccess as e: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@conversation_router.put("/{conversation_uid}/messages/{message_uid}/edit", response_model=List[MessageModel], dependencies=[user_role_checker], summary="Edit a Message and Regenerate Response")
async def edit_message_in_conversation(
    conversation_uid: uuid.UUID, message_uid: uuid.UUID, edit_data: MessageEditModel,
    current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(get_conversation_service),
):
    try: return await conv_service.edit_message_and_regenerate(conversation_uid=conversation_uid, message_to_edit_uid=message_uid, user_uid=current_user.uid, new_prompt_text=edit_data.new_prompt, session=session)
    except (ConversationNotFound, MessageNotFound) as e: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ForbiddenAccess as e: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except HTTPException as e: raise e
    except Exception as e: logger.exception(f"Error editing message: {e}"); raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur interne.")

@conversation_router.put("/{conversation_uid}/rename", response_model=ConversationModel, dependencies=[user_role_checker], summary="Rename a Conversation")
async def rename_conversation_title(
    conversation_uid: uuid.UUID, rename_data: ConversationRenameModel,
    current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(get_conversation_service),
):
    try: return await conv_service.rename_conversation(conversation_uid=conversation_uid, user_uid=current_user.uid, new_title=rename_data.new_title, session=session)
    except ConversationNotFound: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation non trouvée.")
    except ForbiddenAccess as e: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e: logger.exception(f"Error renaming: {e}"); 
    if "validation error" in str(e).lower(): 
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Titre invalide."); raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur interne.")

@conversation_router.post("/{conversation_uid}/upload", status_code=status.HTTP_200_OK, dependencies=[user_role_checker], summary="Upload documents to a conversation (for RAG and DB)")
async def upload_files_to_conversation( 
    conversation_uid: uuid.UUID, files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(get_conversation_service),
):
    logger.info(f"Upload to /upload for conv {conversation_uid} by user {current_user.uid}")
    conversation = await conv_service.get_user_conversation(user_uid=current_user.uid, conversation_uid=conversation_uid, session=session)
    if not conversation: raise ConversationNotFound("Conversation non trouvée ou accès interdit.")
    if not files: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Aucun fichier fourni.")
    try:
        result = await conv_service.process_and_index_files(files=files, conversation_uid=conversation_uid, session=session)
    except HTTPException as e: raise e
    except Exception as e: logger.error(f"Erreur process_and_index_files: {e}", exc_info=True); raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur interne traitement fichiers.")
    
    response_content = {"message": result.get("message", "Traitement terminé."), "documents": result.get("documents", []), "errors": result.get("errors", [])}
    error_count = len(response_content["errors"]); processed_count = len(response_content["documents"])
    if error_count > 0: return JSONResponse(status_code=status.HTTP_207_MULTI_STATUS if processed_count > 0 else status.HTTP_400_BAD_REQUEST, content=response_content)
    if processed_count == 0 and files: logger.warning(f"Aucun document traité pour {conversation_uid}"); response_content["message"] = "Aucun fichier traité."
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_content)

@conversation_router.get("/{conversation_uid}/documents", response_model=List[DocumentModel], dependencies=[user_role_checker], summary="Get documents for a conversation")
async def get_conversation_documents(
    conversation_uid: uuid.UUID, current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session), conv_service: ConversationService = Depends(get_conversation_service),
):
    conversation = await conv_service.get_user_conversation(user_uid=current_user.uid, conversation_uid=conversation_uid, session=session)
    if not conversation: raise ForbiddenAccess("Accès non autorisé aux documents.")
    try: return await conv_service.get_documents_for_conversation(conversation_uid=conversation_uid, session=session)
    except ConversationNotFound: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation non trouvée.")

@conversation_router.delete("/{conversation_uid}/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[user_role_checker], summary="Delete a document from conversation")
async def delete_document_from_conversation(
    conversation_uid: uuid.UUID, document_id: uuid.UUID, 
    current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(get_conversation_service),
):
    try:
        conversation = await conv_service.get_user_conversation(user_uid=current_user.uid, conversation_uid=conversation_uid, session=session)
        if not conversation: raise ForbiddenAccess("Accès non autorisé.")
        await conv_service.remove_document_from_context(document_id=document_id, conversation_uid=conversation_uid, session=session)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except (ConversationNotFound, ForbiddenAccess, MessageNotFound) as e: # MessageNotFound if remove_document uses it (should be DocumentNotFound)
        if isinstance(e, (ConversationNotFound, MessageNotFound)): raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e: logger.error(f"Error deleting document {document_id}: {e}", exc_info=True); raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur interne suppression.")



@conversation_router.get(
    "/{conversation_uid}/documents/{document_id}/download",
    summary="Download a specific document or get its content for preview",
    dependencies=[user_role_checker] 
    # No response_model here as FileResponse handles it
)
async def download_document_content(
    conversation_uid: uuid.UUID,
    document_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(get_conversation_service),
):
    try:
        file_path = await conv_service.get_document_filepath(
            document_uid=document_id,
            conversation_uid=conversation_uid,
            user_uid=current_user.uid, # For ownership check
            session=session
        )
        if not file_path:
            raise HTTPException(status_code=404, detail="Fichier non trouvé ou chemin invalide.")

        # Retrieve document from DB to get filename and mime_type for FileResponse
        doc = await session.get(Document, document_id)
        if not doc: # Should not happen if get_document_filepath succeeded based on doc from DB
             raise HTTPException(status_code=404, detail="Métadonnées du document non trouvées.")

        return FileResponse(
            path=file_path, 
            filename=doc.filename, # Provides a download name for the client
            media_type=doc.mime_type # Helps browser to render correctly if possible
        )
    except ForbiddenAccess as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except HTTPException as e: # Re-raise other HTTP exceptions from service
        raise e
    except Exception as e:
        logger.error(f"Erreur téléchargement document {document_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur lors du téléchargement du fichier.")
    


@conversation_router.patch("/{conversation_uid}/documents/{document_uid}/toggle-active")
async def toggle_document_active_status(
    conversation_uid: uuid.UUID,
    document_uid: uuid.UUID,
    is_active: bool,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Active ou désactive un document pour cette conversation.
    ENDPOINT CRITIQUE pour la sécurité contextuelle.
    """
    try:
        updated_document = await ConversationService().toggle_document_active_status(
            document_uid=document_uid,
            conversation_uid=conversation_uid,
            user_uid=current_user.uid,
            is_active=is_active,
            session=session
        )
        return {
            "message": f"Document {'activé' if is_active else 'désactivé'} avec succès",
            "document": updated_document
        }
    except Exception as e:
        logger.error(f"Erreur toggle document status: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors du changement de statut du document"
        )
    
@conversation_router.get("/conversations/{conversation_uid}/documents/active")
async def get_active_documents(
    conversation_uid: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Récupère uniquement les documents actifs pour cette conversation.
    """
    try:
        # Vérifier l'accès à la conversation
        conversation = await ConversationService().get_user_conversation(
            user_uid=current_user.uid,
            conversation_uid=conversation_uid,
            session=session
        )
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation non trouvée")
        
        # Récupérer les documents actifs
        statement = select(Document).where(
            Document.conversation_uid == conversation_uid,
            Document.is_active == True
        ).order_by(desc(Document.upload_date))
        
        result = await session.exec(statement)
        active_documents = result.all()
        
        return {
            "active_documents": [DocumentModel.from_orm(doc) for doc in active_documents],
            "count": len(active_documents)
        }
        
    except Exception as e:
        logger.error(f"Erreur récupération documents actifs: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des documents actifs"
        )