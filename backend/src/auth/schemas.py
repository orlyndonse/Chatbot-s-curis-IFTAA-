# src/auth/schemas.py

import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict
# Assurez-vous que le chemin est correct pour ConversationModel
from src.conversations.schemas import ConversationModel

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

class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    update_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserDetailModel(UserModel):
    conversations: List[ConversationModel] = []

class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)

class EmailModel(BaseModel):
    addresses : List[str]

class SingleEmailModel(BaseModel):
    email: str

class PasswordResetRequestModel(BaseModel):
    email: str

class PasswordResetConfirmModel(BaseModel):
    # Utilisé par /password-reset-confirm
    token: str # Le token est inclus ici
    new_password: str
    confirm_new_password: str

# --- Ré-ajout de VerifyTokenModel ---
class VerifyTokenModel(BaseModel):
    # Utilisé par POST /verify-email pour recevoir le token dans le corps
    token: str
# --- Fin Ré-ajout ---

class TokenValidationResponse(BaseModel):
    valid: bool
    email: Optional[str] = None
    detail: Optional[str] = None