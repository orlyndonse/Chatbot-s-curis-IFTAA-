---
sidebar_position: 2
title: Configuration de l'Environnement Backend
---

# Configuration de l'Environnement Backend

Après avoir installé tous les [prérequis](./prerequisites.md), vous pouvez configurer l'environnement de développement pour le backend de l'Assistant RAG Fiqh. Le backend est situé dans le dossier `Code_Source/backend/`.

## Étapes de Configuration

1.  **Cloner le Dépôt**:
    * Si vous n'avez pas encore les sources du projet, clonez-les depuis le dépôt Git.
    ```bash
    git clone <URL_DE_VOTRE_DEPOT_GIT>
    cd <NOM_DU_DOSSIER_PROJET>/Code_Source/backend
    ```

2.  **Créer et Activer un Environnement Virtuel Python**:
    * Il est fortement recommandé d'utiliser un environnement virtuel pour isoler les dépendances de ce projet.
    ```bash
    python3 -m venv venv
    ```
    * Pour activer l'environnement virtuel :
        * **macOS/Linux**:
          ```bash
          source venv/bin/activate
          ```
        * **Windows (cmd.exe)**:
          ```bash
          venv\Scripts\activate.bat
          ```
        * **Windows (PowerShell)**:
          ```bash
          venv\Scripts\Activate.ps1
          ```
    * Une fois activé, votre invite de commande devrait afficher `(venv)` au début.

3.  **Installer les Dépendances Python**:
    * Toutes les dépendances Python nécessaires au backend sont listées dans le fichier `requirements.txt`.
    * Installez-les avec pip :
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurer les Variables d'Environnement (Fichier `.env`)**:
    * Le backend utilise un fichier `.env` pour charger sa configuration (voir `src/config.py`).
    * À la racine du dossier `Code_Source/backend/`, créez un fichier nommé `.env`.
    * Copiez le contenu de `src/config.py` pour connaître les variables nécessaires et remplissez-les avec vos valeurs locales. Un exemple de contenu minimal pour `.env` :

    ```env
    # Code_Source/backend/.env (Exemple)

    DATABASE_URL="postgresql+asyncpg://VOTRE_USER_PG:VOTRE_PASS_PG@localhost:5432/VOTRE_DB_NOM"
    JWT_SECRET="VOTRE_CLE_SECRETE_TRES_FORTE_POUR_JWT"
    JWT_ALGORITHM="HS256"

    REDIS_HOST="localhost"
    REDIS_PORT=6379

    # Configuration Email (Adaptez avec vos propres identifiants SMTP)
    MAIL_USERNAME="VOTRE_EMAIL_SMTP"
    MAIL_PASSWORD="VOTRE_MOT_DE_PASSE_SMTP"
    MAIL_FROM="noreply@votredomaine.com"
    MAIL_PORT=587
    MAIL_SERVER="smtp.votreserveurmail.com"
    MAIL_FROM_NAME="Assistant RAG Fiqh"
    # MAIL_STARTTLS=True (valeur par défaut dans config.py)
    # MAIL_SSL_TLS=False (valeur par défaut dans config.py)

    DOMAIN="localhost:8000" # Ou votre domaine de développement
    FRONTEND_URL="http://localhost:3000" # URL de votre frontend en local

    GEMINI_API_KEY="VOTRE_CLE_API_GEMINI"

    # UPLOAD_DIR est géré par le code, mais peut être surchargé ici si besoin.
    ```
    * **Important**: Remplacez les valeurs `VOTRE_...` par vos propres configurations.
        * Assurez-vous que la base de données PostgreSQL et le serveur Redis sont en cours d'exécution et accessibles avec les informations d'identification fournies.

5.  **Initialiser la Base de Données PostgreSQL**:
    * Assurez-vous que votre serveur PostgreSQL est démarré et que vous avez créé la base de données spécifiée dans `DATABASE_URL`.
    * La première fois, ou si vous voulez recréer les tables, vous pouvez utiliser la fonction `init_db` (bien que cela soit souvent géré par Alembic pour les schémas existants). Pour une configuration initiale avec Alembic, voir ci-dessous.

6.  **Exécuter les Migrations Alembic**:
    * Pour créer ou mettre à jour le schéma de la base de données en fonction des modèles SQLModel, utilisez Alembic.
    * Assurez-vous que la variable `sqlalchemy.url` dans `alembic.ini` est correctement configurée pour pointer vers votre base de données PostgreSQL (utilisez un driver synchrone pour Alembic, par exemple `postgresql://VOTRE_USER_PG:VOTRE_PASS_PG@localhost:5432/VOTRE_DB_NOM`).
    ```bash
    alembic upgrade head
    ```
    Cela appliquera toutes les migrations nécessaires pour amener votre base de données au dernier état défini par les scripts de migration dans `migrations/versions/`.

7.  **Exécuter le Script d'Indexation RAG Initial (Optionnel, pour peupler la base vectorielle)**:
    * Si vous avez des documents sources à indexer initialement dans ChromaDB (placés dans `Code_Source/backend/data/fiqh_docs/` par défaut), exécutez le script d'indexation :
    ```bash
    python indexer_rag.py
    ```
    * Cela chargera, découpera et vectorisera les documents pour le système RAG.

8.  **Lancer le Serveur FastAPI**:
    * Une fois tout configuré, vous pouvez lancer le serveur de développement FastAPI en utilisant Uvicorn (qui est listé dans `requirements.txt`).
    * Depuis la racine du dossier `Code_Source/backend/` :
    ```bash
    uvicorn src:app --reload --host 0.0.0.0 --port 8000
    ```
    * `--reload`: Uvicorn redémarrera automatiquement le serveur si des modifications de code sont détectées.
    * `--host 0.0.0.0`: Rend le serveur accessible depuis d'autres machines sur votre réseau (utile si le frontend tourne sur une autre machine ou dans un conteneur).
    * `--port 8000`: Le port sur lequel le serveur écoutera.

Votre backend devrait maintenant être accessible, typiquement à l'adresse `http://localhost:8000`. Vous pouvez vérifier son état en accédant à `http://localhost:8000/docs` dans votre navigateur pour voir la documentation OpenAPI (Swagger UI).

---

Après avoir configuré le backend, l'étape suivante est la [Configuration de l'Environnement Frontend](./frontend-setup.md).