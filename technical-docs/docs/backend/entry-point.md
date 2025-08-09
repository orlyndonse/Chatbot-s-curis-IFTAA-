---
sidebar_position: 2
title: Point d'Entrée de l'Application (src/__init__.py)
---

# Point d'Entrée de l'Application (`src/__init__.py`)

Le fichier `src/__init__.py` sert de point d'entrée principal pour l'application backend FastAPI. C'est ici que l'instance de l'application FastAPI est créée, configurée, et où les différents modules (routeurs, middlewares, gestionnaires d'erreurs, etc.) sont assemblés.

## Initialisation de FastAPI

L'instance de l'application FastAPI est créée avec des métadonnées de base telles que le titre, la description et la version de l'API :

```python
# Extrait de src/__init__.py
# ...
app = FastAPI(
    title="RAG Chat Backend",
    description=description, # La description est définie plus haut dans le fichier
    version=version,         # La version est définie plus haut dans le fichier
    lifespan=lifespan        # Fonction de gestion du cycle de vie
)
# ...
```

- **title**: "RAG Chat Backend" - Titre de l'application affiché dans la documentation OpenAPI (Swagger UI / ReDoc).
- **description**: Fournit une brève description des fonctionnalités de l'API.
- **version**: Définit la version actuelle de l'API (par exemple, "v1").
- **lifespan**: Une fonction de gestion du cycle de vie (asynccontextmanager) est utilisée pour exécuter du code au démarrage et à l'arrêt de l'application.

## Gestion du Cycle de Vie (Lifespan)

La fonction lifespan définie dans `src/__init__.py` permet d'exécuter des opérations critiques au démarrage de l'application :

```python
# Extrait de src/__init__.py
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Démarrage de l'application FastAPI...")
    print("INFO:     Application startup...")

    logger.info("Tentative d'initialisation de la chaîne RAG...")
    print("INFO:     Initialisation de la chaîne RAG...")
    try:
        initialize_rag_chain() # Appelle la fonction d'initialisation de chain.py
        logger.info("Initialisation RAG terminée...")
        print("INFO:     Initialisation RAG terminée (vérifiez les logs détaillés).")
    except Exception as e:
        logger.critical(f"ERREUR CRITIQUE lors de l'initialisation RAG au démarrage: {e}", exc_info=True)
        print(f"ERROR:    ERREUR CRITIQUE lors de l'initialisation RAG: {e}")
    
    yield # Le serveur FastAPI tourne après ce point

    logger.info("Arrêt de l'application FastAPI...")
    print("INFO:     Application shutdown.")
```

- **Initialisation du RAG**: La tâche la plus importante effectuée au démarrage est `initialize_rag_chain()`. Cette fonction, provenant de `src.rag.chain`, configure tous les composants nécessaires au système RAG (LLM, VectorStore, Retriever, etc.) avant que l'application ne commence à accepter des requêtes.
- **Logging**: Des messages sont loggués pour indiquer le début et la fin du processus de démarrage, ainsi que le statut de l'initialisation RAG.

## Enregistrement des Modules

Après la création de l'instance app, plusieurs modules sont enregistrés :

### Gestionnaires d'Erreurs (`register_all_errors(app)`)

Cette fonction, importée de `src.errors`, enregistre des handlers pour les exceptions personnalisées et génériques, assurant que les erreurs API renvoient des réponses JSON structurées et des codes HTTP appropriés.

### Middlewares (`register_middleware(app)`)

Importée de `src.middleware`, cette fonction ajoute les middlewares nécessaires à l'application, tels que :
- **CORSMiddleware** pour gérer les requêtes Cross-Origin Resource Sharing.
- **TrustedHostMiddleware** pour des raisons de sécurité.
- Un **middleware de logging personnalisé** pour tracer les requêtes.

### Routeurs API (`app.include_router(...)`)

Les routeurs des différents modules sont inclus pour organiser les endpoints de l'API. Chaque routeur est associé à un préfixe et à des tags pour la documentation OpenAPI.

- **auth_router** (depuis `src.auth.routes`) pour les endpoints d'authentification, préfixé par `/api/v1/auth`.
- **conversation_router** (depuis `src.conversations.routes`) pour les endpoints liés aux conversations, préfixé par `/api/v1/conversations`.

### Route Racine (`@app.get("/")`)

Un endpoint simple à la racine de l'API (`/`) qui renvoie un message de bienvenue, utile pour vérifier rapidement que l'API est en fonctionnement.

## Conclusion

Ce fichier est donc fondamental car il assemble toutes les pièces du backend pour créer une application fonctionnelle et cohérente. Il orchestrer l'initialisation de tous les composants nécessaires au bon fonctionnement de l'application RAG Chat Backend.

---

Après avoir vu comment l'application est initialisée et ses modules principaux enregistrés, explorons en détail comment la [Configuration de l'Application](../backend/configuration) (src/config.py) est gérée pour paramétrer son comportement.