---
sidebar_position: 4
title: Middlewares (src/middleware.py)
---

# Middlewares (`src/middleware.py`)

Le fichier `src/middleware.py` est responsable de la configuration et de l'enregistrement des middlewares FastAPI pour l'application backend. Les middlewares interceptent chaque requête qui arrive au serveur et chaque réponse avant qu'elle ne soit envoyée au client, permettant d'exécuter du code global.

## Rôle des Middlewares

Dans cette application, les middlewares sont utilisés pour :
* Gérer les requêtes Cross-Origin Resource Sharing (CORS).
* Assurer que les requêtes proviennent d'hôtes de confiance (Trusted Hosts).
* Fournir un logging personnalisé pour chaque requête HTTP.

## Implémentation

La fonction principale `register_middleware(app: FastAPI)` est appelée dans `src/__init__.py` pour ajouter les middlewares à l'instance de l'application FastAPI.

```python
from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging
import os

# Origines autorisées pour CORS
origins = [
    "http://localhost:3000",  # Frontend en développement
    os.getenv("FRONTEND_URL")  # Frontend en production
]

# Désactivation du logger Uvicorn par défaut
logger = logging.getLogger("uvicorn.access")
logger.disabled = True


def register_middleware(app: FastAPI):

    # Middleware de logging personnalisé
    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)
        processing_time = time.time() - start_time

        message = f"{request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {response.status_code} completed after {processing_time}s"

        print(message)
        return response

    # Middleware CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    # Middleware de sécurité des hôtes
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0"],
    )
```

## Configuration des Origines CORS

```python
# Origines autorisées pour CORS
origins = [
    "http://localhost:3000",  # Frontend en développement
    os.getenv("FRONTEND_URL")  # Frontend en production
]
```

La liste des origines autorisées est configurée pour s'adapter aux différents environnements :
- **Développement local** : `http://localhost:3000` (URL standard du serveur de développement React)
- **Production** : URL récupérée via la variable d'environnement `FRONTEND_URL`

## Middlewares Implémentés

### 1. Logging Personnalisé (`custom_logging`)

**Objectif** : Fournir un log détaillé pour chaque requête HTTP reçue par le serveur.

**Fonctionnement** :
- Ce middleware est appliqué à toutes les requêtes (`@app.middleware("http")`).
- Il enregistre l'heure de début avant de passer la requête au prochain handler (`call_next`).
- Après que la réponse est générée, il calcule le temps de traitement.
- Un message de log formaté est ensuite affiché dans la console, contenant l'IP et le port du client, la méthode HTTP, le chemin de l'URL, le code de statut de la réponse, et le temps de traitement.

**Désactivation du logger Uvicorn** : Le logger par défaut de Uvicorn pour les accès (`uvicorn.access`) est désactivé pour éviter les logs dupliqués ou pour avoir un contrôle total sur le format des logs d'accès.

### 2. CORSMiddleware

**Objectif** : Permettre au frontend (hébergé sur une origine différente, par exemple `http://localhost:3000`) de faire des requêtes à l'API backend (par exemple, `http://localhost:8000`).

**Configuration** :
- **allow_origins** : Définit une liste des origines autorisées à accéder à l'API. Elle inclut `http://localhost:3000` pour le développement local et une URL configurable via la variable d'environnement `FRONTEND_URL` pour la production.
- **allow_methods=["*"]** : Autorise toutes les méthodes HTTP standards.
- **allow_headers=["*"]** : Autorise tous les types d'en-têtes dans les requêtes.
- **allow_credentials=True** : Permet aux navigateurs d'envoyer des informations d'identification (comme les cookies ou les en-têtes d'autorisation) avec les requêtes cross-origin.

### 3. TrustedHostMiddleware

**Objectif** : Renforcer la sécurité en s'assurant que l'application ne répond qu'aux requêtes dont l'en-tête `Host` correspond à l'un des hôtes autorisés. Cela aide à prévenir les attaques de type "HTTP Host header attacks".

**Configuration** :
- **allowed_hosts** : Une liste des noms d'hôte ou adresses IP autorisés. Dans ce cas, elle inclut :
  - `localhost` et `127.0.0.1` pour le développement local
  - `0.0.0.0` pour les configurations de déploiement spécifiques

> **Important** : Il est crucial de configurer cette liste correctement pour les environnements de production afin d'assurer la sécurité de l'application.

## Ordre d'Exécution

L'ordre d'ajout des middlewares est important car ils sont exécutés dans l'ordre inverse de leur ajout :
1. **TrustedHostMiddleware** (ajouté en dernier, exécuté en premier)
2. **CORSMiddleware** 
3. **custom_logging** (ajouté en premier, exécuté en dernier)

## Avantages

Ces middlewares sont essentiels pour :
- **Journalisation** : Traçabilité complète des requêtes HTTP
- **Sécurité** : Protection contre les attaques Host header et gestion des origines autorisées
- **Compatibilité** : Communication fluide entre frontend et backend hébergés sur des domaines différents

---

La partie suivante est la [gestion des Erreurs](../backend/error-handling.md) qui est une autre partie cruciale du backend. Continuons avec la description du fichier (src/errors.py).