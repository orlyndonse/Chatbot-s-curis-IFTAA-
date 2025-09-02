from typing import List
import uuid
import logging

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Response
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select, desc

from src.auth.dependencies import RoleChecker, get_current_user
from src.db.main import get_session
from src.db.models import User, Document
from src.errors import ConversationNotFound, ForbiddenAccess, MessageNotFound, DocumentNotFound

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

logger = logging.getLogger(__name__)
conversation_router = APIRouter()

# Dépendance simplifiée pour les rôles utilisateur et admin
user_role_checker = Depends(RoleChecker(["user", "admin"]))


@conversation_router.get(
    "/", 
    response_model=List[ConversationModel], 
    dependencies=[user_role_checker], 
    summary="Récupérer les conversations de l'utilisateur"
)
async def list_user_conversations(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(),  # SIMPLIFIÉ
):
    """Récupère toutes les conversations d'un utilisateur."""
    return await conv_service.get_user_conversations(
        user_uid=current_user.uid, 
        session=session
    )


@conversation_router.post(
    "/", 
    response_model=ConversationModel, 
    status_code=status.HTTP_201_CREATED, 
    dependencies=[user_role_checker], 
    summary="Créer une nouvelle conversation"
)
async def create_new_conversation(
    conversation_data: ConversationCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(),  # SIMPLIFIÉ
):
    """Crée une nouvelle conversation pour l'utilisateur."""
    return await conv_service.create_conversation(
        user=current_user, 
        title=conversation_data.title, 
        session=session
    )


@conversation_router.get(
    "/{conversation_uid}/messages", 
    response_model=List[MessageModel], 
    dependencies=[user_role_checker], 
    summary="Récupérer les messages d'une conversation"
)
async def get_messages_for_conversation(
    conversation_uid: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(),  # SIMPLIFIÉ
):
    """Récupère tous les messages d'une conversation spécifique."""
    try:
        return await conv_service.get_conversation_messages(
            conversation_uid=conversation_uid, 
            user_uid=current_user.uid, 
            session=session
        )
    except ConversationNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Conversation non trouvée."
        )
    except ForbiddenAccess as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=str(e)
        )


@conversation_router.post(
    "/{conversation_uid}/messages", 
    response_model=MessageModel, 
    status_code=status.HTTP_201_CREATED, 
    dependencies=[user_role_checker], 
    summary="Ajouter un message et obtenir une réponse RAG"
)
async def add_message_to_conversation(
    conversation_uid: uuid.UUID,
    message_data: MessageCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(),  # SIMPLIFIÉ
):
    """Ajoute un message utilisateur et génère une réponse AI avec RAG."""
    try:
        # AMÉLIORÉ : Toute la logique est maintenant dans une seule méthode du service
        return await conv_service.add_message_to_conversation(
            conversation_uid=conversation_uid,
            user=current_user,
            prompt_text=message_data.prompt,
            session=session,
        )
    except (ConversationNotFound, ForbiddenAccess) as e:
        status_code = status.HTTP_404_NOT_FOUND if isinstance(e, ConversationNotFound) else status.HTTP_403_FORBIDDEN
        raise HTTPException(status_code=status_code, detail=str(e))
    except HTTPException as e:
        raise e  # Propage les erreurs HTTP déjà formatées par le service
    except Exception as e:
        logger.error(f"Erreur inattendue lors de l'ajout du message: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erreur interne du serveur."
        )
    

@conversation_router.post(
    "/{conversation_uid}/messages/stream", 
    summary="Ajouter un message et obtenir une réponse RAG en streaming",
    dependencies=[user_role_checker]
)
async def stream_message_to_conversation(
    conversation_uid: uuid.UUID,
    message_data: MessageCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(),  # SIMPLIFIÉ
):
    """
    Ajoute un message utilisateur et renvoie la réponse AI en flux continu (SSE).
    La sauvegarde du message se fait à la fin du stream dans le service.
    """
    try:
        # AMÉLIORÉ : La vérification de l'accès se fait maintenant dans le générateur
        return StreamingResponse(
            conv_service.stream_rag_response_generator(
                prompt=message_data.prompt, 
                conversation_uid=conversation_uid, 
                user=current_user,  # AMÉLIORÉ : Passer l'objet User complet
                session=session
            ), 
            media_type="text/event-stream"
        )
        
    except Exception as e:
        logger.error(f"Erreur critique dans l'endpoint de streaming: {e}", exc_info=True)
        # La gestion d'erreur fine (403, 404) est gérée dans le générateur lui-même
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erreur interne du serveur."
        )


@conversation_router.delete(
    "/{conversation_uid}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    dependencies=[user_role_checker], 
    summary="Supprimer une conversation"
)
async def delete_conversation(
    conversation_uid: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(),  # SIMPLIFIÉ
):
    """Supprime définitivement une conversation et tous ses messages."""
    try:
        await conv_service.delete_conversation(
            conversation_uid=conversation_uid, 
            user_uid=current_user.uid, 
            session=session
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ConversationNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Conversation non trouvée."
        )
    except ForbiddenAccess as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=str(e)
        )


