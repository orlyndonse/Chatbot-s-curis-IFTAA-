---
sidebar_position: 2
title: Module Conversations (src/conversations/)
---

# Module Conversations (`src/conversations/`)

Le module `src/conversations/` est central pour la gestion des interactions de chat, des messages et des documents qui fournissent le contexte au système RAG. Il permet aux utilisateurs de créer, lister, renommer et supprimer des conversations, d'y ajouter des messages (prompts), d'obtenir des réponses de l'IA, et de gérer les fichiers associés avec un contrôle granulaire de leur activation pour le contexte RAG.

## Structure du Module

* **`routes.py`**: Définit les endpoints de l'API FastAPI pour toutes les opérations liées aux conversations, messages et documents.
* **`schemas.py`**: Contient les modèles Pydantic pour la validation des données des requêtes et la structuration des réponses concernant les conversations, les messages et les documents.
* **`service.py`**: Logique métier principale, incluant l'interaction avec la base de données (via SQLModel), l'orchestration des appels au pipeline RAG (`rag.chain`), et la gestion des fichiers.

## Fonctionnalités Principales et Flux

### 1. `routes.py` - Endpoints de l'API Conversations

Ce fichier utilise `FastAPI.APIRouter` pour organiser les routes. Tous les endpoints ici sont protégés et nécessitent un utilisateur authentifié (via `get_current_user` et `RoleChecker`).

* **`/` (GET)**: `list_user_conversations`
    * Récupère et retourne la liste de toutes les conversations de l'utilisateur connecté, triées par date de création (la plus récente d'abord).
    * Utilise `ConversationService.get_user_conversations`.

* **`/` (POST)**: `create_new_conversation`
    * Crée une nouvelle conversation pour l'utilisateur.
    * Prend un `ConversationCreateModel` (titre optionnel, premier prompt optionnel).
    * Utilise `ConversationService.create_conversation`.
    * Si aucun titre n'est fourni, un titre par défaut basé sur la date et l'heure est généré.

* **`/{conversation_uid}/messages` (GET)**: `get_messages_for_conversation`
    * Récupère tous les messages (prompts et réponses) d'une conversation spécifique pour l'utilisateur connecté, triés par date de création.
    * Vérifie que l'utilisateur a accès à la conversation.

* **`/{conversation_uid}/messages` (POST)**: `add_message_to_conversation`
    * Ajoute un nouveau message (prompt utilisateur) à une conversation et obtient une rÉponse de l'IA.
    * Prend un `MessageCreateModel` (contenant le texte du prompt).
    * Vérifie l'appartenance de la conversation à l'utilisateur.
    * Appelle `ConversationService.generate_rag_response` pour obtenir la réponse de l'IA.
    * Sauvegarde la paire prompt/réponse via `ConversationService.save_message_pair`.

* **`/{conversation_uid}` (DELETE)**: `delete_conversation`
    * Supprime une conversation spécifique et tous ses messages et documents associés (via la cascade en base de données).
    * Vérifie l'appartenance de la conversation à l'utilisateur.
    * Utilise `ConversationService.delete_conversation`.

* **`/{conversation_uid}/messages/{message_uid}/edit` (PUT)**: `edit_message_in_conversation`
    * Permet à un utilisateur de modifier le prompt d'un de ses messages existants.
    * Prend un `MessageEditModel` (contenant le nouveau texte du prompt).
    * Supprime les messages suivants dans la conversation (ceux créés après le message édité).
    * Régénère une réponse de l'IA basée sur le prompt modifié et l'historique précédent.
    * Met à jour le message original avec le nouveau prompt et la nouvelle réponse.
    * Retourne la liste mise à jour des messages de la conversation.

* **`/{conversation_uid}/rename` (PUT)**: `rename_conversation_title`
    * Permet de renommer le titre d'une conversation.
    * Prend un `ConversationRenameModel` (contenant le nouveau titre).
    * Utilise `ConversationService.rename_conversation`.

