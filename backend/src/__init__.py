import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.auth.routes import auth_router
from src.conversations.routes import conversation_router
from .errors import register_all_errors
from .middleware import register_middleware
from src.rag.chain import initialize_rag_chain

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration API
version = "v1"
version_prefix = f"/api/{version}"

description = """
A REST API for a RAG chat service.

Features:
- User Authentication (Signup, Login, Verification, Password Reset)
- Conversation Management (Create, List, Delete)
- Messaging within Conversations (User Prompts & AI Responses via RAG)
"""

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gère l'initialisation et l'arrêt de l'application."""
    logger.info("Démarrage de l'application FastAPI...")
    print("INFO:     Application startup...")

    # Initialisation du RAG
    logger.info("Tentative d'initialisation de la chaîne RAG...")
    print("INFO:     Initialisation de la chaîne RAG...")
    try:
        initialize_rag_chain()
        logger.info("Initialisation RAG terminée avec succès.")
        print("INFO:     Initialisation RAG terminée.")
    except Exception as e:
        logger.critical(f"ERREUR CRITIQUE lors de l'initialisation RAG: {e}", exc_info=True)
        print(f"ERROR:    ERREUR CRITIQUE lors de l'initialisation RAG: {e}")

    yield

    logger.info("Arrêt de l'application FastAPI...")
    print("INFO:     Application shutdown.")

# Création de l'instance FastAPI
app = FastAPI(
    title="RAG Chat Backend",
    description=description,
    version=version,
    lifespan=lifespan
)

# Enregistrement des composants
register_all_errors(app)
register_middleware(app)
logger.info("Gestionnaires d'erreurs et middlewares enregistrés.")

# Routes API
app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=["Auth"])
app.include_router(conversation_router, prefix=f"{version_prefix}/conversations", tags=["Conversations"])
logger.info("Routeurs API inclus.")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to the RAG Chat API {version}"}