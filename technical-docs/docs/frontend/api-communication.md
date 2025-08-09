---
sidebar_position: 8
title: Communication avec le Backend (fetchWithAuth.js)
---

# Communication avec le Backend (`src/utils/fetchWithAuth.js`)

La communication entre l'application frontend React et le backend FastAPI est gérée principalement par des appels API HTTP. Le fichier `src/utils/fetchWithAuth.js` fournit une fonction utilitaire `fetchWithAuth` qui encapsule la logique standard de `fetch` pour inclure automatiquement les tokens d'authentification, gérer le rafraîchissement des tokens, et traiter les réponses de manière standardisée.

## Fonction `fetchWithAuth`

Cette fonction est un wrapper autour de l'API `fetch` native du navigateur.

```javascript
// Extrait simplifié de Code_Source/frontend/src/utils/fetchWithAuth.js
import { UserContext } from "../contexts/UserContext"; // Pour accéder aux tokens et fonctions de màj
import { useContext } from "react"; // Utilisé indirectement via UserContext

// L'URL de base de l'API est définie ici, pointant vers le backend FastAPI
export const API_BASE_URL = "http://localhost:8000"; // Ou process.env.REACT_APP_API_URL

export const fetchWithAuth = async (url, options = {}) => {
    let { accessToken, refreshToken, updateTokens, logout } = window.userContext || {};
    // ... (logique pour s'assurer que le contexte est disponible)

    const defaultHeaders = {
        'Content-Type': 'application/json',
        // D'autres en-têtes par défaut si nécessaire
    };

    if (accessToken && !options.noAuth) {
        defaultHeaders['Authorization'] = `Bearer ${accessToken}`;
    }

    const config = {
        ...options,
        headers: {
            ...defaultHeaders,
            ...options.headers,
        },
    };

    // Construire l'URL complète
    const fullUrl = `${API_BASE_URL}${url}`;

    let response = await fetch(fullUrl, config);

    if (response.status === 401 && !options.isRetry && refreshToken && !options.noAuth) {
        // ... (Logique de rafraîchissement du token) ...
        // Tente de rafraîchir le token d'accès en utilisant le refreshToken
        // Si succès, réessaie la requête originale avec le nouveau accessToken
        // Si échec, déconnecte l'utilisateur
    }
    // ... (Gestion des autres réponses et erreurs) ...
    return response;
};
```

## Fonctionnalités Principales

### 1. Configuration de l'URL de Base

**`API_BASE_URL`:**
Une constante (actuellement `http://localhost:8000`) définit l'URL de base du serveur backend. Toutes les URLs relatives passées à `fetchWithAuth` sont préfixées par cette base.

### 2. Accès au UserContext

La fonction accède aux tokens (`accessToken`, `refreshToken`) et aux fonctions de mise à jour (`updateTokens`, `logout`) via `window.userContext`. Ceci est une manière de rendre le `UserContext` accessible en dehors des composants React. Le `UserContext` lui-même injecte ses valeurs dans `window.userContext` lors de son initialisation.

### 3. Ajout Automatique du Token d'Accès

Si un `accessToken` est disponible et que l'option `noAuth` n'est pas explicitement mise à `true` dans les options de la requête, l'en-tête `Authorization: Bearer {accessToken}` est automatiquement ajouté à la requête.

### 4. Configuration des En-têtes

Un `Content-Type: application/json` est défini par défaut pour les requêtes envoyant des données JSON. Les en-têtes personnalisés passés dans `options.headers` peuvent surcharger ou compléter les en-têtes par défaut.

### 5. Gestion du Rafraîchissement du Token (Retry Logic)

Si une requête échoue avec un statut **401 Unauthorized** (indiquant potentiellement un `accessToken` expiré), que ce n'est pas déjà une tentative de rafraîchissement (`!options.isRetry`), qu'un `refreshToken` est disponible, et que la requête n'était pas marquée `noAuth` :

1. Une requête est envoyée à l'endpoint `/api/v1/auth/refresh-token` du backend avec le `refreshToken`.
2. Si le rafraîchissement réussit, le backend renvoie un nouvel `accessToken` (et potentiellement un nouveau `refreshToken`).
3. La fonction `updateTokens` du `UserContext` est appelée pour mettre à jour les tokens stockés.
4. La requête originale qui avait échoué est alors réessayée une fois avec le nouvel `accessToken` et l'option `isRetry: true` pour éviter les boucles de rafraîchissement infinies.
5. Si le rafraîchissement du token échoue (par exemple, le `refreshToken` est aussi expiré ou invalide), la fonction `logout` du `UserContext` est appelée, ce qui déconnectera l'utilisateur et le redirigera probablement vers la page de connexion.

### 6. Gestion des Erreurs et des Réponses

- La fonction retourne l'objet `Response` de `fetch`. Le code appelant est responsable de vérifier `response.ok` et de traiter le corps de la réponse (par exemple, avec `response.json()`).
- Si la réponse n'est pas `ok` (et que ce n'est pas une erreur 401 gérée par le rafraîchissement), une erreur est levée, qui peut être interceptée par le code appelant.

### 7. Gestion des Requêtes Multipart

Pour les requêtes `multipart/form-data` (comme le téléversement de fichiers), l'en-tête `Content-Type` ne doit pas être explicitement défini sur `application/json` ; le navigateur le définira correctement avec la bonne limite (boundary). La fonction `fetchWithAuth` le permet en n'appliquant le `Content-Type: application/json` que si `options.body` est une chaîne (`JSON.stringify`).

## Utilisation

`fetchWithAuth` est utilisé dans divers endroits de l'application pour interagir avec l'API backend :

- **Dans les fonctions loader et action de React Router** (par exemple, pour charger des données initiales, se connecter, s'inscrire)
- **Directement dans les composants** (par exemple, dans `App.jsx` pour récupérer des messages, soumettre des prompts, téléverser des fichiers)

### Exemples d'utilisation

```javascript
// Requête GET simple
const response = await fetchWithAuth('/api/v1/conversations');
const conversations = await response.json();

// Requête POST avec données
const response = await fetchWithAuth('/api/v1/auth/login', {
  method: 'POST',
  body: JSON.stringify({ email, password })
});

// Requête sans authentification
const response = await fetchWithAuth('/api/v1/auth/register', {
  method: 'POST',
  body: JSON.stringify(userData),
  noAuth: true
});

// Upload de fichier
const formData = new FormData();
formData.append('file', file);
const response = await fetchWithAuth('/api/v1/upload', {
  method: 'POST',
  body: formData
  // Content-Type sera automatiquement défini par le navigateur
});
```

## Avantages

Cet utilitaire centralise la logique d'authentification des appels API, simplifiant le code dans les composants et les services qui ont besoin de communiquer avec le backend de manière sécurisée. Il offre :

- **Gestion automatique de l'authentification** avec injection des tokens
- **Rafraîchissement transparent des tokens** expirés
- **Gestion centralisée des erreurs** d'authentification
- **Configuration uniforme** des en-têtes et de l'URL de base
- **Support des différents types de contenu** (JSON, FormData, etc.)

---

Le style visuel de l'application frontend est géré par [Tailwind CSS et des styles CSS personnalisés](../frontend/styling.md).