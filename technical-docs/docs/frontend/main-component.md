---
sidebar_position: 4
title: Composant Principal (src/App.jsx)
---

# Composant Principal de l'Application (`src/App.jsx`)

Le fichier `src/App.jsx` définit le composant React racine qui structure l'interface utilisateur principale de l'application Assistant RAG Fiqh une fois que l'utilisateur est authentifié et que les données initiales sont chargées. Il est rendu via le `RouterProvider` configuré dans `src/main.jsx`.

## Rôle et Structure

`App.jsx` est responsable de :
* L'agencement général de l'interface après connexion (barre de navigation, barre latérale, zone de chat, panneau de contexte).
* La gestion d'une partie importante de l'état de l'application lié aux conversations et aux messages.
* L'orchestration des interactions utilisateur avec le backend pour les fonctionnalités de chat.
* L'affichage dynamique du contenu en fonction de l'état de la conversation active.

## Initialisation et Données Chargées

* **`useLoaderData()`**: Le composant utilise le hook `useLoaderData` de React Router DOM pour accéder aux données préchargées par la fonction `appLoader` (définie dans `src/routers/loaders/appLoader.js`).
    * Ces données initiales (`initialData`) incluent typiquement les informations de l'utilisateur connecté et sa liste de conversations existantes.

## Gestion de l'État (Principaux États)

Le composant `App` gère plusieurs états cruciaux à l'aide de `useState`:

* **`conversations`**: Stocke la liste des conversations de l'utilisateur. Initialisée avec `initialData.conversations`.
* **`activeConversationUid`**: L'UID de la conversation actuellement sélectionnée et affichée.
* **`messages`**: Un tableau contenant les messages (prompts et réponses) de la conversation active.
* **`isSidebarOpen`**: Contrôle la visibilité de la barre latérale gauche (liste des conversations).
* **`isContextHubOpen`**: Contrôle la visibilité du panneau latéral droit "Context Hub" (gestion des documents).
* **`isLoadingResponse`**: Booléen indiquant si une réponse de l'IA est en cours de chargement.
* **`currentPrompt`**: Stocke le texte du prompt actuellement saisi par l'utilisateur.
* **`documentToPreview`**: Stocke les informations du document sélectionné pour l'aperçu.
* **`isUploading`**: Booléen indiquant si un téléversement de document est en cours.
* **`uploadedFilesInfo`**: Stocke les informations sur les fichiers téléversés pour la conversation active.
* **`error`**: Stocke les messages d'erreur à afficher.

## Effets (`useEffect`) Principaux

* **Chargement des messages lors du changement de conversation active**:
    * Un `useEffect` est déclenché lorsque `activeConversationUid` change.
    * Si un `activeConversationUid` est défini, il effectue un appel API (via `fetchWithAuth`) à `/api/v1/conversations/{activeConversationUid}/messages` pour récupérer les messages de cette conversation.
    * Met à jour l'état `messages` avec les données récupérées.
* **Chargement des documents lors du changement de conversation active**:
    * Un `useEffect` similaire est déclenché par `activeConversationUid` pour récupérer les documents associés à la conversation via `/api/v1/conversations/{activeConversationUid}/documents`.
    * Met à jour l'état `uploadedFilesInfo`.

## Fonctions de Gestion Principales

Le composant définit de nombreuses fonctions pour gérer les interactions utilisateur et les appels API :

* **`handleSelectConversation(uid)`**: Met à jour `activeConversationUid` lorsqu'une conversation est sélectionnée dans la barre latérale.
* **`handleCreateNewConversation()`**: Appelle l'API pour créer une nouvelle conversation, met à jour la liste `conversations`, et sélectionne la nouvelle conversation.
* **`handleDeleteConversation(uid)`**: Appelle l'API pour supprimer une conversation, met à jour la liste et gère la sélection de la conversation active.
* **`handleRenameConversation(uid, newTitle)`**: Appelle l'API pour renommer une conversation.
* **`handlePromptSubmit()`**: Gère la soumission d'un prompt :
    * Envoie le `currentPrompt` à l'API (`/api/v1/conversations/{activeConversationUid}/messages`).
    * Met à jour l'état `messages` avec le prompt de l'utilisateur et (après réception) la réponse de l'IA.
    * Gère l'état `isLoadingResponse`.
* **`handleEditMessage(messageUid, newPromptText)`**: Gère l'édition d'un message existant.
* **`handleFileUpload(files)`**: Gère le téléversement de fichiers vers le backend pour la conversation active.
* **`handleDeleteDocument(documentId)`**: Gère la suppression d'un document associé à la conversation.
* **`handlePreviewDocument(document)`**: Met à jour `documentToPreview` pour afficher un aperçu du document.
* **`toggleSidebar()`, `toggleContextHub()`**: Fonctions pour ouvrir/fermer les panneaux latéraux.

## Structure du Rendu JSX

Le JSX retourné par `App.jsx` définit la mise en page principale :

* Un conteneur `div` principal avec une disposition flex.
* **`Sidebar`**: Affiche la liste des conversations et permet la création/sélection/suppression. Sa visibilité est contrôlée par `isSidebarOpen`.
* **Zone de contenu principal**:
    * **`TopAppBar`**: Affiche le titre de la conversation active et les contrôles pour les panneaux latéraux et le menu utilisateur.
    * **Zone d'affichage des messages**:
        * Affiche `Greetings.jsx` si aucune conversation n'est active.
        * Sinon, affiche les messages de la conversation active, mappés à partir de l'état `messages`. Chaque message (prompt et réponse) est stylisé.
        * Affiche un indicateur de chargement (`Progress.Spinner`) si `isLoadingResponse` est vrai.
    * **`PromptField`**: Champ de saisie pour que l'utilisateur tape son prompt.
* **`ContextHubPanel`**: Panneau latéral droit pour la gestion des documents (téléversement, liste, filtres). Sa visibilité est contrôlée par `isContextHubOpen`.
* **`DocumentPreview`**: Modale ou panneau pour afficher un aperçu du document sélectionné.
* **`Snackbar`**: Pour afficher les notifications gérées par `SnackbarContext`.

`App.jsx` est donc un composant central et complexe qui agit comme le chef d'orchestre de l'expérience utilisateur principale après l'authentification.

---

La manière dont l'utilisateur navigue entre les différentes vues et comment les données sont chargées pour ces vues est gérée par le [Système de Routage (React Router DOM)](./routing.md).