import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP, func, text
from sqlmodel import Boolean, Column, Field, Relationship, SQLModel, Index


# --- Modèle Utilisateur ---
class User(SQLModel, table=True):
    """Modèle représentant un utilisateur de l'application"""
    __tablename__ = "users"
    
    # Identifiant unique généré automatiquement par la base de données
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, server_default=text("gen_random_uuid()"))
    )
    username: str
    # Email unique avec index pour des recherches rapides
    email:str = Field(index=True, unique=True)
    first_name: str
    last_name: str
    # Rôle par défaut "user"
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    is_verified: bool = Field(default=False)
    # Mot de passe haché, exclu des sérialisations
    password_hash: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False), exclude=True
    )
    verified_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=True)
    )
    # Date de création avec valeur par défaut côté serveur
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    )
    # Date de mise à jour automatique
    update_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    )

    # Relation avec les conversations (suppression en cascade)
    conversations: List["Conversation"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "cascade": "all, delete-orphan"
        }
    )
    # Relation directe avec les messages (optionnelle mais utile)
    messages: List["Message"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<User {self.username}>"


# --- Modèle Conversation ---
class Conversation(SQLModel, table=True):
    """Modèle représentant une conversation entre un utilisateur et l'IA"""
    __tablename__ = "conversations"
    
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, server_default=text("gen_random_uuid()"))
    )
    # Titre de la conversation
    title: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    # Référence vers l'utilisateur propriétaire
    user_uid: uuid.UUID = Field(foreign_key="users.uid", index=True, nullable=False)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)
    )
    update_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    )

    # Relation avec l'utilisateur
    user: User = Relationship(back_populates="conversations")

    # Relation avec les messages (ordonnés par date de création)
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "cascade": "all, delete-orphan",
            "order_by": "Message.created_at"
        }
    )

    # Relation avec les documents
    documents: List["Document"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "cascade": "all, delete-orphan"
        }
    )

    def __repr__(self) -> str:
        return f"<Conversation {self.uid} by {self.user_uid}>"


# --- Modèle Message ---
class Message(SQLModel, table=True):
    """Modèle représentant un message dans une conversation (question utilisateur et réponse IA)"""
    __tablename__ = "messages"
    
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, server_default=text("gen_random_uuid()"))
    )
    # Référence vers la conversation
    conversation_uid: uuid.UUID = Field(foreign_key="conversations.uid", index=True, nullable=False)
    # Référence vers l'utilisateur qui a envoyé le message
    user_uid: uuid.UUID = Field(foreign_key="users.uid", index=True, nullable=False)

    # Question de l'utilisateur (optionnelle)
    prompt: Optional[str] = Field(default=None, sa_column=Column(pg.TEXT))
    # Réponse de l'IA (optionnelle)
    response: Optional[str] = Field(default=None, sa_column=Column(pg.TEXT))

    # Note: Possibilité d'ajouter un champ 'role' ('user' ou 'ai') pour la logique d'affichage frontend
    # role: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)
    )
    # Moins pertinent pour les messages, mais bonne pratique
    update_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    )

    # Relation avec la conversation
    conversation: Conversation = Relationship(back_populates="messages")
    # Relation avec l'utilisateur
    user: User = Relationship(back_populates="messages")

    def __repr__(self):
        content_type = "Prompt" if self.prompt else "Response"
        return f"<{content_type} {self.uid} in Conv {self.conversation_uid}>"
    

class Document(SQLModel, table=True):
    """Modèle représentant un document uploadé dans une conversation"""
    __tablename__ = "documents"

    uid: uuid.UUID = Field(
        sa_column=Column(UUID(as_uuid=True), nullable=False, primary_key=True, server_default=text("gen_random_uuid()"))
    )
    # Nom original du fichier
    filename: str = Field(sa_column=Column(VARCHAR, nullable=False))
    # Référence vers la conversation
    conversation_uid: uuid.UUID = Field(foreign_key="conversations.uid", index=True, nullable=False)
    # Chemin de stockage du fichier (unique)
    file_path: str = Field(sa_column=Column(VARCHAR, nullable=False, unique=True))
    
    # Indicateur si le document est actif/disponible
    is_active: bool = Field(default=True, sa_column=Column(Boolean, nullable=False, server_default=text("true")))
    
    upload_date: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)
    )
    # Taille du fichier en bytes
    size: int = Field(sa_column=Column(Integer, nullable=False))
    # Type MIME du fichier
    mime_type: str = Field(sa_column=Column(VARCHAR, nullable=False))

    # Relation avec la conversation
    conversation: "Conversation" = Relationship(back_populates="documents")


# --- Index pour optimiser les performances des requêtes ---
Index("idx_conversation_user", Conversation.user_uid)
Index("idx_message_conversation", Message.conversation_uid)
Index("idx_message_user", Message.user_uid)
Index("idx_message_created_at", Message.created_at)  # Utile pour l'ordonnancement
Index("idx_document_conversation", Document.conversation_uid)  # Index pour la récupération des documents