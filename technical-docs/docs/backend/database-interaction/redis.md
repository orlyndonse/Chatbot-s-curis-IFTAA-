---
sidebar_position: 4
title: Intégration Redis (src/db/redis.py)
---

# Intégration Redis (`src/db/redis.py`)

Le fichier `src/db/redis.py` gère l'interaction avec un serveur Redis. Dans cette application, Redis est principalement utilisé pour implémenter une blocklist (liste de blocage) pour les tokens JWT (JSON Web Tokens), un mécanisme essentiel pour la gestion de la déconnexion et l'invalidation des tokens.

## Configuration de la Connexion Redis

La connexion au serveur Redis est initialisée en utilisant la bibliothèque `aioredis` pour une compatibilité asynchrone avec FastAPI.

```python
# Extrait de Code_Source/backend/src/db/redis.py
from redis import asyncio as aioredis

from src.config import Config # Importe l'objet Config

# Expiration par défaut pour les JTI dans la blocklist (en secondes)
JTI_EXPIRY = 3600 # Équivalent à 1 heure

# Initialisation du client Redis asynchrone
token_blocklist = aioredis.StrictRedis(
    host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0
)
```

**Détails de configuration :**

- **`aioredis.StrictRedis(...)`** : Crée une instance de client Redis asynchrone.
- **`Config.REDIS_HOST` et `Config.REDIS_PORT`** : L'hôte et le port du serveur Redis sont récupérés depuis l'objet `Config` (provenant de `src/config.py`). Les valeurs par défaut sont "localhost" et 6379.
- **`db=0`** : Sélectionne la base de données Redis numéro 0 (par défaut).
- **`JTI_EXPIRY`** : Constante définissant la durée d'expiration (en secondes) des identifiants de token (JTI) stockés dans Redis. Par défaut, elle est fixée à 3600 secondes (1 heure), ce qui correspond généralement à la durée de vie d'un token d'accès.

## Fonctionnalités de la Blocklist de Tokens

### 1. Ajout d'un JTI à la Blocklist (`add_jti_to_blocklist`)

```python
# Extrait de Code_Source/backend/src/db/redis.py
async def add_jti_to_blocklist(jti: str) -> None:
    # Ajoute le JTI à Redis avec une expiration
    await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)
```

**Objectif :** Invalider un token JWT (typiquement un token d'accès lors de la déconnexion de l'utilisateur).

**Fonctionnement :**

- La fonction prend un `jti` (JWT ID, un identifiant unique présent dans le payload du token JWT) en argument.
- Elle utilise la commande `set` de Redis pour stocker ce `jti` comme clé. La valeur associée peut être une chaîne vide, car seule la présence de la clé importe.
- **`ex=JTI_EXPIRY`** : Une expiration est définie pour cette clé. Cela signifie que le `jti` sera automatiquement supprimé de Redis après la durée spécifiée, évitant ainsi que la blocklist ne grossisse indéfiniment. L'expiration est synchronisée avec la durée de vie typique des tokens d'accès.

### 2. Vérification de la Présence d'un JTI dans la Blocklist (`token_in_blocklist`)

```python
# Extrait de Code_Source/backend/src/db/redis.py
async def token_in_blocklist(jti: str) -> bool:
    # Vérifie si le JTI existe dans Redis
    jti_in_redis = await token_blocklist.get(jti)

    return jti_in_redis is not None
```

**Objectif :** Vérifier si un token JWT (identifié par son `jti`) a été révoqué (c'est-à-dire si son `jti` est présent dans la blocklist).

**Fonctionnement :**

- Prend un `jti` en argument.
- Utilise la commande `get` de Redis pour tenter de récupérer la valeur associée à ce `jti`.
- Si `token_blocklist.get(jti)` retourne une valeur (c'est-à-dire, pas `None`), cela signifie que le `jti` est dans la blocklist et donc que le token est considéré comme révoqué. La fonction retourne `True`.
- Sinon, le token n'est pas dans la blocklist, et la fonction retourne `False`.

**Utilisation :** Cette fonction est appelée par les dépendances de sécurité (comme `TokenBearer` dans `src/auth/dependencies.py`) pour s'assurer que les tokens présentés par les clients n'ont pas été invalidés.

## Avantages de l'Utilisation de Redis

L'utilisation de Redis pour la blocklist des JTI présente plusieurs avantages :

### Performance
- **Accès ultra-rapide** : Redis stocke les données en mémoire, permettant des opérations de lecture/écriture très rapides
- **Latence minimale** : Vérification quasi-instantanée de la validité des tokens

### Gestion Automatique de l'Expiration
- **Nettoyage automatique** : Les JTI expirés sont automatiquement supprimés de Redis
- **Prévention de la croissance excessive** : Évite l'accumulation infinie des tokens révoqués

### Scalabilité
- **Distribution** : Redis peut être configuré en cluster pour gérer de gros volumes
- **Haute disponibilité** : Support de la réplication maître-esclave

### Simplicité d'Implémentation
- **API simple** : Opérations `SET` et `GET` suffisantes pour la blocklist
- **Intégration facile** : Compatible avec l'architecture asynchrone de FastAPI

## Cas d'Usage Typiques

### Déconnexion d'Utilisateur
1. L'utilisateur demande une déconnexion
2. Le serveur ajoute le JTI du token d'accès à la blocklist via `add_jti_to_blocklist()`
3. Toutes les requêtes ultérieures avec ce token seront rejetées

### Révocation de Token
1. Un token est compromis ou doit être révoqué
2. Son JTI est ajouté à la bloclist
3. Le token devient immédiatement inutilisable

### Vérification de Sécurité
1. À chaque requête authentifiée, le système vérifie via `token_in_blocklist()`
2. Si le token est dans la blocklist, l'accès est refusé
3. Sinon, la requête continue normalement

Cette approche offre une méthode efficace et sécurisée pour gérer la révocation des tokens JWT, particulièrement adaptée aux tokens d'accès à courte durée de vie.

---

Nous avons couvert les aspects de la base de données relationnelle et de Redis. La prochaine section se concentrera sur les Composants RAG (src/rag/), en commençant par l'orchestration de la [chaîne RAG](../rag-components/chain.md).