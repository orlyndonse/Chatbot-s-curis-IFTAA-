---
sidebar_position: 2
title: Module Conversations (src/conversations/)
---

# Module Conversations (`src/conversations/`)

Le module `src/conversations/` est central pour la gestion des interactions de chat et des messages. Il permet aux utilisateurs de créer, lister, renommer et supprimer des conversations, d'y ajouter des messages (prompts), d'obtenir des réponses de l'IA enrichies par leurs documents personnels, avec un contrôle granulaire de l'activation des documents pour le contexte RAG.

## Structure du Module

* **`routes.py`**: Définit les endpoints de l'API FastAPI pour toutes les opérations liées aux conversations, messages et gestion des documents utilisateur.
* **`schemas.py`**: Contient les modèles Pydantic pour la validation des données des requêtes et la structuration des réponses concernant les conversations, les messages et les documents.
* **`service.py`**: Logique métier principale, incluant l'interaction avec la base de données (via SQLModel), l'orchestration des appels au pipeline RAG (`rag.chain`), et la gestion des documents utilisateur.

## Fonctionnalités Principales et Flux

### 1. `routes.py` - Endpoints de l'API Conversations

Ce fichier utilise `FastAPI.APIRouter` pour organiser les routes. Tous les endpoints ici sont protégés et nécessitent un utilisateur authentifié (via `get_current_user` et `RoleChecker`).

#### **Gestion des Conversations**

* **`/` (GET)**: `list_user_conversations`
    * Récupère et retourne la liste de toutes les conversations de l'utilisateur connecté, triées par date de création (la plus récente d'abord).
    * Utilise `ConversationService.get_user_conversations`.

* **`/` (POST)**: `create_new_conversation`
    * Crée une nouvelle conversation pour l'utilisateur.
    * Prend un `ConversationCreateModel` (titre optionnel).
    * Utilise `ConversationService.create_conversation`.
    * Si aucun titre n'est fourni, un titre par défaut basé sur la date et l'heure est généré.

* **`/{conversation_uid}` (DELETE)**: `delete_conversation`
    * Supprime une conversation spécifique et tous ses messages associés (via la cascade en base de données).
    * Vérifie l'appartenance de la conversation à l'utilisateur.
    * Utilise `ConversationService.delete_conversation`.
    * **Note** : Les documents de l'utilisateur restent disponibles pour ses autres conversations.

* **`/{conversation_uid}/rename` (PUT)**: `rename_conversation_title`
    * Permet de renommer le titre d'une conversation.
    * Prend un `ConversationRenameModel` (contenant le nouveau titre).
    * Utilise `ConversationService.rename_conversation`.

#### **Gestion des Messages et Interaction RAG**

* **`/{conversation_uid}/messages` (GET)**: `get_messages_for_conversation`
    * Récupère tous les messages (prompts et réponses) d'une conversation spécifique pour l'utilisateur connecté, triés par date de création.
    * Vérifie que l'utilisateur a accès à la conversation.

* **`/{conversation_uid}/messages` (POST)**: `add_message_to_conversation`
    * Ajoute un nouveau message (prompt utilisateur) à une conversation et obtient une réponse de l'IA.
    * Prend un `MessageCreateModel` (contenant le texte du prompt).
    * Vérifie l'appartenance de la conversation à l'utilisateur.
    * **Utilise tous les documents actifs de l'utilisateur** comme contexte RAG, pas seulement ceux d'une conversation spécifique.
    * Appelle `ConversationService.add_message_to_conversation` pour générer la réponse de l'IA et sauvegarder la paire prompt/réponse.

* **`/{conversation_uid}/messages/stream` (POST)**: `stream_message_to_conversation`
    * Version streaming de l'ajout de message, permettant de recevoir la réponse de l'IA en flux continu (Server-Sent Events).
    * Utilise `ConversationService.stream_rag_response_generator` pour le streaming.
    * **Contexte RAG global** : Utilise tous les documents actifs de l'utilisateur.

