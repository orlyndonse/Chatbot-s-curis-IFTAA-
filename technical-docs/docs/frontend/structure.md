---
sidebar_position: 1
title: Structure du Projet Frontend
---

# Structure du Projet Frontend

Le frontend de l'Assistant RAG Fiqh est une application React moderne construite avec Vite. Son code source est situé dans le dossier `Code_Source/frontend/`. L'organisation des fichiers vise une séparation claire des préoccupations, facilitant la maintenance et le développement.

## Organisation Générale des Dossiers (`Code_Source/frontend/`)

```
frontend/
├── public/                     # Fichiers statiques servis directement (ex: favicon.svg)
├── src/                        # Contient tout le code source de l'application React
│   ├── assets/                 # Ressources statiques (images, logos, etc.) importées dans les composants
│   │   └── assets.js           # Fichier JavaScript exportant les assets importés
│   ├── components/             # Composants React réutilisables
│   │   ├── contextHub/         # Composants spécifiques au panneau de gestion des documents (Context Hub)
│   │   │   ├── ContextHubPanel.jsx
│   │   │   ├── ContextSizeIndicator.jsx
│   │   │   ├── DocumentFilters.jsx
│   │   │   ├── DocumentItemCard.jsx
│   │   │   └── DocumentUploadArea.jsx
│   │   ├── Avatar.jsx
│   │   ├── Button.jsx
│   │   ├── DocumentPreview.jsx
│   │   ├── Logo.jsx
│   │   ├── Menu.jsx
│   │   ├── MenuItem.jsx
│   │   ├── PageTitle.jsx
│   │   ├── Progress.jsx
│   │   ├── PromptField.jsx
│   │   ├── Sidebar.jsx
│   │   ├── Snackbar.jsx
│   │   ├── TextField.jsx
│   │   └── TopAppBar.jsx
│   ├── contexts/               # Contextes React pour la gestion de l'état global
│   │   ├── SnackbarContext.jsx
│   │   └── UserContext.jsx
│   ├── hooks/                  # Hooks React personnalisés
│   │   ├── useSnackbar.js
│   │   └── useToggle.js
│   ├── pages/                  # Composants React représentant des pages entières de l'application
│   │   ├── EmailVerified.jsx
│   │   ├── Greetings.jsx
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── ResetLink.jsx
│   │   ├── ResetPassword.jsx
│   │   ├── ResetPasswordSuccess.jsx
│   │   ├── SendEmail.jsx
│   │   └── VerifyEmailHandler.jsx
│   ├── routers/                # Configuration du routage avec React Router DOM
│   │   ├── actions/            # Fonctions d'action pour les soumissions de formulaires
│   │   │   ├── EmailVerifiedAction.js
│   │   │   ├── loginAction.js
│   │   │   ├── registerAction.js
│   │   │   ├── resetLinkAction.js
│   │   │   ├── resetPassword.js
│   │   │   ├── resetPasswordSuccessAction.js
│   │   │   └── sendEmailAction.js
│   │   ├── loaders/            # Fonctions de chargement de données pour les routes
│   │   │   ├── appLoader.js
│   │   │   ├── EmailVerifiedLoader.js
│   │   │   ├── loginLoader.js
│   │   │   ├── registerLoader.js
│   │   │   ├── resetLinkLoader.js
│   │   │   ├── resetPasswordLoader.js
│   │   │   ├── resetPasswordSuccessReloader.js
│   │   │   └── sendEmailLoader.js
│   │   └── routes.jsx          # Définition principale des routes de l'application
│   ├── utils/                  # Fonctions utilitaires
│   │   └── fetchWithAuth.js    # Utilitaire pour les appels API authentifiés
│   ├── App.jsx                 # Composant racine de l'application (layout principal)
│   ├── index.css               # Styles CSS globaux et configuration Tailwind
│   └── main.jsx                # Point d'entrée de l'application React (rendu du composant racine)
├── .eslintrc.cjs               # (ou eslint.config.js) Configuration ESLint pour le linting du code
├── index.html                  # Fichier HTML principal servi par Vite
├── package.json                # Métadonnées du projet, scripts et dépendances Node.js
├── package-lock.json           # Verrouillage des versions des dépendances
├── postcss.config.js           # Configuration PostCSS (utilisé par Tailwind CSS)
├── tailwind.config.js          # Configuration Tailwind CSS
└── vite.config.js              # Fichier de configuration pour Vite (serveur de dev, build, proxy)
```

