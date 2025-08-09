# Documentation Technique : Assistant RAG Fiqh

## 1. Introduction
    1.1. Objectif de cette Documentation Technique
    1.2. Public Cible (Développeurs, Administrateurs Système, Mainteneurs Futurs)
    1.3. Aperçu du Système "Assistant RAG Fiqh" (Vue d'ensemble fonctionnelle et technique)
    1.4. Technologies Clés Utilisées (Liste des langages, frameworks, BDD, etc.)

## 2. Architecture Générale du Système
    2.1. Vue d'Ensemble des Composants et Diagramme d'Architecture
        2.1.1. Frontend (React + Vite)
        2.1.2. Backend (Python - FastAPI)
        2.1.3. Base de Données Relationnelle (PostgreSQL via SQLModel)
        2.1.4. Base de Données Vectorielle (ChromaDB)
        2.1.5. Modèle de Langage (Google Generative AI - Gemini)
        2.1.6. Serveur de Cache/Blocklist (Redis)
    2.2. Flux de Données Principaux (avec diagrammes si possible)
        2.2.1. Flux d'Authentification Utilisateur (Inscription, Vérification Email, Connexion, Reset MDP, Logout)
        2.2.2. Flux de Création et Gestion de Conversation
        2.2.3. Flux de Téléversement, Traitement et Indexation d'un Document
        2.2.4. Flux d'une Requête Utilisateur (Prompt) et Génération de Réponse RAG

## 3. Composant Backend (Python - FastAPI)
    3.1. Structure du Projet Backend (`Code_Source/backend/`)
    3.2. Point d'Entrée de l'Application (`src/__init__.py`)
        3.2.1. Initialisation de FastAPI et des Routeurs
        3.2.2. Gestion du Cycle de Vie (Lifespan) et Initialisation du RAG
    3.3. Configuration (`src/config.py`) (Variables d'environnement, UPLOAD_DIR)
    3.4. Middlewares (`src/middleware.py`) (CORS, TrustedHost, Logging)
    3.5. Gestion des Erreurs (`src/errors.py`) (Exceptions personnalisées et handlers)
    3.6. Modules API Principaux (Routes)
        3.6.1. Authentification (`src/auth/`)
            3.6.1.1. Routes (`routes.py`) : Endpoints pour signup, login, verify-email, password-reset, etc.
            3.6.1.2. Schémas Pydantic (`schemas.py`) : Modèles de données pour les requêtes/réponses.
            3.6.1.3. Services (`service.py`) : Logique métier (création utilisateur, vérification).
            3.6.1.4. Utilitaires (`utils.py`) : Génération de tokens, hachage de mots de passe, sérialiseurs.
            3.6.1.5. Dépendances (`dependencies.py`) : Sécurité (TokenBearer), vérification de rôles.
            3.6.1.6. Gestion des Emails (`src/mail.py`) : Configuration et envoi d'emails.
            3.6.1.7. Gestion de la Blocklist Redis (`src/db/redis.py`) : Invalidation des tokens JWT.
        3.6.2. Conversations et Messages (`src/conversations/`)
            3.6.2.1. Routes (`routes.py`) : Endpoints pour CRUD conversations, messages, documents.
            3.6.2.2. Schémas Pydantic (`schemas.py`) : Modèles de données pour conversations, messages, documents.
            3.6.2.3. Services (`service.py`) : Logique métier (gestion conversations, messages, documents, interaction RAG).
    3.7. Interaction avec la Base de Données Relationnelle (PostgreSQL)
        3.7.1. Connexion et Session (`src/db/main.py`)
        3.7.2. Modèles de Tables (SQLModel - `src/db/models.py`)
            3.7.2.1. User
            3.7.2.2. Conversation
            3.7.2.3. Message
            3.7.2.4. Document (métadonnées des fichiers)
        3.7.3. Migrations de Base de Données (Alembic - `alembic.ini`, dossier `migrations/`)
    3.8. Composants RAG (Logique de base dans `src/rag/` - *voir section 5 pour le détail du pipeline*)
        3.8.1. Orchestration de la Chaîne RAG (`src/rag/chain.py`)
        3.8.2. Chargement et Traitement des Documents (`src/rag/loader.py`)
        3.8.3. Gestion du Vector Store (`src/rag/vectorstore.py`)
        3.8.4. Utilitaires RAG Spécifiques (`src/rag/utils.py`)
    3.9. Dépendances Clés du Backend (`requirements.txt`)

## 4. Composant Frontend (React + Vite)
    4.1. Structure du Projet Frontend (`Code_Source/frontend/`)
        4.1.1. Description des Dossiers Clés (`src`, `src/components`, `src/pages`, `src/routers`, `src/utils`, `src/contexts`, `src/hooks`, `src/assets`)
    4.2. Configuration et Build (Vite)
        4.2.1. `vite.config.js` (Configuration du serveur de dev, proxy)
        4.2.2. `package.json` (Scripts `dev`, `build`, `lint`)
    4.3. Point d'Entrée (`src/main.jsx`) (Initialisation de React, Providers)
    4.4. Composant Principal (`src/App.jsx`) (Layout principal, gestion états globaux UI)
    4.5. Routage (React Router DOM)
        4.5.1. Définition des Routes (`src/routers/routes.jsx`)
        4.5.2. Loaders de Données (`src/routers/loaders/`)
        4.5.3. Actions de Formulaire (`src/routers/actions/`)
    4.6. Gestion de l'État
        4.6.1. `UserContext` (Gestion de l'utilisateur et du token)
        4.6.2. `SnackbarContext` (Notifications utilisateur)
        4.6.3. État local des composants (useState, useEffect dans `App.jsx` pour conversations, messages, etc.)
    4.7. Composants UI Principaux (Description et rôle)
        4.7.1. Authentification (`src/pages/Register.jsx`, `Login.jsx`, `ResetLink.jsx`, `ResetPassword.jsx`, `SendEmail.jsx`, `VerifyEmailHandler.jsx`)
        4.7.2. Interface de Chat (`TopAppBar.jsx`, `Sidebar.jsx`, `PromptField.jsx`, `Greetings.jsx`, gestion de l'affichage des messages dans `App.jsx`)
        4.7.3. Gestion des Documents et Contexte (`ContextHubPanel.jsx`, `DocumentUploadArea.jsx`, `DocumentItemCard.jsx`, `DocumentPreview.jsx`, `ContextSizeIndicator.jsx`, `DocumentFilters.jsx`)
        4.7.4. Composants Réutilisables (`src/components/Button.jsx`, `Logo.jsx`, `TextField.jsx`, `Avatar.jsx`, `Menu.jsx`, `Progress.jsx`, etc.)
    4.8. Communication avec le Backend (`src/utils/fetchWithAuth.js`) (Gestion des appels API authentifiés)
    4.9. Styling
        4.9.1. Tailwind CSS (`tailwind.config.js`, `postcss.config.js`)
        4.9.2. Styles Globaux et Spécifiques (`src/index.css`)
    4.10. Dépendances Clés du Frontend (`package.json`)

## 5. Base de Données Approfondie
    5.1. Schéma de la Base de Données Relationnelle (PostgreSQL)
        5.1.1. Description détaillée des tables et colonnes (basée sur `src/db/models.py`)
        5.1.2. Référence au fichier de backup SQL (`monstockage_backup_2025-04-20.sql`) comme exemple d'état.
    5.2. Rôle et Justification des Tables Principales (User, Conversation, Message, Document)
    5.3. Relations Importantes (Clés étrangères, cascades)
    5.4. Base de Données Vectorielle (ChromaDB)
        5.4.1. Structure de la collection (`COLLECTION_NAME` dans `src/rag/vectorstore.py`)
        5.4.2. Type de métadonnées stockées avec les vecteurs

## 6. Pipeline RAG Détaillé
    6.1. Phase d'Ingestion des Documents (Création et Mise à Jour du Contexte)
        6.1.1. Upload via l'API (`/conversations/{conversation_uid}/upload`)
        6.1.2. Sauvegarde physique des fichiers (`Config.UPLOAD_DIR` dans `src/config.py`)
        6.1.3. Traitement par `ConversationService.process_and_index_files`
            6.1.3.1. Création d'enregistrement `Document` en BDD (métadonnées)
            6.1.3.2. Préparation pour RAG (copie dans un dossier temporaire)
        6.1.4. Chargement par `rag.loader.charger_documents` (gestion des différents formats)
        6.1.5. Découpage par `rag.loader.split_documents` (RecursiveCharacterTextSplitter)
        6.1.6. Création des Embeddings et Stockage dans ChromaDB (`rag.vectorstore.add_documents_to_vectorstore`)
    6.2. Phase de Génération de Réponse
        6.2.1. Réception du prompt utilisateur (`/conversations/{conversation_uid}/messages`)
        6.2.2. Récupération de l'historique formaté de la conversation (`ConversationService.get_formatted_history`)
        6.2.3. Invocation de la `ConversationalRetrievalChain` (`rag.chain.get_rag_chain().ainvoke`)
            6.2.3.1. (Implicite) Condensation de la question avec l'historique (géré par la chaîne)
            6.2.3.2. Recherche de similarité dans ChromaDB via le Retriever (`vectorstore.as_retriever`)
            6.2.3.3. Récupération des documents sources pertinents
            6.2.3.4. Formulation du prompt final avec contexte et question (selon `template_arabe` dans `rag/chain.py`)
            6.2.3.5. Appel au LLM (Gemini via `ChatGoogleGenerativeAI`)
        6.2.4. Sauvegarde de la paire question/réponse dans la BDD (`ConversationService.save_message_pair`)
    6.3. Script d'Indexation Initiale (`indexer_rag.py`)
        6.3.1. Objectif et utilisation
        6.3.2. Source des documents (`SOURCE_DOCS_PATH`)

## 7. Installation et Configuration de l'Environnement de Développement
    7.1. Prérequis (Python 3.x, Node.js & npm/yarn, Git, Docker optionnel pour BDD/Redis)
    7.2. Configuration du Backend
        7.2.1. Clonage du dépôt
        7.2.2. Création et activation d'un environnement virtuel Python
        7.2.3. Installation des dépendances (`pip install -r requirements.txt`)
        7.2.4. Création et configuration du fichier `.env` (basé sur `src/config.py`, lister les variables essentielles : `DATABASE_URL`, `JWT_SECRET`, `MAIL_USERNAME`, `GEMINI_API_KEY`, `FRONTEND_URL`, `REDIS_HOST`, etc.)
        7.2.5. Initialisation de la base de données PostgreSQL
        7.2.6. Exécution des migrations Alembic (`alembic upgrade head`)
        7.2.7. Exécution du script d'indexation RAG initial (`python indexer_rag.py`)
        7.2.8. Lancement du serveur FastAPI (ex: `uvicorn src:app --reload --host 0.0.0.0 --port 8000`)
    7.3. Configuration du Frontend
        7.3.1. Navigation vers le dossier `Code_Source/frontend`
        7.3.2. Installation des dépendances (`npm install` ou `yarn install`)
        7.3.3. (Si nécessaire) Configuration de l'URL du backend (proxy Vite dans `vite.config.js` ou variable d'env)
        7.3.4. Lancement du serveur de développement (`npm run dev` ou `yarn start`)
    7.4. Services Externes (Instructions générales pour PostgreSQL et Redis si non-Dockerisés)

## 8. Déploiement (Considérations Générales)
    8.1. Backend (FastAPI) : Utilisation de Gunicorn + Uvicorn workers, gestion des variables d'environnement.
    8.2. Frontend (React/Vite) : Build de production (`npm run build`), servir les fichiers statiques.
    8.3. Base de Données (PostgreSQL) : Instance managée ou auto-hébergée.
    8.4. Base Vectorielle (ChromaDB) : Stratégies de persistance du dossier `chroma_db_fiqh`.
    8.5. Variables d'Environnement en Production.
    8.6. Considérations de sécurité (HTTPS, secrets, etc.).

## 9. Tests (`Code_Source/backend/src/tests/`)
    9.1. Configuration des Tests (Pytest, `conftest.py` pour les mocks et fixtures).
    9.2. Exemples de Tests Existants (adapter `test_auth.py`, `test_question.py` à la structure actuelle).
    9.3. Comment Lancer les Tests.

## 10. Documentation Utilisateur (Docusaurus - `Code_Source/user-docs/`)
    10.1. Aperçu de la Structure de la Documentation Utilisateur (référence à `user-docs/sidebars.js`).
    10.2. Points Clés de la Configuration de Docusaurus (`user-docs/docusaurus.config.js`).
    10.3. Comment builder et servir la documentation utilisateur.

## 11. Pistes d'Amélioration et Évolutions Futures
    (Section à remplir avec les idées d'évolutions du projet)

## 12. Conclusion
    (Bref résumé du document et du projet)

## 13. Annexe
    13.1. Glossaire des Termes Techniques Spécifiques au Projet
    13.2. Schéma Détaillé de la Base de Données (peut être une image générée ou un export)