* **`/{conversation_uid}/messages/{message_uid}/edit` (PUT)**: `edit_message_in_conversation`
    * Permet à un utilisateur de modifier le prompt d'un de ses messages existants.
    * Prend un `MessageEditModel` (contenant le nouveau texte du prompt).
    * Supprime les messages suivants dans la conversation (ceux créés après le message édité).
    * Régénère une réponse de l'IA basée sur le prompt modifié et l'historique précédent.
    * **Utilise tous les documents actifs de l'utilisateur** pour la régénération.
    * Retourne la liste mise à jour des messages de la conversation.

* **`/{conversation_uid}/messages/{message_uid}/edit/stream` (PUT)**: `stream_edit_message_in_conversation`
    * Version streaming de l'édition de message, permettant de recevoir la nouvelle réponse en flux continu.
    * Utilise `ConversationService.stream_edit_response_generator`.

#### **Gestion des Documents Utilisateur (Globaux)**

Les endpoints de documents gèrent les documents **de l'utilisateur** (globaux) et non spécifiques à une conversation.

* **`/{conversation_uid}/documents` (GET)**: `get_conversation_documents`
    * Récupère **tous les documents de l'utilisateur**.
    * Ces documents sont disponibles comme contexte RAG dans **toutes** les conversations de l'utilisateur.
    * Vérifie l'appartenance de la conversation pour s'assurer que l'utilisateur est autorisé.

* **`/{conversation_uid}/documents/active` (GET)**: `get_active_documents`
    * Récupère uniquement les **documents actifs de l'utilisateur**.
    * Ces documents actifs sont utilisés comme contexte RAG dans **toutes** les conversations de l'utilisateur.
    * Retourne la liste des documents avec `is_active: true` et le nombre total.

* **`/{conversation_uid}/documents/{document_uid}/toggle-active` (PATCH)**: `toggle_document_active_status`
    * Active ou désactive un **document utilisateur** pour le contexte RAG.
    * **Impact global** : Ce changement affecte **toutes les conversations** de l'utilisateur.
    * Permet un contrôle granulaire des documents utilisés dans la génération de réponses.

* **`/{conversation_uid}/documents/{document_id}` (DELETE)**: `delete_document_from_conversation`
    * Supprime un **document utilisateur**.
    * **Impact global** : Le document ne sera plus disponible dans **aucune conversation** de l'utilisateur.
    * Utilise `ConversationService.delete_document_permanently`.

* **`/{conversation_uid}/documents/{document_id}/download` (GET)**: `download_document_content`
    * Permet de télécharger le contenu d'un **document utilisateur**.
    * Utilise `ConversationService.get_document_filepath` pour obtenir le chemin absolu du fichier.
    * Vérifie que le document appartient bien à l'utilisateur connecté.

### 2. `schemas.py` - Modèles de Données Pydantic

* `MessageBase`, `MessageModel`, `MessageCreateModel`: Pour les messages.
* `MessageEditModel`: Pour l'édition d'un message existant.
* `ConversationBase`, `ConversationCreateModel`, `ConversationModel`: Pour les conversations.
* `ConversationRenameModel`: Pour renommer une conversation.
* `DocumentModel`: Représente les métadonnées d'un **document utilisateur** :
    * `uid`: Identifiant unique du document
    * `filename`: Nom du fichier
    * `user_uid`: UID de l'utilisateur propriétaire
    * `upload_date`: Date de téléversement
    * `size`: Taille du fichier en octets
    * `mime_type`: Type MIME du fichier
    * `is_active`: Statut d'activation pour le contexte RAG global de l'utilisateur
* `ConversationDetailModel`: Modèle étendu pour une conversation, incluant ses messages.
* `UserConversationsModel`: Modèle pour représenter un utilisateur avec toutes ses conversations.

### 3. `service.py` - Logique Métier (`ConversationService`)

#### **Gestion des Conversations**
* `get_conversation_by_uid`, `get_user_conversation`, `get_user_conversations`: Récupération de conversations.
* `create_conversation`: Crée une nouvelle conversation.
* `delete_conversation`: Supprime une conversation (les documents utilisateur restent intacts).
* `rename_conversation`: Renomme une conversation.

