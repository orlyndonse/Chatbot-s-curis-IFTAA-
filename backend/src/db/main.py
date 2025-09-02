from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator

from src.config import Config

# Création du moteur de base de données asynchrone
async_engine = AsyncEngine(create_engine(url=Config.DATABASE_URL))


async def init_db() -> None:
    """Initialise la base de données en créant toutes les tables définies dans les modèles"""
    async with async_engine.begin() as conn:
        # Exécute la création des tables de manière synchrone dans le contexte asynchrone
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Générateur qui fournit une session de base de données asynchrone
    Utilisé comme dépendance dans FastAPI pour l'injection de session
    """
    Session = sessionmaker(
        bind=async_engine, 
        class_=AsyncSession, 
        expire_on_commit=False  # Évite l'expiration des objets après commit
    )

    async with Session() as session:
        yield session