---
sidebar_position: 2
title: Modèles de Données (src/db/models.py)
---

# Modèles de Données (`src/db/models.py`)

Le fichier `src/db/models.py` définit la structure des tables de la base de données relationnelle (PostgreSQL) en utilisant SQLModel. Chaque classe héritant de `SQLModel, table=True` représente une table dans la base de données. Ces modèles sont utilisés par SQLAlchemy pour les opérations ORM et par Alembic pour générer les migrations de schéma.

## Modèle `User`

Représente un utilisateur de l'application.

```python
# Extrait de Code_Source/backend/src/db/models.py
class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, server_default=text("gen_random_uuid()"))
    )
    username: str
    email: str = Field(index=True, unique=True)
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
        default_factory=datetime.utcnow,
        sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    )
    update_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    )

    # Relations
    conversations: List["Conversation"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"}
    )
    messages: List["Message"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
```

### Champs Principaux

- **`uid (UUID)`** : Clé primaire, générée automatiquement par la base de données (`gen_random_uuid()`).
- **`username (str)`** : Nom d'utilisateur.
- **`email (str)`** : Adresse email unique, indexée.
- **`first_name (str)`, `last_name (str)`** : Prénom et nom de l'utilisateur.
- **`role (str)`** : Rôle de l'utilisateur (par défaut "user").
- **`is_verified (bool)`** : Indique si l'email de l'utilisateur a été vérifié (par défaut False).
- **`password_hash (str)`** : Hash sécurisé du mot de passe de l'utilisateur (exclu par défaut lors de la sérialisation).
- **`verified_at (Optional[datetime])`** : Date et heure de la vérification de l'email.
- **`created_at`, `update_at (datetime)`** : Timestamps pour la création et la dernière mise à jour, avec des valeurs par défaut gérées par la base de données et/ou l'application.

### Relations

- **`conversations`** : Relation un-à-plusieurs avec le modèle Conversation. La suppression d'un utilisateur entraîne la suppression de ses conversations (`cascade="all, delete-orphan"`).
- **`messages`** : Relation un-à-plusieurs avec le modèle Message.

## Modèle `Conversation`

Représente une session de chat entre un utilisateur et l'IA.

```python
# Extrait de Code_Source/backend/src/db/models.py
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, server_default=text("gen_random_uuid()"))
    )
    title: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    user_uid: uuid.UUID = Field(foreign_key="users.uid", index=True, nullable=False)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)
    )
    update_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    )

    # Relations
    user: User = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan", "order_by": "Message.created_at"}
    )
    documents: List["Document"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"}
    )
```

### Champs Principaux

- **`uid (UUID)`** : Clé primaire.
- **`title (str)`** : Titre de la conversation.
- **`user_uid (UUID)`** : Clé étrangère vers `users.uid`, indexée.
- **`created_at`, `update_at (datetime)`** : Timestamps. `created_at` est indexé.

### Relations

- **`user`** : Relation plusieurs-à-un avec le modèle User.
- **`messages`** : Relation un-à-plusieurs avec le modèle Message. La suppression d'une conversation entraîne la suppression de ses messages. Les messages sont ordonnés par `created_at`.
- **`documents`** : Relation un-à-plusieurs avec le modèle Document. La suppression d'une conversation entraîne la suppression des métadonnées de ses documents.

## Modèle `Message`

Représente une paire de question (prompt) et de réponse (IA) au sein d'une conversation.

```python
# Extrait de Code_Source/backend/src/db/models.py
class Message(SQLModel, table=True):
    __tablename__ = "messages"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, server_default=text("gen_random_uuid()"))
    )
    conversation_uid: uuid.UUID = Field(foreign_key="conversations.uid", index=True, nullable=False)
    user_uid: uuid.UUID = Field(foreign_key="users.uid", index=True, nullable=False) # User who sent the message

    prompt: Optional[str] = Field(default=None, sa_column=Column(pg.TEXT))
    response: Optional[str] = Field(default=None, sa_column=Column(pg.TEXT))

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)
    )
    update_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    )

    # Relations
    conversation: Conversation = Relationship(back_populates="messages")
    user: User = Relationship(back_populates="messages")
```

