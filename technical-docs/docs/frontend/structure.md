---
sidebar_position: 1
title: Structure du Projet Frontend
---

# Structure du Projet Frontend

Le frontend de l'Assistant RAG Fiqh est une application React moderne construite avec Vite. Son code source est situé dans le dossier `Code_Source/frontend/`. L'organisation des fichiers vise une séparation claire des préoccupations, facilitant la maintenance et le développement.

## Organisation Générale des Dossiers (`Code_Source/frontend/`)

```
frontend/
├── node_modules/               # Dépendances Node.js installées
├── public/                     # Fichiers statiques servis directement
├── src/                        # Contient tout le code source de l'application React
│   ├── assets/                 # Ressources statiques (images, logos, icônes)
│   │   ├── icons/              # Icônes SVG utilisées dans l'application
│   │   ├── assets.js           # Fichier JavaScript exportant les assets importés
│   │   ├── avatar.jpg
│   │   ├── banner.png
│   │   ├── banner1.webp
│   │   ├── favicon.svg
│   │   ├── favicon2.svg
│   │   ├── logo-dark.svg
│   │   ├── logo-icon.svg
│   │   └── logo-light.svg
│   ├── components/             # Composants React réutilisables
│   │   ├── contextHub/         # Composants spécifiques au panneau de gestion des documents
│   │   │   ├── ContextHubPanel.jsx
│   │   │   ├── ContextSizeIndicator.jsx
│   │   │   ├── DocumentFilters.jsx
│   │   │   ├── DocumentItemCard.jsx
│   │   │   └── DocumentUploadArea.jsx
│   │   ├── Avatar.jsx
│   │   ├── Button.jsx
│   │   ├── DocumentPreview.jsx
│   │   ├── Icon.jsx            # Composant pour les icônes SVG locales
│   │   ├── LogsPanel.jsx       # Panneau de débogage des logs
│   │   ├── Logo.jsx
│   │   ├── Menu.jsx
│   │   ├── MenuItem.jsx
│   │   ├── PageTitle.jsx
│   │   ├── Progress.jsx
│   │   ├── PromptField.jsx
│   │   ├── Sidebar.jsx
│   │   ├── Snackbar.jsx
│   │   ├── StreamingMarkdown.jsx # Composant pour l'affichage en streaming
│   │   ├── TextField.jsx
│   │   ├── ToggleIcons.jsx     # Icônes SVG pour les toggles
│   │   └── TopAppBar.jsx
│   ├── contexts/               # Contextes React pour la gestion de l'état global
│   │   ├── LanguageContext.jsx # Contexte pour la gestion de la langue
│   │   ├── SnackBarContext.jsx
│   │   └── UserContext.jsx
│   ├── hooks/                  # Hooks React personnalisés
│   │   ├── useIcon.js          # Hook pour charger les icônes
│   │   ├── useSnackbar.js
│   │   └── useToggle.js
│   ├── pages/                  # Composants React représentant des pages entières
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
│   │   │   ├── resetPasswordSuccessLoader.js
│   │   │   └── sendEmailLoader.js
│   │   └── routes.jsx          # Définition principale des routes de l'application
│   ├── utils/                  # Fonctions utilitaires
│   │   ├── fetchWithAuth.js    # Utilitaire pour les appels API authentifiés
│   │   └── translations.js     # Fichier de traductions
│   ├── .prettierignore         # Fichiers ignorés par Prettier
│   ├── .prettierrc             # Configuration Prettier
│   ├── App.jsx                 # Composant racine de l'application (layout principal)
│   ├── index.css               # Styles CSS globaux et configuration Tailwind
│   └── main.jsx                # Point d'entrée de l'application React
├── .env                        # Variables d'environnement
├── .gitignore                  # Fichiers ignorés par Git
├── eslint.config.js            # Configuration ESLint
├── index.html                  # Fichier HTML principal servi par Vite
├── package-lock.json           # Verrouillage des versions des dépendances
├── package.json                # Métadonnées du projet, scripts et dépendances Node.js
├── postcss.config.js           # Configuration PostCSS (utilisé par Tailwind CSS)
├── README.md                   # Documentation du projet
├── tailwind.config.js          # Configuration Tailwind CSS
└── vite.config.js              # Fichier de configuration pour Vite
```

## Description des Dossiers Clés dans `src/`

### `assets/`
Contient les ressources statiques comme les images, logos et icônes qui sont importées directement dans les composants JavaScript/JSX. Le sous-dossier `icons/` contient les icônes SVG utilisées par le composant `Icon.jsx`. Le fichier `assets.js` centralise l'exportation de ces assets.

### `components/`
Regroupe les composants React réutilisables qui constituent l'interface utilisateur.

#### **Composants Principaux d'Interface**
- **`Sidebar.jsx`**: Panneau latéral gauche contenant le Logo, la navigation entre conversations, les fonctionnalités de renommage/suppression, et l'ExtendedFab pour créer de nouvelles discussions.
- **`TopAppBar.jsx`**: Barre de navigation supérieure avec contrôles des panneaux, Avatar utilisateur, Menu de paramètres (thème, langue, documentation, déconnexion).
- **`PromptField.jsx`**: Zone de saisie principale avec champ multiline auto-redimensionnable, UploadButton intégré, et IconBtn d'envoi avec gestion des états de chargement.
- **`StreamingMarkdown.jsx`**: Composant spécialisé pour l'affichage du contenu Markdown avec support du streaming en temps réel et gestion des états de chargement.

#### **Gestion des Documents**
- **`DocumentPreview.jsx`**: Modale d'aperçu multi-format (PDF, images, texte) avec boutons d'action pour activer/désactiver les documents dans le contexte.
- **`contextHub/`**: Sous-dossier dédié aux composants du "Context Hub" - le panneau latéral droit pour la gestion des documents (téléversement, liste, filtres, indicateur de taille).

