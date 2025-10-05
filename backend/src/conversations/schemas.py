import uuid
from datetime import datetime
from typing import List, Optional, Annotated
from pydantic import BaseModel, Field, ConfigDict

# ===========================
# SCHÉMAS DE MESSAGE
# ===========================

class MessageBase(BaseModel):
    """Modèle de base pour les messages avec prompt et réponse optionnels."""
    prompt: Optional[str] = None
    response: Optional[str] = None

class MessageModel(MessageBase):
    """Modèle complet de message avec métadonnées."""
    uid: uuid.UUID
    conversation_uid: uuid.UUID
    user_uid: uuid.UUID 
    created_at: datetime

class MessageCreateModel(BaseModel):
    """Modèle pour la création d'un nouveau message."""
    prompt: str 

class MessageEditModel(BaseModel):
    """Modèle pour l'édition d'un message existant."""
    new_prompt: str

# ===========================
# SCHÉMAS DE CONVERSATION
# ===========================

class ConversationBase(BaseModel):
    """Modèle de base pour les conversations."""
    title: str = Field(..., max_length=100)

class ConversationCreateModel(BaseModel):
    """Modèle pour la création d'une nouvelle conversation."""
    title: Optional[str] = Field(None, max_length=100)
    first_prompt: Optional[str] = None

class ConversationModel(ConversationBase):
    """Modèle complet de conversation avec métadonnées."""
    model_config = ConfigDict(from_attributes=True)
    
    uid: uuid.UUID
    user_uid: uuid.UUID
    created_at: datetime
    update_at: datetime

class ConversationRenameModel(BaseModel):
    """Modèle pour renommer une conversation existante."""
    new_title: Annotated[str, Field(min_length=1, max_length=100)]

# ===========================
# SCHÉMAS DE DOCUMENT
# ===========================

class DocumentModel(BaseModel):
    """
    Modèle pour les documents de la bibliothèque d'un utilisateur.
    Le statut d'activation est ajouté dynamiquement en fonction du contexte de la conversation.
    """
    model_config = ConfigDict(from_attributes=True)

    uid: uuid.UUID
    filename: str = Field(..., max_length=255)
    user_uid: uuid.UUID  # CORRIGÉ : Lié à l'utilisateur
    upload_date: datetime
    size: int
    mime_type: str = Field(..., max_length=100)
    
    # NOUVEAU : Ce champ sera ajouté par la logique du service pour le frontend
    isActiveInContext: Optional[bool] = None

class DocumentUploadResponse(BaseModel):
    """Réponse pour l'upload de documents avec gestion d'erreurs."""
    message: str
    documents: List[DocumentModel]
    errors: Optional[List[dict]] = None

class DocumentDeleteResponse(BaseModel):
    """Réponse pour la suppression de documents."""
    message: str

# ===========================
# SCHÉMAS COMPOSITES
# ===========================

class ConversationDetailModel(ConversationModel):
    """
    Modèle détaillé d'une conversation incluant ses messages et documents.
    Utilisé pour les vues complètes de conversation.
    """
    model_config = ConfigDict(from_attributes=True)
    
    messages: List[MessageModel] = []
    documents: List[DocumentModel] = []

class UserConversationsModel(BaseModel):
    """
    Modèle utilisateur avec toutes ses conversations.
    Utilisé pour les vues de profil utilisateur.
    """
    model_config = ConfigDict(from_attributes=True)

    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    created_at: datetime
    update_at: datetime
    conversations: List[ConversationModel] = []