---
sidebar_position: 1
title: Connexion et Session (src/db/main.py)
---

# Connexion et Gestion des Sessions SQLAlchemy (`src/db/main.py`)

Le fichier `src/db/main.py` est responsable de l'établissement de la connexion à la base de données PostgreSQL et de la fourniture des sessions de base de données pour les opérations CRUD (Create, Read, Update, Delete) dans l'application. Il utilise SQLModel, qui s'appuie sur SQLAlchemy pour la partie ORM asynchrone.

## Configuration de la Connexion

La connexion à la base de données est configurée à l'aide d'un moteur SQLAlchemy asynchrone.

```python
# Extrait de Code_Source/backend/src/db/main.py
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine # create_engine est utilisé par AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator

from src.config import Config # Importe l'objet Config

# Création du moteur asynchrone SQLAlchemy
async_engine = AsyncEngine(create_engine(url=Config.DATABASE_URL))
```

**Détails de configuration :**

- **`Config.DATABASE_URL`** : L'URL de connexion à la base de données est récupérée depuis l'objet Config (défini dans `src/config.py`). Elle doit être au format attendu par SQLAlchemy pour PostgreSQL avec un driver asynchrone (par exemple, `postgresql+asyncpg://user:password@host:port/dbname`).

- **`create_engine(url=Config.DATABASE_URL)`** : Bien que `create_engine` de SQLModel/SQLAlchemy soit synchrone par défaut, il est utilisé ici par `AsyncEngine` pour initialiser la configuration de base de la connexion.

- **`async_engine = AsyncEngine(...)`** : Crée le moteur SQLAlchemy qui gérera les connexions de manière asynchrone, compatible avec FastAPI et asyncio.

## Initialisation de la Base de Données

Une fonction `init_db()` est fournie pour créer toutes les tables définies par les modèles SQLModel si elles n'existent pas encore. Cette fonction est typiquement appelée au démarrage de l'application ou lors de la configuration initiale.

```python
# Extrait de Code_Source/backend/src/db/main.py
async def init_db() -> None:
    async with async_engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all) # Optionnel: pour supprimer les tables avant de les recréer
        await conn.run_sync(SQLModel.metadata.create_all)
```

**Fonctionnement :**

- **`async with async_engine.begin() as conn`** : Ouvre une connexion à la base de données.

- **`await conn.run_sync(SQLModel.metadata.create_all)`** : Exécute la commande `CREATE TABLE IF NOT EXISTS` pour toutes les tables déclarées via les modèles SQLModel (qui héritent de `SQLModel, table=True`).

## Fourniture des Sessions Asynchrones

Pour interagir avec la base de données, les opérations CRUD nécessitent une session. La fonction `get_session()` est une dépendance FastAPI qui fournit une session `AsyncSession` pour chaque requête qui en a besoin.

```python
# Extrait de Code_Source/backend/src/db/main.py
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    # Création d'une factory de session liée au moteur asynchrone
    Session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with Session() as session:
        yield session
```

**Détails d'implémentation :**

- **`sessionmaker(...)`** : Crée une usine (factory) de sessions configurée pour utiliser `async_engine` et la classe `AsyncSession` de SQLModel.

- **`expire_on_commit=False`** : Empêche les objets de la session d'expirer après un commit, ce qui est souvent utile dans un contexte web asynchrone.

- **`async with Session() as session`** : Crée une nouvelle session pour la durée de la requête. La session est automatiquement fermée (et les ressources libérées) à la fin du bloc `async with`.

- **`yield session`** : Fournit la session au code du endpoint de la route FastAPI.

Cette approche garantit que chaque requête dispose d'une session de base de données isolée et gérée correctement, ce qui est essentiel pour la fiabilité et la concurrence dans une application asynchrone.

## Avantages de cette Architecture

- **Gestion automatique des ressources** : Les sessions sont automatiquement fermées après chaque requête
- **Isolation des transactions** : Chaque requête dispose de sa propre session
- **Compatibilité asynchrone** : Optimisé pour les applications FastAPI asynchrones
- **Sécurité** : Prévention des fuites de sessions et des conflits de concurrence

---

Après avoir établi comment la connexion et les sessions sont gérées, nous allons détailler les [Modèles de Données](../database-interaction/models.md) (src/db/models.py) qui définissent la structure des tables.