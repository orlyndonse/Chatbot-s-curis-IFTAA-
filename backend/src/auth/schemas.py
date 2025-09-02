import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict
# Assurez-vous que le chemin est correct pour ConversationModel
from src.conversations.schemas import ConversationModel

# Modèle pour la création d'un utilisateur (inscription)
class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "Orly",
                "last_name": "Ndonse",
                "username": "orlyndonse",
                "email": "orlndosyl@gmail.com",
                "password": "testpass123",
            }
        }
    }

# Modèle de base pour représenter un utilisateur
class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)  # Exclut le hash du mot de passe des réponses
    created_at: datetime
    update_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Modèle étendu avec les conversations de l'utilisateur
class UserDetailModel(UserModel):
    conversations: List[ConversationModel] = []

# Modèle pour la connexion d'un utilisateur
class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)

# Modèle pour une liste d'adresses email
class EmailModel(BaseModel):
    addresses : List[str]

# Modèle pour une seule adresse email
class SingleEmailModel(BaseModel):
    email: str

# Modèle pour la demande de réinitialisation de mot de passe
class PasswordResetRequestModel(BaseModel):
    email: str

# Modèle pour la confirmation de réinitialisation de mot de passe
class PasswordResetConfirmModel(BaseModel):
    # Utilisé par /password-reset-confirm
    token: str  # Le token est inclus ici
    new_password: str
    confirm_new_password: str

# Modèle pour la vérification d'email avec token
class VerifyTokenModel(BaseModel):
    # Utilisé par POST /verify-email pour recevoir le token dans le corps
    token: str

# Modèle de réponse pour la validation de token
class TokenValidationResponse(BaseModel):
    valid: bool
    email: Optional[str] = None  # Email associé au token si valide
    detail: Optional[str] = None  # Message détaillé en cas d'erreur