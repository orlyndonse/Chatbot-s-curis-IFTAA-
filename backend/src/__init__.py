# src/__init__.py

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Import des routeurs de l'application
from src.auth.routes import auth_router
from src.conversations.routes import conversation_router # Utilise le routeur de conversation

# Import des fonctions pour enregistrer les erreurs et middlewares
from .errors import register_all_errors
from .middleware import register_middleware

# Import de la fonction d'initialisation du RAG
from src.rag.chain import initialize_rag_chain

# Configuration du logger (peut être centralisée ailleurs si préféré)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Configuration de l'application ---
version = "v1"
version_prefix = f"/api/{version}"

description = """
A REST API for a RAG chat service.

Features:
- User Authentication (Signup, Login, Verification, Password Reset)
- Conversation Management (Create, List, Delete)
- Messaging within Conversations (User Prompts & AI Responses via RAG)
"""

# --- Fonction Lifespan pour l'initialisation au démarrage ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gère les événements de démarrage et d'arrêt de l'application.
    Initialise les composants nécessaires comme la chaîne RAG au démarrage.
    """
    logger.info("Démarrage de l'application FastAPI...")
    print("INFO:     Application startup...") # Garder les prints pour visibilité immédiate au démarrage

    # --- Initialisation du RAG ---
    logger.info("Tentative d'initialisation de la chaîne RAG...")
    print("INFO:     Initialisation de la chaîne RAG...")
    try:
        initialize_rag_chain() # Appelle la fonction d'initialisation de chain.py
        logger.info("Initialisation RAG terminée (succès probable, vérifier les logs de chain.py).")
        print("INFO:     Initialisation RAG terminée (vérifiez les logs détaillés).")
    except Exception as e:
        logger.critical(f"ERREUR CRITIQUE lors de l'initialisation RAG au démarrage: {e}", exc_info=True)
        print(f"ERROR:    ERREUR CRITIQUE lors de l'initialisation RAG: {e}")
        # Vous pourriez décider ici d'arrêter l'application si le RAG est essentiel,
        # ou continuer en sachant que les requêtes RAG échoueront.

    yield # Le serveur FastAPI tourne après ce point

    # --- Code d'arrêt (si nécessaire) ---
    logger.info("Arrêt de l'application FastAPI...")
    print("INFO:     Application shutdown.")
    # Ajoutez ici du code si vous avez besoin de nettoyer des ressources à l'arrêt

# --- Création de l'instance FastAPI ---
# On passe la fonction lifespan pour gérer le démarrage/arrêt
app = FastAPI(
    title="RAG Chat Backend",
    description=description,
    version=version,
    lifespan=lifespan # <--- Intégration de la fonction lifespan
)

# --- Enregistrement des erreurs et middlewares ---
register_all_errors(app)
register_middleware(app)
logger.info("Gestionnaires d'erreurs et middlewares enregistrés.")

# --- Inclusion des Routeurs ---
app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=["Auth"])
app.include_router(conversation_router, prefix=f"{version_prefix}/conversations", tags=["Conversations"])
logger.info("Routeurs API inclus.")

# Les anciens routeurs (question_router, reponse_router, tables3_router)
# sont commentés, comme dans votre version précédente. Décommentez/supprimez
# selon si leur logique a été intégrée ailleurs ou s'ils sont obsolètes.

# Exemple de route simple à la racine (optionnel)
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to the RAG Chat API {version}"}

# --- Fin du fichier __init__.py ---