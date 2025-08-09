# src/conversations/schemas.py
import uuid
from datetime import datetime
from typing import List, Optional, Annotated
from pydantic import BaseModel, Field, ConfigDict # Ensure ConfigDict is imported

# --- Message Schemas ---
# ... (Message schemas remain the same) ...
class MessageBase(BaseModel):
    prompt: Optional[str] = None
    response: Optional[str] = None

class MessageModel(MessageBase):
    uid: uuid.UUID
    conversation_uid: uuid.UUID
    user_uid: uuid.UUID 
    created_at: datetime

class MessageCreateModel(BaseModel):
    prompt: str 

# --- Conversation Schemas ---
# ... (Conversation schemas remain the same) ...
class ConversationBase(BaseModel):
    title: str = Field(..., max_length=100)

class ConversationCreateModel(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    first_prompt: Optional[str] = None

class ConversationModel(ConversationBase):
    uid: uuid.UUID
    user_uid: uuid.UUID
    created_at: datetime
    update_at: datetime
    # If you want DocumentModel to be usable in from_orm, this model also needs the config
    # if it's ever created from an ORM object directly.
    model_config = ConfigDict(from_attributes=True)


# --- Document Schemas ---
class DocumentModel(BaseModel):
    # --- ADD THIS LINE ---
    model_config = ConfigDict(from_attributes=True)
    # --- END ADDITION ---

    uid: uuid.UUID
    filename: str = Field(..., max_length=255)
    conversation_uid: uuid.UUID
    upload_date: datetime
    size: int
    mime_type: str = Field(..., max_length=100)
    is_active: bool = Field(default=True)

# Schema for returning a conversation with its messages and documents
class ConversationDetailModel(ConversationModel):
    # This model also needs the config if it's created via from_orm
    model_config = ConfigDict(from_attributes=True)
    
    messages: List[MessageModel] = []
    documents: List[DocumentModel] = []

# Schema for user data including conversations
class UserConversationsModel(BaseModel):
    # This model also needs the config if it's created via from_orm
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

class MessageEditModel(BaseModel):
    new_prompt: str

class ConversationRenameModel(BaseModel):
    new_title: Annotated[str, Field(min_length=1, max_length=100)]

class DocumentUploadResponse(BaseModel): # This is what your route should ideally return
    message: str
    documents: List[DocumentModel] # List of successfully processed document metadata
    errors: Optional[List[dict]] = None

class DocumentDeleteResponse(BaseModel):
    message: str