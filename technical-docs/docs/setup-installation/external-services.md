---
sidebar_position: 4
title: Configuration des Services Externes
---

# Configuration des Services Externes (PostgreSQL, Redis)

L'Assistant RAG Fiqh dépend de deux services externes principaux pour son fonctionnement : une base de données PostgreSQL et un serveur Redis. Cette section donne des indications générales pour leur configuration si vous ne les exécutez pas via Docker.

Si vous utilisez Docker et un fichier `docker-compose.yml` (non fourni dans ce projet de base mais recommandé pour faciliter le développement), la configuration de ces services sera largement automatisée. Les instructions ci-dessous concernent une installation et une configuration manuelles.

## 1. PostgreSQL

PostgreSQL est utilisé comme base de données relationnelle principale pour stocker les informations des utilisateurs, les conversations, les messages, et les métadonnées des documents.

* **Installation**:
    * Suivez les instructions officielles sur [postgresql.org/download/](https://www.postgresql.org/download/) pour votre système d'exploitation.
* **Création de la Base de Données**:
    * Une fois PostgreSQL installé et le service démarré, vous devez créer une base de données pour l'application. Vous pouvez le faire via la ligne de commande `psql` ou un outil graphique comme pgAdmin.
        ```sql
        CREATE DATABASE nom_de_votre_base_de_donnees;
        ```
    * Assurez-vous que l'encodage de la base de données est UTF-8.
* **Création d'un Utilisateur (Rôle)**:
    * Il est recommandé de créer un utilisateur dédié pour l'application avec les droits nécessaires sur la base de données créée.
        ```sql
        CREATE USER votre_utilisateur WITH PASSWORD 'votre_mot_de_passe_securise';
        GRANT ALL PRIVILEGES ON DATABASE nom_de_votre_base_de_donnees TO votre_utilisateur;
        ```
* **Configuration dans l'Application**:
    * Mettez à jour la variable `DATABASE_URL` dans votre fichier `.env` (à la racine de `Code_Source/backend/`) pour refléter vos informations de connexion :
        ```env
        DATABASE_URL="postgresql+asyncpg://votre_utilisateur:votre_mot_de_passe_securise@localhost:5432/nom_de_votre_base_de_donnees"
        ```
    * Assurez-vous également que l'URL dans `alembic.ini` (pour les migrations) est correctement configurée (avec un driver synchrone) :
        ```ini
        sqlalchemy.url = postgresql://votre_utilisateur:votre_mot_de_passe_securise@localhost:5432/nom_de_votre_base_de_donnees
        ```

## 2. Redis

Redis est utilisé pour la blocklist des tokens JWT, permettant d'invalider les tokens lors de la déconnexion.

* **Installation**:
    * Suivez les instructions sur [redis.io/download/](https://redis.io/download/).
    * Pour Windows, l'utilisation de WSL (Windows Subsystem for Linux) ou de ports non officiels est une option, mais Docker est souvent plus simple.
* **Démarrage du Serveur**:
    * Une fois installé, assurez-vous que le serveur Redis est en cours d'exécution. La commande par défaut est souvent `redis-server`.
* **Configuration dans l'Application**:
    * Les paramètres de connexion à Redis sont définis dans `src/config.py` et peuvent être surchargés via le fichier `.env` :
        ```env
        # Code_Source/backend/.env (Exemple pour Redis)
        REDIS_HOST="localhost"
        REDIS_PORT=6379
        ```
    * Les valeurs par défaut (`localhost` et `6379`) sont généralement suffisantes pour une installation Redis locale standard.
    * Aucun mot de passe n'est configuré par défaut dans l'application pour se connecter à Redis. Si votre instance Redis nécessite une authentification, vous devrez adapter le code dans `src/db/redis.py` pour inclure le mot de passe lors de l'initialisation du client `aioredis`.

## Considérations de Sécurité

* Pour un environnement de production, assurez-vous que PostgreSQL et Redis sont correctement sécurisés (mots de passe forts, configuration du pare-feu, écoute uniquement sur les interfaces réseau nécessaires, etc.).
* N'utilisez pas les identifiants par défaut ou des mots de passe faibles.

Une fois ces services externes configurés et en cours d'exécution, et après avoir configuré le backend et le frontend, votre environnement de développement local devrait être pleinement opérationnel.

---

La configuration de l'environnement de développement étant maintenant couverte, la section suivante abordera les [Considérations Générales pour le Déploiement](../deployment/general-considerations.md).