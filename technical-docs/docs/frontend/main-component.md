---
sidebar_position: 4
title: Composant Principal (src/App.jsx)
---

# Composant Principal (`src/App.jsx`)

`src/App.jsx` est le composant racine qui structure l'interface principale de l'application une fois l'utilisateur authentifié. Il agit comme un chef d'orchestre pour la logique de chat, la gestion des conversations, des documents, et coordonne l'ensemble des composants de l'interface utilisateur.

## Données Initiales

* **`useLoaderData()`**: Le composant utilise ce hook pour accéder aux données préchargées par `appLoader`:
    * `user`: Les informations de l'utilisateur connecté.
    * `conversations`: La liste de toutes les conversations de l'utilisateur.
    * `initialMessages`: Les messages de la conversation la plus récente (sauf si l'on vient de se connecter).

## Gestion de l'État

`App.jsx` utilise `useState` et `useCallback` pour gérer de nombreux états et fonctions :

### **Conversations et Messages**
* `allConversations`: La liste complète des conversations, mise à jour après création, suppression ou renommage.
* `activeConversation`: L'objet de la conversation actuellement sélectionnée.
* `currentMessages`: Le tableau des messages (prompts et réponses) pour la conversation active.
* `isSendingMessage`: Booléen pour l'état de chargement lors de l'envoi d'un message.
* `editingMessageId` et `editText`: Gèrent l'état d'édition d'un message existant.
* `isEditingMessage`: Booléen indiquant si une édition de message est en cours.

### **Interface Utilisateur et Navigation**
* `isSidebarOpen` et `isContextHubOpen`: Contrôlent la visibilité des panneaux latéraux (Sidebar et ContextHub).
* `isCreatingConversation`: Booléen pour l'état de chargement lors de la création d'une nouvelle conversation.
* `renamingConvId` et `renameInputText`: Gèrent l'état de renommage d'une conversation dans la Sidebar.
* `isSavingRename`: Booléen pour l'état de chargement du renommage.
* `isDeletingConversation`: Stocke l'UID de la conversation en cours de suppression.

### **Gestion des Documents et Aperçus**
* `documentsInContext`: Tableau des documents associés à la conversation active.
* `currentContextSize` et `maxContextSize`: Gèrent la taille du contexte utilisé.
* `isUploading`: Booléen pour l'état de chargement lors du téléversement de fichiers via PromptField ou ContextHub.
* `deletingDocumentId`: Stocke l'UID du document en cours de suppression.
* `isPreviewModalOpen` et `documentToPreview`: Gèrent l'affichage de la modale DocumentPreview.
* `isPreviewLoading`: État de chargement pour l'aperçu de document dans DocumentPreview.

### **Streaming et Communication**
* États pour gérer le streaming en temps réel des réponses IA.
* Gestion des connexions Server-Sent Events (SSE).
* Accumulation progressive du contenu streamé.

## Fonctions de Gestion Principales

### **Coordination des Composants d'Interface**
* **`toggleSidebar()` / `toggleContextHub()`**: Contrôlent l'affichage des panneaux latéraux et gèrent la responsivité.
* **`handleNewConversationRequest()`**: Coordonne la création d'une nouvelle conversation entre App, Sidebar et PromptField.
* **`fetchConversationData(uid)`**: Fonction `useCallback` qui récupère les messages et documents pour une conversation sélectionnée via Sidebar.

### **Gestion des Messages avec PromptField**
* **`handleSendMessage(prompt)`**: Traite les soumissions du PromptField avec streaming en temps réel :
  - Création optimiste d'une nouvelle conversation si nécessaire
  - Affichage immédiat du message utilisateur
  - Streaming Server-Sent Events (SSE) pour la réponse de l'IA
  - Mise à jour en temps réel de l'interface utilisateur

* **`handleSaveEdit(uid, newPrompt)`**: Gère l'édition d'un message existant depuis l'interface de chat :
  - Mise à jour optimiste de l'interface
  - Streaming de la nouvelle réponse générée
  - Gestion des erreurs et restauration en cas d'échec

### **Gestion des Conversations via Sidebar**
* **`handleDeleteConversation(uid)`**: Traite les suppressions initiées depuis la Sidebar.
* **`handleStartRename(uid, title)` / `handleSaveRename(uid, newTitle)`**: Gèrent le processus de renommage inline dans la Sidebar.

### **Gestion des Documents et DocumentPreview**
* **`handleFileUploadForPromptField(files)`**: Traite les téléversements depuis le PromptField.
* **`handleFileSubmitForContextHub(files)`**: Gère le téléversement multiple de fichiers via le ContextHub.
* **`handleDeleteDocumentFromContext(docUid)`**: Gère la suppression d'un document depuis le ContextHub.
* **`handleToggleDocumentActiveState(docUid)`**: Active ou désactive un document depuis le ContextHub ou DocumentPreview.
* **`handlePreviewDocument(doc)`**: Ouvre la modale DocumentPreview avec support multi-format (PDF, texte, images).

### **Fonctions Utilitaires**
* **`handleCancelEdit()` / `handleCancelRename()`**: Fonctions de nettoyage pour annuler les opérations en cours dans l'interface.

## Architecture des Composants Principaux

### **Sidebar** 
Panneau latéral gauche gérant :
- Navigation entre conversations avec Avatar et Logo
- Fonctionnalités de renommage et suppression inline
- ExtendedFab pour créer de nouvelles conversations
- Gestion responsive avec overlay sur mobile

### **PromptField**
Zone de saisie principale incluant :
- Champ de texte multiline avec auto-resize
- UploadButton intégré pour le téléversement de fichiers
- IconBtn d'envoi avec états de chargement
- Support des raccourcis clavier (Enter pour envoyer, Shift+Enter pour nouvelle ligne)

### **ContextHub et DocumentPreview**
Système de gestion documentaire comprenant :
- Panneau latéral droit (ContextHub) pour la liste et l'upload
- Modale DocumentPreview pour l'aperçu multi-format
- Indicateurs de taille de contexte et filtres
- États d'activation/désactivation des documents

### **TopAppBar**
Barre de navigation supérieure avec :
- Contrôles des panneaux (toggles pour Sidebar et ContextHub)
- Menu utilisateur avec Avatar
- Sélecteurs de thème et langue
- Accès à la documentation

## Système de Streaming

L'application implémente un système de streaming sophistiqué pour une expérience utilisateur fluide :

### **Server-Sent Events (SSE)**
- Connexion streaming pour les nouveaux messages et l'édition
- Décodage progressif des chunks de données
- Gestion du signal `[DONE]` pour terminer le streaming
- Accumulation du contenu en temps réel

### **États de Streaming**
- `isLoading`: Propriété sur les messages pour indiquer le streaming actif
- Mise à jour optimiste de l'interface utilisateur
- Indicateurs visuels de progression via CircularProgress

### **Gestion des Erreurs de Streaming**
- Capture et affichage des erreurs de connexion
- Restauration de l'état en cas d'échec
- Notifications via Snackbar

## Structure du Rendu JSX

Le JSX de `App.jsx` assemble les composants principaux :

* **`Sidebar`**: Navigation entre conversations avec Logo, ExtendedFab et gestion des états de renommage/suppression.
* **`TopAppBar`**: Barre de navigation avec contrôles des panneaux, Avatar utilisateur et Menu de paramètres.
* **Zone de contenu principal**: Affiche soit `Greetings.jsx` (si pas de conversation), soit la liste des `currentMessages` avec rendu via `StreamingMarkdown`.
* **`PromptField`**: Champ de saisie avec UploadButton intégré et IconBtn d'envoi.
* **`ContextHubPanel`**: Panneau latéral droit pour la gestion des documents.
* **`DocumentPreview`**: Modale d'aperçu multi-format avec support PDF, images et texte.

### **Rendu des Messages**

Le rendu des messages utilise une approche hybride :
- **Messages utilisateur (prompts)**: Affichage en texte brut avec édition inline
- **Réponses IA**: Rendu via `StreamingMarkdown` avec support du formatage Markdown en temps réel
- **Animations**: Utilisation de Framer Motion pour des transitions fluides entre les composants

## Gestion de la Responsivité

L'application adapte automatiquement son comportement selon la taille d'écran :
- Fermeture automatique des panneaux (Sidebar, ContextHub) sur mobile après sélection
- Layouts adaptatifs pour les panneaux latéraux
- Overlays pour les écrans plus petits
- Logo adaptatif (visible dans TopAppBar sur mobile, dans Sidebar sur desktop)

## Intégration du Support RTL

L'application inclut un support complet pour les langues de droite à gauche :
- Classes CSS dynamiques basées sur la langue sélectionnée via LanguageContext
- Marges adaptatives pour les panneaux selon la direction du texte
- Composants Icon et MenuItem adaptés pour RTL

---

Le composant App constitue le cœur de l'expérience utilisateur post-authentification et orchestre toutes les interactions entre les composants principaux (Sidebar, PromptField, ContextHub, DocumentPreview, TopAppBar), offrant une expérience cohérente et responsive.

---

La manière dont l'utilisateur navigue entre les différentes vues et comment les données sont chargées pour ces vues est gérée par le [Système de Routage (React Router DOM)](./routing.md).