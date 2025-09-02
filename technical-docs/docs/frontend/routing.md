---
sidebar_position: 5
title: Routage (React Router DOM)
---

# Routage avec React Router DOM

Le frontend utilise [React Router DOM](https://reactrouter.com/) pour gérer la navigation. La configuration est centralisée dans `src/routers/` et utilise les "Data Routers" avec des `loaders` pour le chargement de données et des `actions` pour la soumission de formulaires.

## Fichier de Configuration (`src/routers/routes.jsx`)

Ce fichier utilise `createBrowserRouter` en lui passant un **tableau d'objets de route**, qui est la syntaxe moderne recommandée.

```jsx
// Extrait de src/routers/routes.jsx
import { createBrowserRouter } from "react-router-dom";
import App from '../App.jsx'
// ... autres imports de pages, loaders et actions ...

const router = createBrowserRouter([
    {
        path: '/',
        element: <App />,
        loader: appLoader,
    },
    {
        path: '/verify-email', // Attend un ?token=... dans l'URL
        element: <VerifyEmailHandler />,
    },
    {
        path: '/login',
        element: <Login />,
        action: loginAction,
        loader: loginLoader,
    },
    {
        path: '/register',
        element: <Register />,
        loader: registerLoader,
        action: registerAction,
    },
    {
        path: '/reset-link',
        element: <ResetLink />,
        loader: resetLinkLoader,
        action: resetLinkAction,
    },
    {
        path: '/reset-password', // Attend un ?token=...
        element: <ResetPassword />,
        loader: resetPasswordLoader,
        action: resetPasswordAction,
    },
    {
        path: '/send-email', // Attend un ?email=...
        element: <SendEmail />,
        loader: sendEmailLoader,
        action: sendEmailAction
    },
    {
        path: "/resetpasswordsuccess", // Attend un ?email=...
        element: <ResetPasswordSuccess />,
        loader: resetPasswordSuccessLoader,
        action: resetPasswordSuccessAction
    },
]);

export default router;
```

## Éléments Clés

### `createBrowserRouter`
Crée l'instance du routeur qui utilise les APIs du navigateur pour gérer l'historique et les URLs.

### Tableau de routes
Chaque objet du tableau définit une route avec :

- **`path`**: Le chemin de l'URL (par exemple : `/`, `/login`, `/register`).
- **`element`**: Le composant React à afficher pour cette route.
- **`loader`** (Optionnel): Une fonction asynchrone qui charge des données avant le rendu de la page. Les données sont accessibles via le hook `useLoaderData`. Utilisé pour protéger les routes et récupérer les données initiales.
- **`action`** (Optionnel): Une fonction asynchrone qui s'exécute lors de la soumission d'un `<Form>` de React Router. Idéal pour gérer les mutations de données (login, register, etc.).

## Types de Routes

### Route Principale (`path="/"`)
- Rend le composant `App.jsx` (l'interface principale de chat).
- Utilise `appLoader` pour charger les données de l'utilisateur et ses conversations avant d'afficher le composant. Si l'utilisateur n'est pas authentifié, le loader peut rediriger vers la page de connexion.

### Routes d'Authentification
- **`/login`, `/register`**: Rendent les composants de connexion et d'inscription.
- Associées à des loaders (vérification si l'utilisateur est déjà connecté) et des actions (traitement des formulaires de connexion/inscription).
- **`/reset-link`, `/reset-password`, `/send-email`**: Gèrent le processus de réinitialisation de mot de passe.

### Routes Spécifiques
- **`/verify-email`**: Gère la vérification d'email après inscription, utilisant des paramètres de query (`?token=...`).
- **`/resetpasswordsuccess`**: Page de confirmation après réinitialisation réussie.

## Fonctions loader (`src/routers/loaders/`)

Les loaders sont des fonctions asynchrones appelées avant le rendu de la route. Ils servent à :

- Charger des données critiques nécessaires à la page
- Implémenter la protection des routes (vérification d'authentification)
- Effectuer des redirections conditionnelles

Les données retournées par un loader sont accessibles dans le composant via `useLoaderData()`.

**Exemple** : `appLoader.js` récupère les informations utilisateur (`/api/v1/auth/me`) et ses conversations (`/api/v1/conversations`) avant d'afficher l'application principale. Si aucun token valide n'est trouvé, il redirige vers `/login`.

## Fonctions action (`src/routers/actions/`)

Les actions sont des fonctions asynchrones appelées lors de la soumission de formulaires (`<Form>` de React Router). Elles permettent de :

- Gérer la logique de soumission des données au backend
- Traiter les réponses du serveur
- Effectuer des redirections après succès ou retourner des erreurs

**Exemple** : `loginAction.js` récupère les données du formulaire de connexion, les envoie à l'endpoint `/api/v1/auth/login`, stocke les tokens et redirige vers l'application ou retourne des erreurs.

## Intégration dans main.jsx

L'instance `router` créée dans `src/routers/routes.jsx` est fournie au composant `<RouterProvider>` dans `src/main.jsx`, activant le système de routage pour toute l'application.

```jsx
// Extrait de src/main.jsx
import { RouterProvider } from 'react-router-dom';
import router from './routers/routes';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <UserProvider>
      <LanguageProvider>
        <SnackbarProvider>
          <RouterProvider router={router} />
        </SnackbarProvider>
      </LanguageProvider>
    </UserProvider>
  </StrictMode>
);
```

## Avantages de cette Architecture

Ce système de routage basé sur React Router DOM 6+ offre :

- Une gestion déclarative des routes
- Un chargement de données efficace grâce aux loaders
- Une gestion propre des soumissions de formulaires via les actions
- Une protection des routes intégrée
- Une expérience utilisateur fluide avec des transitions optimisées
- Une séparation claire entre la logique de données (loaders/actions) et les composants UI

---

La gestion de l'état global, comme l'état de l'utilisateur ou les notifications, est souvent gérée via des [Contextes React](../frontend/state-management.md).