from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Response
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
import uuid

from src.auth.dependencies import RoleChecker
from src.db.main import get_session
from src.db.models import User, Document
from src.auth.schemas import UserModel
from sqlalchemy import select, desc
from src.conversations.service import ConversationService
from sqlalchemy.orm import selectinload
import logging
from src.errors import DocumentNotFound
from src.conversations.schemas import DocumentModel



logger = logging.getLogger(__name__)

admin_router = APIRouter()
# Applique le vérificateur de rôle à TOUTES les routes de ce fichier
admin_dependencies = [Depends(RoleChecker(["admin"]))]

# 1. Route pour lister tous les utilisateurs
@admin_router.get("/users", response_model=List[UserModel], dependencies=admin_dependencies)
async def get_all_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).order_by(User.created_at.desc()))
    users = result.scalars().all()
    return users

# 2. Route pour supprimer un utilisateur
@admin_router.delete("/users/{user_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=admin_dependencies)
async def delete_user(
    user_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends()
):
    # On charge l'utilisateur avec ses documents pré-chargés
    user = await session.get(User, user_uid, options=[selectinload(User.documents)])
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # 1. Nettoyer complètement chaque document (fichier + vecteurs)
    documents_to_delete = list(user.documents) 
    for doc in documents_to_delete:
        try:
            # On utilise la fonction de service qui fait le nettoyage complet
            await conv_service.delete_document_permanently(
                document_id=doc.uid,
                user_uid=user.uid,
                session=session
            )
        except Exception as e:
            # On log l'erreur mais on continue pour ne pas bloquer la suppression
            logging.error(f"Échec de la suppression complète du document {doc.uid} lors de la suppression de l'utilisateur {user.uid}: {e}")

    # 2. Maintenant que les dépendances sont nettoyées, on peut supprimer l'utilisateur.
    # La cascade configurée dans models.py s'occupera des conversations et messages.
    await session.delete(user)
    await session.commit()
    
    return None

# 3. Route pour changer le rôle d'un utilisateur (exemple)
@admin_router.patch("/users/{user_uid}/role", response_model=UserModel, dependencies=admin_dependencies)
async def update_user_role(user_uid: uuid.UUID, role_data: dict, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_uid)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    new_role = role_data.get("role")
    if new_role not in ["admin", "user"]:
        raise HTTPException(status_code=400, detail="Rôle invalide")
        
    user.role = new_role
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

# 4. Route pour qu'un admin uploade des documents pour un utilisateur
@admin_router.post(
    "/users/{user_uid}/upload",
    summary="[ADMIN] Upload documents for a user",
    dependencies=admin_dependencies
)
async def admin_upload_for_user(
    user_uid: uuid.UUID,
    files: List[UploadFile] = File(...),
    session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(),
):
    """
    Permet à un administrateur d'uploader un ou plusieurs documents
    dans la bibliothèque d'un utilisateur spécifique.
    """
    user = await session.get(User, user_uid)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # --- MODIFICATION : Appeler la logique du service ---
    result = await conv_service.upload_documents_for_user(
        target_user_uid=user_uid,
        files=files,
        session=session
    )
    
    response_content = {
        "message": f"Traitement terminé pour l'utilisateur {user.username}",
        "user_uid": str(user_uid),
        "documents": result.get("documents", []),
        "errors": result.get("errors", [])
    }
    
    # Gérer la réponse en fonction du succès ou des erreurs
    if response_content["errors"]:
        status_code = status.HTTP_207_MULTI_STATUS if response_content["documents"] else status.HTTP_400_BAD_REQUEST
        return JSONResponse(status_code=status_code, content=response_content)
    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response_content)


# 5. Lister les documents d'un utilisateur spécifique
@admin_router.get(
    "/users/{user_uid}/documents",
    response_model=List[DocumentModel],
    summary="[ADMIN] Get all documents for a specific user",
    dependencies=admin_dependencies
)
async def get_user_documents_for_admin(
    user_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
):
    """
    Permet à un administrateur de récupérer la liste complète des documents
    appartenant à un utilisateur spécifique.
    """
    user = await session.get(User, user_uid)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")

    docs_stmt = select(Document).where(Document.user_uid == user_uid).order_by(desc(Document.upload_date))
    docs_result = await session.execute(docs_stmt)
    
    # On utilise .scalars() pour extraire les objets Document de chaque ligne de résultat
    documents = docs_result.scalars().all()
    
    return [DocumentModel.from_orm(doc) for doc in documents]


# 6. Supprimer un document spécifique d'un utilisateur
@admin_router.delete(
    "/users/{user_uid}/documents/{document_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="[ADMIN] Delete a specific document for a user",
    dependencies=admin_dependencies
)
async def delete_user_document_for_admin(
    user_uid: uuid.UUID,
    document_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    conv_service: ConversationService = Depends(),
):
    """
    Permet à un administrateur de supprimer de manière permanente un document
    spécifique de la bibliothèque d'un utilisateur.
    """
    # La fonction de service `delete_document_permanently` est parfaite pour ça.
    # Elle vérifie déjà que le document appartient bien à l'utilisateur
    # avant de tout supprimer (fichier, vecteurs, BDD).
    try:
        await conv_service.delete_document_permanently(
            document_id=document_uid,
            user_uid=user_uid, # On passe l'UID de l'URL pour la vérification d'appartenance
            session=session
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except DocumentNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Erreur admin lors de la suppression du document {document_uid}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la suppression du document."
        )