#### **Gestion des Messages et Interaction RAG Globale**
* `get_formatted_history`: Prépare l'historique des messages d'une conversation.
* `get_active_user_document_uids`: Récupère les UIDs de **tous les documents actifs de l'utilisateur**.
* `generate_rag_response`: Utilise **tous les documents actifs de l'utilisateur** comme contexte, quelle que soit la conversation.
* `save_message_pair`: Sauvegarde un prompt utilisateur et la réponse IA correspondante.
* `add_message_to_conversation`: Logique complète pour ajouter un message avec contexte RAG global.
* `stream_rag_response_generator`: Streaming avec contexte RAG global.
* `stream_edit_response_generator`: Streaming d'édition avec contexte RAG global.

#### **Gestion des Documents Utilisateur (Globaux)**
* `get_user_documents`: Récupère tous les documents d'un utilisateur.
* `get_active_user_documents`: Récupère uniquement les documents actifs d'un utilisateur.
* `toggle_user_document_active_status`: Active/désactive un document utilisateur (impact sur toutes ses conversations).
* `delete_user_document_permanently`: Supprime un document utilisateur (impact global).
* `get_user_document_filepath`: Vérifie l'appartenance du document à l'utilisateur.

## Architecture de Gestion des Documents

### Architecture Centralisée

L'architecture centralise la gestion des documents au niveau **utilisateur** :

* **Documents globaux par utilisateur** :
    - Chaque utilisateur possède une bibliothèque personnelle de documents
    - Les documents sont partagés automatiquement entre **toutes** les conversations de l'utilisateur
    - Un seul contrôle d'activation par document affecte toutes les conversations

* **Module Administration (`src/admin/`)** :
    - **Téléversement exclusif** des documents par les administrateurs
    - **Attribution globale** des documents à des utilisateurs spécifiques
    - Les documents deviennent immédiatement disponibles dans toutes les conversations de l'utilisateur cible

### Flux de Gestion Documentaire Globale

1. **Téléversement administrateur** : Les administrateurs téléversent des documents et les associent à un utilisateur spécifique.

2. **Disponibilité globale** : Les documents deviennent automatiquement disponibles dans **toutes** les conversations de l'utilisateur.

3. **Contrôle utilisateur global** : 
   - L'activation/désactivation d'un document affecte **toutes** les conversations
   - La suppression d'un document le retire de **toutes** les conversations
   - Le téléchargement reste possible depuis n'importe quelle conversation

4. **Contexte RAG unifié** : Tous les documents actifs de l'utilisateur constituent le contexte RAG, indépendamment de la conversation courante.

## Flux de Fonctionnement RAG Global

Lorsqu'un utilisateur envoie un message dans **n'importe quelle** conversation :

1. **Vérification des permissions** : Contrôle de l'accès à la conversation
2. **Récupération de l'historique** : Formatage des messages de la conversation courante
3. **Contexte documentaire global** : Récupération de **tous** les documents actifs de l'utilisateur (`is_active=true`)
4. **Génération de la réponse** : Appel au pipeline RAG avec le contexte global de l'utilisateur
5. **Sauvegarde** : Enregistrement de la paire question-réponse dans la conversation courante

### Avantages de cette Architecture

- **Cohérence inter-conversations** : L'utilisateur bénéficie du même contexte documentaire dans toutes ses conversations
- **Simplicité de gestion** : Un seul endroit pour contrôler l'activation des documents
- **Efficacité** : Pas de duplication de documents entre conversations
- **Flexibilité** : L'utilisateur peut créer des conversations thématiques tout en gardant accès à sa bibliothèque complète

Ce module est donc au cœur de l'application, gérant les interactions conversationnelles tout en s'appuyant sur une bibliothèque documentaire globale par utilisateur pour enrichir les réponses IA.

---

Ensuite, nous détaillerons l'interaction avec la [Base de Données Relationnelle (PostgreSQL)](../database-interaction/connection-session.md)