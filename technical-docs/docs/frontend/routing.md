---
sidebar_position: 5
title: Routage (React Router DOM)
---

# Routage avec React Router DOM

Le frontend de l'Assistant RAG Fiqh utilise la bibliothèque [React Router DOM](https://reactrouter.com/) pour gérer la navigation et le rendu des différentes vues (pages) de l'application. La configuration du routage est centralisée dans le dossier `src/routers/` et utilise les fonctionnalités modernes de React Router, notamment les "Data Routers" avec les chargeurs de données (`loaders`) et les actions de formulaire (`actions`).

## Structure du Dossier de Routage (`src/routers/`)

* **`routes.jsx`**: Fichier principal qui définit l'arborescence des routes de l'application.
* **`loaders/`**: Contient les fonctions "loader" qui sont exécutées avant le rendu d'une route pour charger des données. Chaque loader est généralement associé à une ou plusieurs routes.
* **`actions/`**: Contient les fonctions "action" qui sont exécutées lorsque des formulaires associés à une route sont soumis. Elles gèrent typiquement la logique de soumission des données au backend.

## Configuration Principale des Routes (`src/routers/routes.jsx`)

Ce fichier utilise `createBrowserRouter` et `createRoutesFromElements` de React Router DOM pour définir les routes.

```jsx
// Extrait simplifié de Code_Source/frontend/src/routers/routes.jsx
import {
  Route,
  createBrowserRouter,
  createRoutesFromElements,
  redirect,
} from 'react-router-dom';

// Import des composants de page
import App from '../App';
import Login from '../pages/Login';
// ... autres imports de pages, loaders et actions ...

// Import des loaders
import appLoader from './loaders/appLoader';
import loginLoader from './loaders/loginLoader';
// ... autres imports de loaders ...

// Import des actions
import loginAction from './actions/loginAction';
import registerAction from './actions/registerAction';
// ... autres imports d'actions ...

const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      {/* Route principale de l'application (protégée) */}
      <Route
        path="/"
        element={<App />}
        loader={appLoader} // Charge les données utilisateur et conversations
        // errorElement={<RootBoundary />} // Gestion d'erreur (non implémenté dans le code fourni)
      />

      {/* Routes d'authentification */}
      <Route path="/login" element={<Login />} loader={loginLoader} action={loginAction} />
      <Route path="/register" element={<Register />} loader={registerLoader} action={registerAction} />
      <Route path="/verify-email/:token" element={<VerifyEmailHandler />} />
      <Route path="/email-verified" element={<EmailVerified />} loader={emailVerifiedLoader} action={emailVerifiedAction} />
      {/* ... autres routes pour la réinitialisation de mot de passe, etc. ... */}

      {/* Redirection par défaut si aucune route ne correspond */}
      <Route path="*" loader={async () => redirect('/')} />
    </>
  )
);

export default router;
```

### Éléments Clés

- **`createBrowserRouter`**: Crée une instance de routeur qui utilise les APIs du DOM (par exemple, l'API History pour les URLs).
- **`createRoutesFromElements`**: Permet de définir les routes en utilisant une syntaxe JSX avec le composant `<Route>`.
- **`<Route>`**: Chaque composant `<Route>` définit une correspondance entre un chemin d'URL (`path`), un composant React à rendre (`element`), une fonction de chargement de données optionnelle (`loader`), et une fonction d'action optionnelle (`action`).

### Types de Routes

**Route Principale (`path="/"`):**
- Rend le composant `App.jsx` (l'interface principale de chat).
- Utilise `appLoader` pour charger les données de l'utilisateur et ses conversations avant d'afficher le composant App. Si le loader détermine que l'utilisateur n'est pas authentifié, il peut rediriger vers la page de connexion.

**Routes d'Authentification (par exemple, `/login`, `/register`):**
- Rendent les composants de page correspondants (par exemple, `Login.jsx`, `Register.jsx`).
- Sont associées à des loaders (par exemple, `loginLoader` peut vérifier si l'utilisateur est déjà connecté et le rediriger) et des actions (par exemple, `loginAction` est appelée lors de la soumission du formulaire de connexion).

**Routes Spécifiques (par exemple, `/verify-email/:token`):**
- Gèrent des cas comme la vérification d'email après l'inscription, en utilisant des paramètres d'URL.

**Route `*` (Catch-all):**
- Redirige vers la route principale (`/`) si aucun autre chemin ne correspond.

## Fonctions loader (`src/routers/loaders/`)

Les loaders sont des fonctions asynchrones qui sont appelées avant le rendu de la route. Ils sont utilisés pour :

- Charger des données critiques nécessaires à la page.
- Implémenter la logique de protection des routes : par exemple, vérifier si un utilisateur est authentifié avant d'accéder à une route protégée. Si ce n'est pas le cas, le loader peut retourner une `redirect` vers la page de connexion.

Les données retournées par un loader sont accessibles dans le composant de la route via le hook `useLoaderData()`.

**Exemple :** `appLoader.js` récupère les informations de l'utilisateur actuel (`/api/v1/auth/me`) et ses conversations (`/api/v1/conversations`) avant d'afficher l'application principale. S'il n'y a pas de token ou si l'utilisateur n'est pas valide, il redirige vers `/login`.

## Fonctions action (`src/routers/actions/`)

Les actions sont des fonctions asynchrones qui sont appelées lorsque des formulaires (`<Form>` de React Router) associés à une route sont soumis. Elles sont utilisées pour :

- Gérer la logique de soumission des données au backend (par exemple, envoyer les informations de connexion ou d'inscription).
- Traiter la réponse du backend.
- Effectuer des redirections après une action réussie (par exemple, rediriger vers l'application après une connexion réussie) ou retourner des erreurs à afficher dans le formulaire.

**Exemple :** `loginAction.js` récupère les données du formulaire de connexion, les envoie à l'endpoint `/api/v1/auth/login` du backend, et gère la réponse (stockage des tokens, redirection, ou retour d'erreurs).

## Intégration dans main.jsx

L'instance `router` créée dans `src/routers/routes.jsx` est fournie au composant `<RouterProvider>` dans `src/main.jsx`, ce qui active le système de routage pour l'ensemble de l'application.

```jsx
// Extrait de src/main.jsx
import { RouterProvider } from 'react-router-dom';
import router from './routers/routes';

ReactDOM.createRoot(document.getElementById('root')).render(
  <RouterProvider router={router} />
);
```

## Avantages de cette Architecture

Ce système de routage basé sur React Router DOM 6+ permet :

- Une gestion déclarative des routes
- Un chargement de données efficace grâce aux loaders
- Une gestion propre des soumissions de formulaires via les actions
- Une protection des routes intégrée
- Une expérience utilisateur fluide avec des transitions optimisées

---

La gestion de l'état global, comme l'état de l'utilisateur ou les notifications, est souvent gérée via des [Contextes React](../frontend/state-management.md).