@conversation_router.put(
    "/{conversation_uid}/messages/{message_uid}/edit", 
    response_model=List[MessageModel], 
    dependencies=[user_role_checker], 
    summary="Modifier un message et régénérer la réponse"
)
async def edit_message_in_conversation(
    conversation_uid: uuid.UUID,
    message_uid: uuid.UUID,
    edit_data: MessageEditModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(),  # SIMPLIFIÉ
):
    """Modifie un message utilisateur et régénère la réponse AI correspondante."""
    try:
        return await conv_service.edit_message_and_regenerate(
            conversation_uid=conversation_uid,
            message_to_edit_uid=message_uid,
            user_uid=current_user.uid,
            new_prompt_text=edit_data.new_prompt,
            session=session
        )
    except (ConversationNotFound, MessageNotFound) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e)
        )
    except ForbiddenAccess as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=str(e)
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(f"Erreur lors de la modification du message: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erreur interne."
        )


@conversation_router.put(
    "/{conversation_uid}/rename", 
    response_model=ConversationModel, 
    dependencies=[user_role_checker], 
    summary="Renommer une conversation"
)
async def rename_conversation_title(
    conversation_uid: uuid.UUID,
    rename_data: ConversationRenameModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(),  # SIMPLIFIÉ
):
    """Modifie le titre d'une conversation."""
    try:
        return await conv_service.rename_conversation(
            conversation_uid=conversation_uid,
            user_uid=current_user.uid,
            new_title=rename_data.new_title,
            session=session
        )
    except ConversationNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Conversation non trouvée."
        )
    except ForbiddenAccess as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Erreur lors du renommage: {e}")
        if "validation error" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                detail="Titre invalide."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erreur interne."
        )


@conversation_router.post(
    "/{conversation_uid}/upload", 
    status_code=status.HTTP_200_OK, 
    dependencies=[user_role_checker], 
    summary="Télécharger des documents pour le RAG"
)
async def upload_files_to_conversation(
    conversation_uid: uuid.UUID,
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(),  # SIMPLIFIÉ
):
    """Télécharge et indexe des documents pour enrichir le contexte RAG."""
    logger.info(f"Téléchargement de fichiers pour la conversation {conversation_uid} par l'utilisateur {current_user.uid}")
    
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Aucun fichier fourni."
        )
    
    try:
        # AMÉLIORÉ : La vérification de l'accès est maintenant gérée dans le service
        result = await conv_service.process_and_index_files(
            files=files, 
            conversation_uid=conversation_uid, 
            user_uid=current_user.uid,  # AMÉLIORÉ : Passer user_uid au lieu de vérifier ici
            session=session
        )
        
        # Préparer la réponse avec les résultats du traitement
        response_content = {
            "message": result.get("message", "Traitement terminé."),
            "documents": result.get("documents", []),
            "errors": result.get("errors", [])
        }
        
        error_count = len(response_content["errors"])
        processed_count = len(response_content["documents"])
        
        # Déterminer le code de statut en fonction des résultats
        if error_count > 0:
            status_code = (status.HTTP_207_MULTI_STATUS if processed_count > 0 
                          else status.HTTP_400_BAD_REQUEST)
            return JSONResponse(status_code=status_code, content=response_content)
        
        if processed_count == 0 and files:
            logger.warning(f"Aucun document traité pour la conversation {conversation_uid}")
            response_content["message"] = "Aucun fichier traité."
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=response_content)
        
    except (ConversationNotFound, ForbiddenAccess) as e:
        status_code = status.HTTP_404_NOT_FOUND if isinstance(e, ConversationNotFound) else status.HTTP_403_FORBIDDEN
        raise HTTPException(status_code=status_code, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erreur lors du traitement des fichiers: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erreur interne lors du traitement des fichiers."
        )


@conversation_router.get(
    "/{conversation_uid}/documents", 
    response_model=List[DocumentModel], 
    dependencies=[user_role_checker], 
    summary="Récupérer les documents d'une conversation"
)
async def get_conversation_documents(
    conversation_uid: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(),  # SIMPLIFIÉ
):
    """Récupère tous les documents associés à une conversation."""
    # AMÉLIORÉ : La vérification de l'accès est maintenant gérée dans le service
    try:
        return await conv_service.get_documents_for_conversation(
            conversation_uid=conversation_uid,
            user_uid=current_user.uid,  # AMÉLIORÉ : Passer user_uid pour vérification
            session=session
        )
    except (ConversationNotFound, ForbiddenAccess) as e:
        status_code = status.HTTP_404_NOT_FOUND if isinstance(e, ConversationNotFound) else status.HTTP_403_FORBIDDEN
        raise HTTPException(status_code=status_code, detail=str(e))


