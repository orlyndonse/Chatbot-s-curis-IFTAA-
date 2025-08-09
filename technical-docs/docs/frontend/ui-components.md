---
sidebar_position: 7
title: Composants UI Principaux
---

# Composants UI Principaux (`src/components/`)

Le dossier `src/components/` contient une collection de composants React réutilisables qui constituent les blocs de construction de l'interface utilisateur de l'Assistant RAG Fiqh. Ces composants sont conçus pour être modulaires et sont utilisés à travers différentes pages et sections de l'application.

## Composants Généraux

* **`Avatar.jsx`**:
    * Affiche un avatar utilisateur. Il peut prendre une source d'image (`src`) ou afficher des initiales (`children`) si aucune image n'est fournie.
    * Gère différentes tailles (`size`) et formes (`shape`, par exemple "circle", "rounded").
* **`Button.jsx`**:
    * Un composant bouton stylisé et polyvalent.
    * Supporte différentes variantes (`variant`: "contained", "outlined", "text"), couleurs (`color`: "primary", "secondary", "error", etc.), et tailles (`size`).
    * Peut afficher une icône de début (`startIcon`) ou de fin (`endIcon`).
    * Gère l'état désactivé (`disabled`) et l'état de chargement (`loading`) en affichant un indicateur de progression.
* **`DocumentPreview.jsx`**:
    * Affiche un aperçu du contenu d'un document dans une modale ou un panneau.
    * Prend le contenu du document (`content`), son nom (`filename`), et le type MIME (`mimeType`) pour adapter l'affichage (par exemple, pour les PDF ou le texte brut).
    * Inclut une action de fermeture (`onClose`).
* **`Logo.jsx`**:
    * Affiche le logo de l'application. Il utilise les fichiers SVG `logo-light.svg` et `logo-dark.svg` du dossier `src/assets/` et s'adapte au thème (clair/sombre) de l'application.
* **`Menu.jsx`** et **`MenuItem.jsx`**:
    * Implémentent un menu déroulant. `Menu` est le conteneur qui gère l'ouverture/fermeture et le positionnement, tandis que `MenuItem` représente chaque élément cliquable dans le menu.
    * Utilisés par exemple pour le menu utilisateur dans le `TopAppBar`.
* **`PageTitle.jsx`**:
    * Un composant simple pour afficher un titre de page H1 de manière cohérente.
* **`Progress.jsx`**:
    * Fournit des indicateurs de progression.
    * Inclut un `Progress.Spinner` pour un indicateur de chargement circulaire et un `Progress.Linear` pour une barre de progression linéaire.
* **`PromptField.jsx`**:
    * Le champ de saisie de texte principal où l'utilisateur tape ses questions/prompts.
    * Inclut un bouton d'envoi et gère l'état du texte saisi.
    * Peut s'adapter en hauteur pour les prompts plus longs.
* **`Sidebar.jsx`**:
    * La barre latérale gauche de l'application principale.
    * Affiche la liste des conversations de l'utilisateur.
    * Permet de créer une nouvelle conversation, de sélectionner une conversation existante, de la renommer ou de la supprimer.
    * Sa visibilité est contrôlée par l'état `isSidebarOpen` dans `App.jsx`.
* **`Snackbar.jsx`**:
    * Le composant visuel pour les notifications (snackbars).
    * Il consomme les informations du `SnackbarContext` (message, sévérité, état ouvert/fermé) pour s'afficher et se masquer.
    * Affiche différents styles en fonction de la sévérité ("success", "error", etc.).
* **`TextField.jsx`**:
    * Un composant de champ de saisie de texte générique, utilisé dans les formulaires (connexion, inscription, etc.).
    * Supporte des labels, des messages d'aide, des icônes, et la gestion des erreurs de validation.
* **`TopAppBar.jsx`**:
    * La barre de navigation supérieure de l'application principale.
    * Affiche le logo, le titre de la conversation active.
    * Contient les boutons pour basculer la `Sidebar` et le `ContextHubPanel`.
    * Inclut le menu utilisateur (avatar, options de déconnexion, etc.).

## Composants Spécifiques au `ContextHub` (`src/components/contextHub/`)

Ces composants sont dédiés au panneau latéral droit ("Context Hub") qui gère le contexte des documents pour une conversation.

* **`ContextHubPanel.jsx`**:
    * Le composant principal du panneau "Context Hub".
    * Intègre les autres composants du `contextHub` pour afficher la zone de téléversement, les filtres, la liste des documents et l'indicateur de taille du contexte.
    * Sa visibilité est contrôlée par l'état `isContextHubOpen` dans `App.jsx`.
* **`ContextSizeIndicator.jsx`**:
    * Affiche une indication visuelle (par exemple, une barre de progression ou un texte) de la taille totale des documents téléversés pour le contexte actuel, potentiellement par rapport à une limite.
* **`DocumentFilters.jsx`**:
    * Fournit des options pour filtrer la liste des documents affichés (par exemple, par type, par date).
* **`DocumentItemCard.jsx`**:
    * Affiche les informations d'un seul document téléversé sous forme de carte.
    * Permet des actions sur le document comme la prévisualisation ou la suppression.
* **`DocumentUploadArea.jsx`**:
    * La zone où l'utilisateur peut glisser-déposer des fichiers ou cliquer pour sélectionner des fichiers à téléverser.
    * Gère la logique de sélection des fichiers avant de les envoyer à la fonction de téléversement dans `App.jsx`.

Ces composants sont construits en utilisant React et sont stylisés avec Tailwind CSS, comme le reste de l'application frontend. Ils sont conçus pour être composables et pour encapsuler une logique d'interface utilisateur spécifique, rendant le code de l'application plus organisé et plus facile à maintenir.

---

La communication entre ces composants frontend et le serveur backend est gérée par des [appels API, notamment via `fetchWithAuth.js`](./api-communication.md).