* **`/{conversation_uid}/upload` (POST)**: `upload_files_to_conversation`
    * Permet de téléverser un ou plusieurs fichiers dans le contexte d'une conversation.
    * Vérifie l'appartenance de la conversation.
    * Utilise `ConversationService.process_and_index_files` pour sauvegarder les fichiers, enregistrer leurs métadonnées en base de données, et les indexer dans la base vectorielle pour le RAG.
    * Les documents sont activés par défaut pour le contexte RAG.
    * Retourne un résumé du traitement, incluant les documents traités avec succès et les erreurs éventuelles.

* **`/{conversation_uid}/documents` (GET)**: `get_conversation_documents`
    * Récupère la liste des métadonnées de tous les documents associés à une conversation.
    * Vérifie l'accès de l'utilisateur à la conversation.

* **`/{conversation_uid}/documents/active` (GET)**: `get_active_documents`
    * **NOUVEAU** : Récupère uniquement les documents actifs utilisés pour le RAG.
    * Vérifie l'appartenance de la conversation à l'utilisateur.
    * Retourne la liste des documents avec `is_active: true` et le nombre total.

* **`/{conversation_uid}/documents/{document_id}` (DELETE)**: `delete_document_from_conversation`
    * Supprime un document spécifique (son enregistrement en base de données) du contexte d'une conversation.
    * Le fichier physique sur le serveur et les références dans le vector store ne sont pas supprimés (TODO dans l'implémentation).

* **`/{conversation_uid}/documents/{document_uid}/toggle-active` (PATCH)**: `toggle_document_active_status`
    * **NOUVEAU** : Permet d'activer ou désactiver un document pour le contexte RAG.
    * Prend un paramètre booléen `is_active`.
    * Permet un contrôle granulaire des documents utilisés dans la génération de réponses.
    * Vérifie les permissions d'accès à la conversation.

* **`/{conversation_uid}/documents/{document_id}/download` (GET)**: `download_document_content`
    * Permet de télécharger le contenu d'un fichier spécifique associé à une conversation.
    * Utilise `ConversationService.get_document_filepath` pour obtenir le chemin absolu du fichier sur le serveur après vérification des droits.
    * Renvoie une `FileResponse`.

### 2. `schemas.py` - Modèles de Données Pydantic pour les Conversations

Ce fichier définit les structures de données (Pydantic models) utilisées pour la validation et la sérialisation des données liées aux conversations, messages et documents.

* `MessageBase`, `MessageModel`, `MessageCreateModel`: Pour les messages.
* `MessageEditModel`: Pour l'édition d'un message existant.
* `ConversationBase`, `ConversationCreateModel`, `ConversationModel`: Pour les conversations.
    * `ConversationCreateModel` permet de spécifier un titre optionnel et un premier prompt lors de la création.
* `ConversationRenameModel`: Pour renommer une conversation (nouveau titre).
* `DocumentModel`: Représente les métadonnées d'un document téléversé avec **contrôle d'activation RAG** :
    * `uid`: Identifiant unique du document
    * `filename`: Nom du fichier (max 255 caractères)
    * `conversation_uid`: UID de la conversation associée
    * `upload_date`: Date de téléversement
    * `size`: Taille du fichier en octets
    * `mime_type`: Type MIME du fichier (max 100 caractères)
    * `is_active`: **NOUVEAU** - Statut d'activation pour le contexte RAG (défaut: `true`)
* `ConversationDetailModel`: Modèle étendu pour une conversation, incluant la liste de ses messages (`MessageModel`) et de ses documents (`DocumentModel`).
* `UserConversationsModel`: Modèle pour représenter un utilisateur avec toutes ses conversations.
* `DocumentUploadResponse`: Structure la réponse après un téléversement de documents.
* `DocumentDeleteResponse`: Pour la réponse après la suppression d'un document.

Tous les modèles destinés à être créés à partir d'objets ORM (comme `ConversationModel`, `DocumentModel`, `ConversationDetailModel`, `UserConversationsModel`) incluent `model_config = ConfigDict(from_attributes=True)`.

### 3. `service.py` - Logique Métier des Conversations (`ConversationService`)

La classe `ConversationService` contient la logique métier principale pour la gestion des conversations, des messages, des documents et l'interaction avec le système RAG avec **contrôle de sécurité renforcé**.

#### **Gestion des Conversations**
* `get_conversation_by_uid`, `get_user_conversation`, `get_user_conversations`: Récupération de conversations.
* `create_conversation`: Crée une nouvelle conversation.
* `delete_conversation`: Supprime une conversation.
* `rename_conversation`: Renomme une conversation.

#### **Gestion des Messages et Interaction RAG Sécurisée**
* `get_formatted_history`: Prépare l'historique des messages d'une conversation dans un format attendu par la chaîne RAG (liste de tuples `(prompt, response)`).
* `get_active_document_uids`: **CRITIQUE pour la sécurité** - Récupère uniquement les UIDs des documents actifs pour une conversation donnée.
* `generate_rag_response`: Fonction clé qui interagit avec la `ConversationalRetrievalChain` de `rag.chain.py` pour obtenir une réponse de l'IA. Elle utilise **exclusivement** les documents actifs de la conversation pour garantir la sécurité et la pertinence du contexte.
* `save_message_pair`: Sauvegarde un prompt utilisateur et la réponse IA correspondante en base de données.
* `add_message_to_conversation`: Logique complète pour ajouter un message utilisateur, générer une réponse RAG, et sauvegarder la paire. (Note: les routes utilisent directement `generate_rag_response` et `save_message_pair` plutôt que cette méthode).
* `get_conversation_messages`, `get_message_by_uid`: Récupération de messages.
* `edit_message_and_regenerate`: Gère l'édition d'un prompt, la suppression des messages suivants, la régénération d'une réponse IA, et la mise à jour du message.

#### **Gestion Avancée des Documents avec Contrôle RAG**
* `get_documents_for_conversation`: Récupère les métadonnées des documents d'une conversation.
* `process_and_index_files`: Gère le téléversement de fichiers :
    * Sauvegarde physique des fichiers dans un répertoire spécifique à la conversation sous `Config.UPLOAD_DIR`.
    * Enregistre les métadonnées dans la table `Document` de la base de données SQL avec `is_active=True` par défaut.
    * Charge, découpe (`charger_documents`, `split_documents` de `src.rag.loader`), et indexe les documents dans la base vectorielle ChromaDB (`add_documents_to_vectorstore` de `src.rag.vectorstore`).
    * Enrichit les métadonnées des chunks avec `document_uid`, `conversation_uid`, et `source`.
* `get_document_filepath`: Récupère le chemin absolu d'un fichier sur le serveur, en vérifiant les droits d'accès de l'utilisateur à la conversation et en appliquant des contrôles de sécurité contre le path traversal.
* `toggle_document_active_status`: **NOUVEAU** - Active ou désactive un document pour le contexte RAG. Permet un contrôle granulaire des documents utilisés dans les réponses.
* `remove_document_from_context`: Supprime l'enregistrement d'un document de la base de données SQL. **Note importante** : La suppression du vector store et du fichier physique n'est pas implémentée (marquée TODO dans le code).

#### **Sécurité et Contrôle d'Accès**
Le service implémente plusieurs couches de sécurité :
- Vérification systématique de l'appartenance des conversations aux utilisateurs
- Utilisation exclusive des documents actifs dans le contexte RAG
- Validation des chemins de fichiers contre les attaques de path traversal
- Isolation des données par conversation et par utilisateur

## Flux de Fonctionnement RAG Sécurisé

Lorsqu'un utilisateur envoie un message :

1. **Vérification des permissions** : Contrôle de l'accès à la conversation
2. **Récupération de l'historique** : Formatage des messages précédents
3. **Sélection des documents actifs** : Seuls les documents avec `is_active=true` sont utilisés
4. **Génération de la réponse** : Appel au pipeline RAG avec le contexte sécurisé
5. **Sauvegarde** : Enregistrement de la paire question-réponse

Ce module est donc au cœur de l'application, reliant l'interface utilisateur, la base de données, et le système d'intelligence artificielle avec des mécanismes de sécurité robustes et un contrôle granulaire du contexte documentaire.

---

Ensuite, nous détaillerons l'interaction avec la [Base de Données Relationnelle (PostgreSQL)](../database-interaction/connection-session.md).