## Description des Dossiers Clés dans `src/`

### `assets/`
Contient les ressources statiques comme les images (logo, bannière) qui sont importées directement dans les composants JavaScript/JSX. Le fichier `assets.js` centralise l'exportation de ces assets.

### `components/`
Regroupe les composants React réutilisables qui constituent l'interface utilisateur.

- **`contextHub/`**: Un sous-dossier dédié aux composants formant le "Context Hub", le panneau latéral droit pour la gestion des documents (téléversement, liste, filtres, indicateur de taille).
- Les autres fichiers sont des composants d'interface utilisateur plus généraux (boutons, champs de texte, barre de navigation, barre latérale, etc.).

### `contexts/`
Implémente les Contextes React pour partager l'état et la logique à travers différentes parties de l'application sans avoir à passer des props manuellement à chaque niveau.

- `UserContext.jsx`: Gère l'état de l'utilisateur authentifié et les tokens d'authentification.
- `SnackbarContext.jsx`: Gère l'affichage des notifications (snackbars) à l'utilisateur.

### `hooks/`
Contient des hooks React personnalisés pour encapsuler et réutiliser la logique d'état ou des effets secondaires.

- `useSnackbar.js`: Hook pour accéder facilement aux fonctions du `SnackbarContext`.
- `useToggle.js`: Hook simple pour gérer un état booléen de bascule (toggle).

### `pages/`
Composants qui représentent des vues ou des pages complètes de l'application, typiquement associées à des routes spécifiques (par exemple, les pages de connexion, d'inscription, de vérification d'email, etc.). Le composant `Greetings.jsx` sert de page d'accueil pour la zone de chat.

### `routers/`
Gère la logique de navigation de l'application à l'aide de React Router DOM.

- **`actions/`**: Contient les fonctions d'action utilisées par React Router pour gérer les soumissions de formulaires (par exemple, `loginAction.js`, `registerAction.js`).
- **`loaders/`**: Contient les fonctions de chargement de données utilisées par React Router pour récupérer des données avant le rendu d'une route (par exemple, `appLoader.js` pour charger les données utilisateur et les conversations initiales).
- **`routes.jsx`**: Définit la configuration principale des routes de l'application, en associant les chemins d'URL aux composants de page, aux loaders et aux actions.

### `utils/`
Fonctions utilitaires diverses.

- `fetchWithAuth.js`: Une fonction wrapper pour les appels `fetch`, qui ajoute automatiquement le token d'authentification aux en-têtes et gère la logique de base des erreurs et des redirections.

### Fichiers racine de `src/`

- **`App.jsx`**: Le composant principal qui assemble la structure de base de l'application (layout, barre de navigation, barre latérale, zone de chat principale) et gère une partie importante de l'état de l'application (conversations actives, messages, etc.).
- **`index.css`**: Fichier CSS global, incluant les directives Tailwind CSS et potentiellement des styles personnalisés de base.
- **`main.jsx`**: Le point d'entrée JavaScript de l'application. Il initialise React, attache le composant `App` au DOM, et configure le `RouterProvider` et les fournisseurs de contexte (`UserProvider`, `SnackbarProvider`).

## Fichiers de Configuration à la Racine du Frontend

- **`index.html`**: Le template HTML de base servi par Vite, dans lequel l'application React est injectée. Il inclut également des liens vers les polices et les icônes Material Symbols.
- **`vite.config.js`**: Fichier de configuration pour Vite, définissant le port du serveur de développement et la configuration du proxy pour les appels API vers le backend.
- **`tailwind.config.js`** et **`postcss.config.js`**: Fichiers de configuration pour Tailwind CSS, permettant de personnaliser le thème, les couleurs, les polices, etc.
- **`package.json`**: Définit les métadonnées du projet, les scripts (`dev`, `build`, `lint`), et les dépendances JavaScript.

## Conclusion

Cette structure modulaire aide à maintenir le code organisé et à faciliter la collaboration et l'évolution du projet frontend. La séparation claire entre les composants, les pages, les contextes, et les utilitaires permet une meilleure maintenabilité et réutilisabilité du code.

---

Après avoir exploré la structure, nous examinerons la [Configuration et le Processus de Build du Frontend](./config-build.md) avec Vite.