@conversation_router.delete(
    "/{conversation_uid}/documents/{document_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    dependencies=[user_role_checker], 
    summary="Supprimer un document d'une conversation"
)
async def delete_document_from_conversation(
    conversation_uid: uuid.UUID,
    document_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(),  # SIMPLIFIÉ
):
    """Supprime un document du contexte d'une conversation."""
    try:
        await conv_service.remove_document_from_context(
            document_id=document_id, 
            conversation_uid=conversation_uid,
            user_uid=current_user.uid,  # AMÉLIORÉ : Passer user_uid pour vérification
            session=session
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
        
    except (ConversationNotFound, DocumentNotFound) as e:
        if isinstance(e, (ConversationNotFound)):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Erreur lors de la suppression du document {document_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erreur interne lors de la suppression."
        )


@conversation_router.get(
    "/{conversation_uid}/documents/{document_id}/download",
    summary="Télécharger un document ou obtenir son contenu",
    dependencies=[user_role_checker]
)
async def download_document_content(
    conversation_uid: uuid.UUID,
    document_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(),  # SIMPLIFIÉ
):
    """Télécharge le contenu d'un document spécifique."""
    try:
        # Récupérer le chemin du fichier avec vérification des permissions
        file_path = await conv_service.get_document_filepath(
            document_uid=document_id,
            conversation_uid=conversation_uid,
            user_uid=current_user.uid,
            session=session
        )
        
        if not file_path:
            raise HTTPException(
                status_code=404, 
                detail="Fichier non trouvé ou chemin invalide."
            )

        # Récupérer les métadonnées du document
        doc = await session.get(Document, document_id)
        if not doc:
            raise HTTPException(
                status_code=404, 
                detail="Métadonnées du document non trouvées."
            )

        return FileResponse(
            path=file_path,
            filename=doc.filename,
            media_type=doc.mime_type
        )
        
    except ForbiddenAccess as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=str(e)
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erreur lors du téléchargement du document {document_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail="Erreur interne du serveur lors du téléchargement du fichier."
        )


@conversation_router.patch(
    "/{conversation_uid}/documents/{document_uid}/toggle-active",
    summary="Activer/désactiver un document pour le RAG",
    dependencies=[user_role_checker]
)
async def toggle_document_active_status(
    conversation_uid: uuid.UUID,
    document_uid: uuid.UUID,
    is_active: bool,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(),  # SIMPLIFIÉ
):
    """Active ou désactive un document pour le contexte RAG de la conversation."""
    try:
        updated_document = await conv_service.toggle_document_active_status(
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
        
    except (ConversationNotFound, ForbiddenAccess) as e:
        status_code = status.HTTP_404_NOT_FOUND if isinstance(e, ConversationNotFound) else status.HTTP_403_FORBIDDEN
        raise HTTPException(status_code=status_code, detail=str(e))
    except Exception as e:
        logger.error(f"Erreur lors du changement de statut du document: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors du changement de statut du document"
        )


@conversation_router.get(
    "/{conversation_uid}/documents/active",
    summary="Récupérer les documents actifs d'une conversation",
    dependencies=[user_role_checker]
)
async def get_active_documents(
    conversation_uid: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(),  # SIMPLIFIÉ
):
    """Récupère uniquement les documents actifs utilisés pour le RAG."""
    try:
        # AMÉLIORÉ : La vérification de l'accès est maintenant gérée dans le service
        active_documents = await conv_service.get_active_documents_for_conversation(
            conversation_uid=conversation_uid,
            user_uid=current_user.uid,
            session=session
        )
        
        return {
            "active_documents": [DocumentModel.from_orm(doc) for doc in active_documents],
            "count": len(active_documents)
        }
        
    except (ConversationNotFound, ForbiddenAccess) as e:
        status_code = status.HTTP_404_NOT_FOUND if isinstance(e, ConversationNotFound) else status.HTTP_403_FORBIDDEN
        raise HTTPException(status_code=status_code, detail=str(e))
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des documents actifs: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des documents actifs"
        )
    

@conversation_router.put(
    "/{conversation_uid}/messages/{message_uid}/edit/stream", 
    summary="Modifier un message et rÃ©gÃ©nÃ©rer la rÃ©ponse en streaming",
    dependencies=[user_role_checker]
)
async def stream_edit_message_in_conversation(
    conversation_uid: uuid.UUID,
    message_uid: uuid.UUID,
    edit_data: MessageEditModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(),
):
    """Modifie un message utilisateur et rÃ©gÃ©nÃ¨re la rÃ©ponse AI en streaming."""
    try:
        return StreamingResponse(
            conv_service.stream_edit_response_generator(
                conversation_uid=conversation_uid,
                message_uid=message_uid,
                new_prompt=edit_data.new_prompt,
                user=current_user,
                session=session
            ), 
            media_type="text/event-stream"
        )
        
    except Exception as e:
        logger.error(f"Erreur critique dans l'endpoint de streaming d'édition: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erreur interne du serveur."
        )