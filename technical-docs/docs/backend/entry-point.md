---
sidebar_position: 2
title: Point d'EntrÃ©e de l'Application (src/__init__.py)
---

# Point d'EntrÃ©e de l'Application (`src/__init__.py`)

Le fichier `src/__init__.py` sert de point d'entrÃ©e principal pour l'application backend FastAPI. C'est ici que l'instance de l'application FastAPI est crÃ©Ã©e, configurÃ©e, et oÃ¹ les diffÃ©rents modules (routeurs, middlewares, gestionnaires d'erreurs, etc.) sont assemblÃ©s.

## Configuration de l'Application

### Variables de Configuration

```python
# Configuration de base
version = "v1"
version_prefix = f"/api/{version}"

description = """
A REST API for a RAG chat service.

Features:
- User Authentication (Signup, Login, Verification, Password Reset)
- Conversation Management (Create, List, Delete)
- Messaging within Conversations (User Prompts & AI Responses via RAG)
"""
```

### Configuration du Logger

```python
# Configuration du logger (peut Ãªtre centralisÃ©e ailleurs si prÃ©fÃ©rÃ©)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
```

## Gestion du Cycle de Vie (Lifespan)

La fonction lifespan dÃ©finie dans `src/__init__.py` permet d'exÃ©cuter des opÃ©rations critiques au dÃ©marrage de l'application :

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    GÃ¨re les Ã©vÃ©nements de dÃ©marrage et d'arrÃªt de l'application.
    Initialise les composants nÃ©cessaires comme la chaÃ®ne RAG au dÃ©marrage.
    """
    logger.info("DÃ©marrage de l'application FastAPI...")
    print("INFO:     Application startup...") # Garder les prints pour visibilitÃ© immÃ©diate au dÃ©marrage

    # --- Initialisation du RAG ---
    logger.info("Tentative d'initialisation de la chaÃ®ne RAG...")
    print("INFO:     Initialisation de la chaÃ®ne RAG...")
    try:
        initialize_rag_chain() # Appelle la fonction d'initialisation de chain.py
        logger.info("Initialisation RAG terminÃ©e (succÃ¨s probable, vÃ©rifier les logs de chain.py).")
        print("INFO:     Initialisation RAG terminÃ©e (vÃ©rifiez les logs dÃ©taillÃ©s).")
    except Exception as e:
        logger.critical(f"ERREUR CRITIQUE lors de l'initialisation RAG au dÃ©marrage: {e}", exc_info=True)
        print(f"ERROR:    ERREUR CRITIQUE lors de l'initialisation RAG: {e}")
        # Vous pourriez dÃ©cider ici d'arrÃªter l'application si le RAG est essentiel,
        # ou continuer en sachant que les requÃªtes RAG Ã©choueront.

    yield # Le serveur FastAPI tourne aprÃ¨s ce point

    # --- Code d'arrÃªt (si nÃ©cessaire) ---
    logger.info("ArrÃªt de l'application FastAPI...")
    print("INFO:     Application shutdown.")
    # Ajoutez ici du code si vous avez besoin de nettoyer des ressources Ã  l'arrÃªt
```

**Points clÃ©s :**
- **Initialisation du RAG**: La tÃ¢che la plus importante effectuÃ©e au dÃ©marrage est `initialize_rag_chain()`. Cette fonction, provenant de `src.rag.chain`, configure tous les composants nÃ©cessaires au systÃ¨me RAG (LLM, VectorStore, Retriever, etc.) avant que l'application ne commence Ã  accepter des requÃªtes.
- **Double logging**: Des messages sont Ã  la fois logguÃ©s (pour les fichiers de log) et affichÃ©s via print (pour visibilitÃ© immÃ©diate au dÃ©marrage).
- **Gestion d'erreur**: En cas d'Ã©chec de l'initialisation RAG, l'application peut continuer mais les requÃªtes RAG Ã©choueront.

## Initialisation de FastAPI

L'instance de l'application FastAPI est crÃ©Ã©e avec des mÃ©tadonnÃ©es de base et la fonction lifespan :

```python
# --- CrÃ©ation de l'instance FastAPI ---
# On passe la fonction lifespan pour gÃ©rer le dÃ©marrage/arrÃªt
app = FastAPI(
    title="RAG Chat Backend",
    description=description,
    version=version,
    lifespan=lifespan # <--- IntÃ©gration de la fonction lifespan
)
```

- **title**: "RAG Chat Backend" - Titre de l'application affichÃ© dans la documentation OpenAPI (Swagger UI / ReDoc).
- **description**: Fournit une description dÃ©taillÃ©e des fonctionnalitÃ©s de l'API.
- **version**: DÃ©finit la version actuelle de l'API ("v1").
- **lifespan**: Une fonction de gestion du cycle de vie (asynccontextmanager) utilisÃ©e pour exÃ©cuter du code au dÃ©marrage et Ã  l'arrÃªt de l'application.

## Enregistrement des Modules

AprÃ¨s la crÃ©ation de l'instance app, plusieurs modules sont enregistrÃ©s dans l'ordre suivant :

### 1. Gestionnaires d'Erreurs (`register_all_errors(app)`)

```python
register_all_errors(app)
```

Cette fonction, importÃ©e de `src.errors`, enregistre des handlers pour les exceptions personnalisÃ©es et gÃ©nÃ©riques, assurant que les erreurs API renvoient des rÃ©ponses JSON structurÃ©es et des codes HTTP appropriÃ©s.

### 2. Middlewares (`register_middleware(app)`)

```python
register_middleware(app)
logger.info("Gestionnaires d'erreurs et middlewares enregistrÃ©s.")
```

ImportÃ©e de `src.middleware`, cette fonction ajoute les middlewares nÃ©cessaires Ã  l'application, tels que :
- **CORSMiddleware** pour gÃ©rer les requÃªtes Cross-Origin Resource Sharing.
- **TrustedHostMiddleware** pour des raisons de sÃ©curitÃ©.
- Un **middleware de logging personnalisÃ©** pour tracer les requÃªtes.

### 3. Routeurs API (`app.include_router(...)`)

```python
app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=["Auth"])
app.include_router(conversation_router, prefix=f"{version_prefix}/conversations", tags=["Conversations"])
logger.info("Routeurs API inclus.")
```

Les routeurs des diffÃ©rents modules sont inclus pour organiser les endpoints de l'API. Chaque routeur est associÃ© Ã  un prÃ©fixe et Ã  des tags pour la documentation OpenAPI :

- **auth_router** (depuis `src.auth.routes`) pour les endpoints d'authentification, prÃ©fixÃ© par `/api/v1/auth`.
- **conversation_router** (depuis `src.conversations.routes`) pour les endpoints liÃ©s aux conversations, prÃ©fixÃ© par `/api/v1/conversations`.

**Note sur les anciens routeurs :**
Le code contient des commentaires mentionnant que les anciens routeurs (`question_router`, `reponse_router`, `tables3_router`) sont commentÃ©s. Ils peuvent Ãªtre dÃ©commentÃ©s/supprimÃ©s selon si leur logique a Ã©tÃ© intÃ©grÃ©e ailleurs ou s'ils sont obsolÃ¨tes.

### 4. Route Racine (`@app.get("/")`)

```python
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to the RAG Chat API {version}"}
```

Un endpoint simple Ã  la racine de l'API (`/`) qui renvoie un message de bienvenue incluant la version, utile pour vÃ©rifier rapidement que l'API est en fonctionnement.

## Structure des Imports

Le fichier organise ses imports de maniÃ¨re logique :

```python
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
```

## Conclusion

Ce fichier est fondamental car il assemble toutes les piÃ¨ces du backend pour crÃ©er une application fonctionnelle et cohÃ©rente. Il orchestre l'initialisation de tous les composants nÃ©cessaires au bon fonctionnement de l'application RAG Chat Backend, en gÃ©rant particuliÃ¨rement l'initialisation critique du systÃ¨me RAG au dÃ©marrage.

---

AprÃ¨s avoir vu comment l'application est initialisÃ©e et ses modules principaux enregistrÃ©s, explorons en dÃ©tail comment la [Configuration de l'Application](../backend/configuration) (src/config.py) est gÃ©rÃ©e pour paramÃ©trer son comportement.