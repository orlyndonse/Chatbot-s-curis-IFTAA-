---
sidebar_position: 3
title: Configuration de l'Application (src/config.py)
---

# Configuration de l'Application (`src/config.py`)

Le fichier `src/config.py` est central pour la gestion de la configuration de l'application backend. Il utilise la bibliothèque [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) pour charger, valider et rendre accessibles les paramètres de configuration à partir de variables d'environnement et/ou d'un fichier `.env`.

## Rôle

Ce module a pour objectif de :
* Centraliser toutes les configurations nécessaires au fonctionnement de l'application.
* Valider les types de données des variables de configuration.
* Permettre une configuration flexible selon les environnements (développement, test, production) via les variables d'environnement ou un fichier `.env`.
* Fournir un accès typé et facile aux configurations dans le reste de l'application.

## Structure du Fichier

Le fichier définit une classe `Settings` qui hérite de `BaseSettings` de Pydantic. Chaque attribut de cette classe représente un paramètre de configuration.

```python
# Extrait de Code_Source/backend/src/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    DOMAIN: str
    FRONTEND_URL: str = "http://localhost:3000"
    GEMINI_API_KEY: str

    UPLOAD_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploaded_files")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

Config = Settings()

if not os.path.exists(Config.UPLOAD_DIR):
    os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
```

## Paramètres de Configuration Clés

Voici les principaux paramètres définis et leur utilité :

### Base de Données et Cache

- **DATABASE_URL** (str) : L'URL de connexion à la base de données PostgreSQL. Format attendu : `postgresql+asyncpg://user:password@host:port/dbname`.
- **REDIS_HOST** (str, défaut: "localhost") : L'hôte du serveur Redis, utilisé pour la blocklist des tokens.
- **REDIS_PORT** (int, défaut: 6379) : Le port du serveur Redis.

### Authentification

- **JWT_SECRET** (str) : La clé secrète utilisée pour signer et vérifier les tokens JWT (JSON Web Tokens) pour l'authentification.
- **JWT_ALGORITHM** (str) : L'algorithme utilisé pour la signature des tokens JWT (par exemple, "HS256").

### Configuration Email

- **MAIL_USERNAME**, **MAIL_PASSWORD**, **MAIL_FROM**, **MAIL_PORT**, **MAIL_SERVER**, **MAIL_FROM_NAME** : Ensemble des paramètres nécessaires pour configurer le service d'envoi d'emails (utilisé pour la vérification de compte et la réinitialisation de mot de passe).
- **MAIL_STARTTLS**, **MAIL_SSL_TLS**, **USE_CREDENTIALS**, **VALIDATE_CERTS** : Options de configuration supplémentaires pour la connexion au serveur SMTP.

### URLs et Domaines

- **DOMAIN** (str) : Le domaine principal sur lequel l'application est hébergée. Utilisé pour construire des URLs absolues (par exemple, dans les emails).
- **FRONTEND_URL** (str, défaut: "http://localhost:3000") : L'URL de base de l'application frontend. Utilisée pour construire les liens de redirection dans les emails (vérification, réinitialisation de mot de passe).

### Services Externes

- **GEMINI_API_KEY** (str) : La clé API pour accéder aux services de Google Generative AI (Gemini), utilisée par le pipeline RAG.

### Stockage de Fichiers

- **UPLOAD_DIR** (str, défaut: chemin vers `Code_Source/backend/uploaded_files`) : Le chemin absolu du répertoire sur le serveur où les fichiers téléversés par les utilisateurs seront stockés physiquement. Le code s'assure que ce répertoire existe au démarrage.

## Chargement de la Configuration

```python
model_config = SettingsConfigDict(env_file=".env", extra="ignore")
```

Cette configuration indique à Pydantic de charger les valeurs des paramètres :
1. **D'abord** depuis les variables d'environnement du système.
2. **Ensuite**, si une variable n'est pas trouvée dans l'environnement, Pydantic tentera de la charger depuis un fichier nommé `.env` situé à la racine du projet backend.
3. **extra="ignore"** signifie que si des variables supplémentaires sont présentes dans le fichier `.env` ou l'environnement qui ne correspondent pas à des attributs de la classe `Settings`, elles seront ignorées sans erreur.

```python
Config = Settings()
```

Une instance de la classe `Settings` est créée sous le nom `Config`. C'est cet objet `Config` qui sera importé et utilisé dans les autres modules de l'application pour accéder aux valeurs de configuration.

## Création du Répertoire d'Upload

À la fin du fichier, un bloc de code vérifie l'existence du répertoire défini par `Config.UPLOAD_DIR` et le crée s'il n'existe pas. Cela garantit que l'application dispose d'un endroit où sauvegarder les fichiers dès son démarrage.

```python
if not os.path.exists(Config.UPLOAD_DIR):
    os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
```

## Avantages de cette Approche

Ce mécanisme de configuration centralisé et basé sur Pydantic offre :
- **Robustesse** : Validation automatique des types de données
- **Flexibilité** : Configuration via variables d'environnement ou fichier `.env`
- **Sécurité** : Centralisation des paramètres sensibles
- **Maintenabilité** : Un seul point de configuration pour toute l'application

---

Maintenant, on va aborder Le fichier src/middleware.py qui est responsable de [la configuration et l'enregistrement des middlewares FastAPI pour l'application backend](../backend/middleware.md)