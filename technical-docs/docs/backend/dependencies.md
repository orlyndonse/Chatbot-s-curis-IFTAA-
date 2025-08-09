---
sidebar_position: 9 # Ajustez si nécessaire en fonction de l'ordre final dans la catégorie backend
title: Dépendances Clés du Backend
---

# Dépendances Clés du Backend (`requirements.txt`)

Le fichier `requirements.txt` à la racine du projet backend (`Code_Source/backend/`) liste toutes les bibliothèques Python nécessaires au fonctionnement de l'application. Voici une description des dépendances les plus importantes et de leur rôle dans le projet :

## Framework et Utilitaires Web

* **`fastapi`**: Framework web moderne et performant pour construire des APIs avec Python, basé sur les standards OpenAPI et JSON Schema.
* **`uvicorn`**: Serveur ASGI (Asynchronous Server Gateway Interface) pour exécuter des applications FastAPI.
* **`pydantic`** et **`pydantic-settings`**: Utilisés pour la validation des données (schémas de requête/réponse) et la gestion de la configuration.
* **`python-multipart`**: Nécessaire pour FastAPI pour gérer les formulaires encodés en `multipart/form-data` (utilisé pour le téléversement de fichiers). (Bien que non listé explicitement, c'est une dépendance courante pour l'upload de fichiers avec FastAPI et pourrait être implicitement requis ou ajouté si l'upload est direct via FastAPI et non via un service externe).

## Authentification et Sécurité

* **`passlib[bcrypt]`**: Bibliothèque pour le hachage sécurisé des mots de passe, avec le support de l'algorithme bcrypt.
* **`python-jose[cryptography]`**: Pour l'encodage, le décodage et la signature des tokens JWT (JSON Web Tokens).
* **`itsdangerous`**: Utilisé pour générer des tokens sécurisés et signés basés sur le temps (par exemple, pour les liens de vérification d'email et de réinitialisation de mot de passe).

## Base de Données et ORM

* **`sqlmodel`**: Bibliothèque qui combine Pydantic et SQLAlchemy pour une interaction ORM moderne et typée avec la base de données.
* **`sqlalchemy`**: Toolkit SQL et ORM (Object Relational Mapper) sous-jacent utilisé par SQLModel.
* **`asyncpg`**: Driver PostgreSQL asynchrone pour SQLAlchemy, permettant des opérations de base de données non bloquantes.
* **`alembic`**: Outil de migration de schéma de base de données pour SQLAlchemy. (Bien que non listé dans `requirements.txt`, il est utilisé via `alembic.ini` et est essentiel si des migrations sont gérées).
* **`redis`** (et `aioredis` via `redis[asyncio]` implicitement si la version de `redis` le supporte, ou directement `aioredis`): Client Python asynchrone pour interagir avec le serveur Redis (utilisé pour la blocklist des tokens).

## Logique RAG (Retrieval Augmented Generation)

* **`langchain`**: Framework principal pour construire des applications basées sur les LLMs, fournissant les chaînes, les composants et les abstractions nécessaires.
* **`langchain-community`**: Contient des intégrations communautaires pour Langchain, y compris certains chargeurs de documents et wrappers.
* **`langchain-google-genai`**: Intégration spécifique pour utiliser les modèles de Google Generative AI (comme Gemini) avec Langchain.
* **`google-generativeai`**: Bibliothèque client Python officielle pour interagir avec l'API Google Generative AI.
* **`chromadb`**: Client pour la base de données vectorielle ChromaDB, utilisée pour stocker et rechercher les embeddings de documents.
* **`sentence-transformers`**: Bibliothèque pour générer des embeddings de phrases/textes (utilisée via `HuggingFaceEmbeddings` de Langchain).
* **`PyPDF2`** ou **`pypdf`**: (Présent comme `pypdf` dans `requirements.txt`) Utilisé par `PyPDFLoader` de Langchain pour lire le contenu des fichiers PDF.
* **`unstructured`**: (Présent dans `requirements.txt`) Utilisé par `UnstructuredHTMLLoader` et potentiellement d'autres chargeurs pour extraire le contenu de divers formats de fichiers.
* **`python-magic`**: (Présent dans `requirements.txt`) Utilisé pour détecter les types MIME des fichiers, ce qui peut aider au choix du bon chargeur de document.
* **`camel_tools`**: Utilisé pour la normalisation avancée du texte arabe.
* **`arabic_reshaper`**: Pour la mise en forme correcte des caractères arabes (liaison des lettres).
* **`python-bidi`**: Implémente l'algorithme bidirectionnel Unicode pour un affichage correct du texte mixte (comme l'arabe avec des chiffres).

## Envoi d'Emails

* **`fastapi-mail`**: Extension FastAPI pour faciliter l'envoi d'emails (utilisée dans `src/mail.py`). (Note: votre `requirements.txt` ne le liste pas explicitement mais votre code `src/mail.py` l'utilise). Si elle n'est pas dans `requirements.txt`, elle devrait y être ajoutée.

## Autres Utilitaires

* **`aiofiles`**: Pour les opérations asynchrones sur les fichiers (utilisé dans `ConversationService` pour sauvegarder les fichiers téléversés).
* **`python-dotenv`**: Pour charger les variables d'environnement à partir d'un fichier `.env` lors du développement.

Cette liste n'est pas exhaustive mais couvre les dépendances les plus critiques qui définissent l'architecture et les capacités du backend. Il est important de maintenir ce fichier `requirements.txt` à jour et d'utiliser des environnements virtuels pour gérer ces dépendances.

---

Nous avons couvert la majorité des aspects du backend. La prochaine section de la documentation technique se concentrera sur le [Composant Frontend (React)](../../frontend/structure.md).