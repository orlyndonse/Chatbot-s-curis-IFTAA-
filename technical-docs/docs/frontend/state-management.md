---
sidebar_position: 6
title: Gestion de l'État (Contextes React)
---

# Gestion de l'État avec les Contextes React

Pour gérer l'état global et partager des données ou des fonctions à travers différents niveaux de composants sans avoir à passer manuellement des props (prop drilling), l'application frontend utilise l'API Context de React. Deux contextes principaux sont définis dans le dossier `src/contexts/`.

## 1. `UserContext` (`src/contexts/UserContext.jsx`)

Ce contexte est crucial pour la gestion de l'état d'authentification de l'utilisateur et des informations qui lui sont associées.

* **État Géré**:
    * `currentUser`: Stocke les informations de l'utilisateur actuellement connecté (par exemple, email, prénom, nom, rôle). Initialisé à `null`.
    * `accessToken`: Stocke le token JWT d'accès. Initialisé à partir du `localStorage` pour la persistance entre les sessions.
    * `refreshToken`: Stocke le token JWT de rafraîchissement. Initialisé également à partir du `localStorage`.
    * `isLoading`: Un booléen pour indiquer si une opération d'authentification (comme la vérification initiale du token) est en cours.

* **Fonctions Fournies**:
    * `login(userData, access, refresh)`: Met à jour `currentUser`, `accessToken`, `refreshToken`, et stocke les tokens dans le `localStorage`.
    * `logout(navigate)`: Réinitialise les états à `null` ou leurs valeurs initiales, supprime les tokens du `localStorage`, et redirige l'utilisateur (généralement vers la page de connexion) en utilisant la fonction `Maps` de React Router.
    * `updateTokens(newAccessToken, newRefreshToken)`: Met à jour les tokens d'accès et de rafraîchissement en mémoire et dans le `localStorage`. Utilisée par `fetchWithAuth` lors du rafraîchissement d'un token.
    * `updateUser(updatedUserData)`: Permet de mettre à jour les informations de `currentUser` (non implémenté dans le code fourni mais la structure est là).

* **Logique d'Initialisation (`useEffect`)**:
    * Au montage du `UserProvider`, un `useEffect` tente de charger les tokens depuis le `localStorage`.
    * Si un `accessToken` est trouvé, il tente de récupérer les informations de l'utilisateur via un appel à `/api/v1/auth/me` en utilisant `fetchWithAuth`.
        * Si l'appel réussit, `currentUser` est mis à jour.
        * Si le token est invalide ou expiré (et ne peut être rafraîchi par `fetchWithAuth`), la fonction `logout` est appelée pour nettoyer l'état.
    * Gère l'état `isLoading` pendant ce processus de vérification initiale.

* **Utilisation**:
    * Le `UserProvider` enveloppe l'application dans `src/main.jsx`, rendant le contexte accessible globalement.
    * Les composants peuvent consommer ce contexte via le hook `useContext(UserContext)` ou un hook personnalisé comme `useAuth()` (non explicitement fourni mais une pratique courante).

## 2. `SnackbarContext` (`src/contexts/SnackbarContext.jsx`)

Ce contexte gère l'affichage des notifications temporaires (snackbars) à l'utilisateur pour fournir des retours sur les actions (par exemple, succès d'une opération, erreur).

* **État Géré**:
    * `snackbarOpen`: Booléen indiquant si le snackbar est visible.
    * `snackbarMessage`: Le message à afficher dans le snackbar.
    * `snackbarSeverity`: Le type de notification (par exemple, "success", "error", "warning", "info"), qui influence le style du snackbar.

* **Fonctions Fournies**:
    * `showSnackbar(message, severity)`: Fonction pour déclencher l'affichage d'un snackbar avec un message et une sévérité donnés. Elle rend le snackbar visible et le cache automatiquement après un délai (défini par `SNACKBAR_DURATION`, par défaut 6000 ms).

* **Utilisation**:
    * Le `SnackbarProvider` enveloppe également l'application dans `src/main.jsx`.
    * Les composants peuvent afficher des notifications en utilisant le hook `useSnackbar()` (défini dans `src/hooks/useSnackbar.js`), qui fournit un accès simplifié à la fonction `showSnackbar`.
    * Le composant `Snackbar.jsx` (dans `src/components/`) est responsable du rendu visuel du snackbar en fonction des états du `SnackbarContext`.

L'utilisation de l'API Context de React permet une gestion de l'état partagé de manière propre et découplée, particulièrement pour des fonctionnalités transversales comme l'authentification et les notifications. Pour des besoins de gestion d'état plus complexes et spécifiques à des fonctionnalités (comme l'état des conversations et des messages dans `App.jsx`), des états locaux aux composants (`useState`, `useReducer`) ou des bibliothèques de gestion d'état plus dédiées (Redux, Zustand, Jotai) pourraient être envisagées si la complexité l'exigeait. Dans ce projet, l'état principal des conversations est géré au niveau du composant `App.jsx`.

---

Les éléments visuels réutilisables de l'application sont définis en tant que [Composants UI Principaux](./ui-components.md).