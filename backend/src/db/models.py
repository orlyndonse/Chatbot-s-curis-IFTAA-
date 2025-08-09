import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP, func, text
from sqlmodel import Boolean, Column, Field, Relationship, SQLModel, Index



# --- User Model (Mostly Unchanged) ---
class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, server_default=text("gen_random_uuid()")) # Use server_default
    )
    username: str
    email:str = Field(index=True, unique=True) # Added unique constraint
    first_name: str
    last_name: str
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    is_verified: bool = Field(default=False)
    password_hash: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False), exclude=True
    )
    verified_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=True)
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, # Use default_factory
        sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now(), nullable=False) # Ensure non-nullable, server default
    )
    update_at: datetime = Field(
        default_factory=datetime.utcnow, # Use default_factory
        sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False) # Ensure non-nullable, server default, onupdate
    )

    # Relationship to Conversations
    conversations: List["Conversation"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "cascade": "all, delete-orphan" # Cascade delete conversations when user is deleted
        }
    )
    # Direct relationship to Messages (optional, but can be useful)
    messages: List["Message"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"} # No cascade here, handled by conversation
    )

    def __repr__(self):
        return f"<User {self.username}>"


# --- Conversation Model (Replaces Table3) ---
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations" # Renamed table
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, server_default=text("gen_random_uuid()"))
    )
    title: str = Field(sa_column=Column(pg.VARCHAR, nullable=False)) # Store conversation title
    user_uid: uuid.UUID = Field(foreign_key="users.uid", index=True, nullable=False) # Ensure non-nullable
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)
    )
    update_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    )

    # Relationship to User
    user: User = Relationship(back_populates="conversations")

    # Relationship to Messages
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "cascade": "all, delete-orphan", # Cascade delete messages when conversation is deleted
            "order_by": "Message.created_at" # Order messages by creation time
        }
    )

    documents: List["Document"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "cascade": "all, delete-orphan"
        }
    )

    def __repr__(self) -> str:
        return f"<Conversation {self.uid} by {self.user_uid}>"


# --- Message Model (Combines Question & Reponse logic) ---
class Message(SQLModel, table=True):
    __tablename__ = "messages" # New table for all messages
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, server_default=text("gen_random_uuid()"))
    )
    conversation_uid: uuid.UUID = Field(foreign_key="conversations.uid", index=True, nullable=False)
    user_uid: uuid.UUID = Field(foreign_key="users.uid", index=True, nullable=False) # User who sent the message

    prompt: Optional[str] = Field(default=None, sa_column=Column(pg.TEXT)) # User's input
    response: Optional[str] = Field(default=None, sa_column=Column(pg.TEXT)) # AI's output

    # Consider adding a 'role' field ('user' or 'ai') if needed for frontend display logic
    # role: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)
    )
    update_at: datetime = Field( # Less relevant for messages, but good practice
        default_factory=datetime.utcnow,
        sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    )

    # Relationship to Conversation
    conversation: Conversation = Relationship(back_populates="messages")
    # Relationship to User
    user: User = Relationship(back_populates="messages")

    def __repr__(self):
        content_type = "Prompt" if self.prompt else "Response"
        return f"<{content_type} {self.uid} in Conv {self.conversation_uid}>"
    

class Document(SQLModel, table=True):
    __tablename__ = "documents"

    uid: uuid.UUID = Field(
        sa_column=Column(UUID(as_uuid=True), nullable=False, primary_key=True, server_default=text("gen_random_uuid()"))
    )
    filename: str = Field(sa_column=Column(VARCHAR, nullable=False))
    conversation_uid: uuid.UUID = Field(foreign_key="conversations.uid", index=True, nullable=False)
    file_path: str = Field(sa_column=Column(VARCHAR, nullable=False, unique=True))
    
    # Ajoutez ce champ
    is_active: bool = Field(default=True, sa_column=Column(Boolean, nullable=False, server_default=text("true")))
    
    upload_date: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)
    )
    size: int = Field(sa_column=Column(Integer, nullable=False))
    mime_type: str = Field(sa_column=Column(VARCHAR, nullable=False))

    conversation: "Conversation" = Relationship(back_populates="documents")



# Add necessary indexes
Index("idx_conversation_user", Conversation.user_uid)
Index("idx_message_conversation", Message.conversation_uid)
Index("idx_message_user", Message.user_uid)
Index("idx_message_created_at", Message.created_at) # Useful for ordering
Index("idx_document_conversation", Document.conversation_uid)  # Index for document retrieval