### Champs Principaux

- **`uid (UUID)`** : Clé primaire.
- **`conversation_uid (UUID)`** : Clé étrangère vers `conversations.uid`, indexée.
- **`user_uid (UUID)`** : Clé étrangère vers `users.uid` (l'utilisateur qui a initié le prompt), indexée.
- **`prompt (Optional[str])`** : Le texte de la question de l'utilisateur.
- **`response (Optional[str])`** : Le texte de la réponse générée par l'IA.
- **`created_at`, `update_at (datetime)`** : Timestamps. `created_at` est indexé.

### Relations

- **`conversation`** : Relation plusieurs-à-un avec le modèle Conversation.
- **`user`** : Relation plusieurs-à-un avec le modèle User.

## Modèle `Document`

Représente les métadonnées d'un fichier téléversé par un utilisateur dans le contexte d'une conversation.

```python
# Extrait de Code_Source/backend/src/db/models.py
class Document(SQLModel, table=True):
    __tablename__ = "documents"

    uid: uuid.UUID = Field(
        sa_column=Column(UUID(as_uuid=True), nullable=False, primary_key=True, server_default=text("gen_random_uuid()"))
    )
    filename: str = Field(sa_column=Column(VARCHAR, nullable=False))
    conversation_uid: uuid.UUID = Field(foreign_key="conversations.uid", index=True, nullable=False)
    
    file_path: str = Field(sa_column=Column(VARCHAR, nullable=False, unique=True))
    upload_date: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)
    )
    size: int = Field(sa_column=Column(Integer, nullable=False))
    mime_type: str = Field(sa_column=Column(VARCHAR, nullable=False))

    # Relation
    conversation: "Conversation" = Relationship(back_populates="documents")
```

### Champs Principaux

- **`uid (UUID)`** : Clé primaire.
- **`filename (str)`** : Nom original du fichier téléversé.
- **`conversation_uid (UUID)`** : Clé étrangère vers `conversations.uid`, indiquant à quelle conversation ce document est principalement associé pour le contexte. Indexée.
- **`file_path (str)`** : Chemin relatif (par rapport à `Config.UPLOAD_DIR`) où le fichier est stocké sur le serveur. Unique.
- **`upload_date (datetime)`** : Date et heure du téléversement. Indexée.
- **`size (int)`** : Taille du fichier en octets.
- **`mime_type (str)`** : Type MIME du fichier.

### Relation

- **`conversation`** : Relation plusieurs-à-un avec le modèle Conversation.

## Index

Plusieurs index sont explicitement définis pour optimiser les requêtes courantes :

- `idx_conversation_user` sur `Conversation.user_uid`
- `idx_message_conversation` sur `Message.conversation_uid`
- `idx_message_user` sur `Message.user_uid`
- `idx_message_created_at` sur `Message.created_at`
- `idx_document_conversation` sur `Document.conversation_uid`

De plus, `User.email` est également marqué comme `index=True` et `unique=True`.

## Architecture Relationnelle

Ces modèles constituent le schéma de la base de données principale de l'application, gérant les utilisateurs, leurs interactions et les documents qu'ils fournissent. L'architecture relationnelle permet :

- **Intégrité référentielle** : Les relations entre les entités sont maintenues par des clés étrangères
- **Cascade de suppression** : La suppression d'un utilisateur ou d'une conversation entraîne automatiquement la suppression des entités liées
- **Optimisation des performances** : Les index permettent des requêtes rapides sur les champs fréquemment utilisés
- **Traçabilité** : Tous les modèles incluent des timestamps de création et de mise à jour

---

Maintenant que nous avons vu les modèles, la prochaine section portera sur les [Migrations de Base de Données avec Alembic](../database-interaction/migrations.md).