#### **Composants d'Interface de Base**
- **`Button.jsx`**: Ensemble de composants boutons (Button, IconBtn, ExtendedFab, UploadButton) avec variantes et animations.
- **`Avatar.jsx`**: Affichage d'avatar utilisateur avec génération de couleur basée sur le nom.
- **`Logo.jsx`**: Composant logo adaptatif (versions claire/sombre) avec navigation vers l'accueil.
- **`Icon.jsx`**: Système d'icônes unifié supportant les icônes SVG locales et Material Symbols.
- **`Menu.jsx` / `MenuItem.jsx`**: Composants pour les menus déroulants avec support des icônes et actions.
- **`Progress.jsx`**: Indicateurs de chargement (CircularProgress, LinearProgress) avec animations.
- **`TextField.jsx`**: Champs de formulaire standardisés.
- **`Snackbar.jsx`**: Notifications utilisateur avec animations.
- **`ToggleIcons.jsx`**: Icônes SVG spécialisées pour les états de toggle.
- **`LogsPanel.jsx`**: Composant de débogage pour l'affichage des logs (outil de développement).
- **`PageTitle.jsx`**: Gestion des titres de page via Helmet.

### `contexts/`
Implémente les Contextes React pour partager l'état et la logique à travers différentes parties de l'application sans avoir à passer des props manuellement à chaque niveau.

- `UserContext.jsx`: Gère l'état de l'utilisateur authentifié et les tokens d'authentification.
- `SnackBarContext.jsx`: Gère l'affichage des notifications (snackbars) à l'utilisateur.
- `LanguageContext.jsx`: Gère la langue actuelle de l'interface et les traductions.

### `hooks/`
Contient des hooks React personnalisés pour encapsuler et réutiliser la logique d'état ou des effets secondaires.

- `useSnackbar.js`: Hook pour accéder facilement aux fonctions du `SnackBarContext`.
- `useToggle.js`: Hook simple pour gérer un état booléen de bascule (toggle).
- `useIcon.js`: Hook pour charger et gérer les icônes SVG.

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
- `translations.js`: Gère les chaînes de traduction pour l'internationalisation de l'application.

### Fichiers racine de `src/`

- **`App.jsx`**: Le composant principal qui assemble la structure de base de l'application (layout, barre de navigation, barre latérale, zone de chat principale) et gère une partie importante de l'état de l'application (conversations actives, messages, streaming en temps réel, gestion des logs de débogage).
- **`index.css`**: Fichier CSS global, incluant les directives Tailwind CSS et potentiellement des styles personnalisés de base.
- **`main.jsx`**: Le point d'entrée JavaScript de l'application. Il initialise React, attache le composant `App` au DOM, et configure le `RouterProvider` et les fournisseurs de contexte (`UserProvider`, `SnackBarProvider`, `LanguageProvider`).

## Fichiers de Configuration à la Racine du Frontend

- **`index.html`**: Le template HTML de base servi par Vite, dans lequel l'application React est injectée. Il inclut également des liens vers les polices et les icônes Material Symbols.
- **`vite.config.js`**: Fichier de configuration pour Vite, définissant le port du serveur de développement et la configuration du proxy pour les appels API vers le backend.
- **`tailwind.config.js`** et **`postcss.config.js`**: Fichiers de configuration pour Tailwind CSS, permettant de personnaliser le thème, les couleurs, les polices, etc.
- **`package.json`**: Définit les métadonnées du projet, les scripts (`dev`, `build`, `lint`), et les dépendances JavaScript.
- **`eslint.config.js`**: Configuration ESLint pour le linting du code JavaScript/React.
- **`.prettierrc`** et **`.prettierignore`**: Configuration de Prettier pour le formatage automatique du code.

## Fonctionnalités Principales

### Streaming en Temps Réel
L'application intègre le streaming des réponses de l'IA en temps réel, offrant une expérience utilisateur fluide et interactive. Cette fonctionnalité est implémentée via :
- Le composant `StreamingMarkdown.jsx` pour l'affichage progressif du contenu
- Des endpoints de streaming dans `App.jsx` pour les nouveaux messages et l'édition

### Système de Logs de Débogage
Un système de logs intégré permet de suivre en temps réel les opérations de streaming, les appels API et les erreurs, facilitant le débogage et la surveillance des performances.

### Gestion du Markdown RTL
Le composant `StreamingMarkdown.jsx` inclut une prise en charge complète du texte de droite à gauche (RTL) avec un style adapté à l'arabe, incluant :
- Direction RTL native
- Alignement à droite pour tous les éléments
- Styles adaptés pour les listes, tableaux et éléments de code

## Technologies Utilisées

- **React** avec **Vite** pour le développement et le build
- **Tailwind CSS** pour le styling avec support RTL
- **React Router DOM** avec actions et loaders pour le routage
- **React Markdown** avec **remark-gfm** pour le rendu du contenu Markdown
- **Framer Motion** pour les animations fluides
- **ESLint** et **Prettier** pour la qualité et le formatage du code
- **PostCSS** pour le traitement CSS

## Conclusion

Cette structure modulaire aide à maintenir le code organisé et à faciliter la collaboration et l'évolution du projet frontend. La séparation claire entre les composants, les pages, les contextes, et les utilitaires permet une meilleure maintenabilité et réutilisabilité du code. Les fonctionnalités de streaming, de débogage et de gestion RTL enrichissent l'expérience utilisateur tout en maintenant une architecture propre et extensible.

---

Après avoir exploré la structure, nous examinerons la [Configuration et le Processus de Build du Frontend](./config-build.md) avec Vite.