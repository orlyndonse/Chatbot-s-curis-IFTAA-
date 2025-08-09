---
sidebar_position: 3
title: Configuration de l'Environnement Frontend
---

# Configuration de l'Environnement Frontend

Après avoir configuré le backend, voici les étapes pour mettre en place l'environnement de développement du frontend de l'Assistant RAG Fiqh. Le frontend est développé avec React et Vite, et son code source se trouve dans `Code_Source/frontend/`.

## Étapes de Configuration

1.  **Naviguer vers le Dossier Frontend**:
    * Depuis la racine de votre projet cloné, déplacez-vous dans le répertoire du frontend :
    ```bash
    cd <NOM_DU_DOSSIER_PROJET>/Code_Source/frontend
    ```

2.  **Installer les Dépendances Node.js**:
    * Les dépendances du projet frontend sont listées dans le fichier `package.json`.
    * Utilisez `npm` (ou `yarn` si vous l'avez utilisé pour initialiser le projet ou si un `yarn.lock` est présent) pour installer ces dépendances :
        * Avec npm :
          ```bash
          npm install
          ```
        * Ou avec Yarn :
          ```bash
          yarn install
          ```
    * Cela téléchargera et installera toutes les bibliothèques nécessaires (React, React Router, Tailwind CSS, etc.) dans un dossier `node_modules` à l'intérieur de `Code_Source/frontend/`.

3.  **Configuration de l'URL du Backend (Proxy Vite)**:
    * Le frontend a besoin de communiquer avec le backend. Pour faciliter cela en développement et éviter les problèmes de CORS, un proxy est configuré dans Vite.
    * Ouvrez le fichier `Code_Source/frontend/vite.config.js`.
    * Vérifiez la section `server.proxy` :
    ```javascript
    // Extrait de Code_Source/frontend/vite.config.js
    export default defineConfig({
      // ... autres configurations ...
      server: {
        port: 3000, // Port sur lequel le serveur de dev frontend tournera
        proxy: {
          // Les requêtes du frontend vers /api/v1/auth (ou tout autre chemin d'API)
          // seront redirigées vers le backend tournant sur localhost:8000
          '/api/v1': { // Ajustez ce préfixe si vos appels API backend sont différents
            target: 'http://localhost:8000', // URL de votre backend FastAPI
            changeOrigin: true, // Nécessaire pour les hôtes virtuels
            // secure: false, // Décommentez si votre backend utilise HTTPS avec un certificat auto-signé en dev
          },
        },
      }
    })
    ```
    * **`port: 3000`**: Le serveur de développement Vite pour le frontend tournera sur `http://localhost:3000`.
    * **`proxy`**:
        * Les requêtes du frontend commençant par `/api/v1` (par exemple, `/api/v1/auth/login`) seront automatiquement redirigées par Vite vers `http://localhost:8000/api/v1/...`.
        * Assurez-vous que `target: 'http://localhost:8000'` correspond bien à l'URL et au port où votre backend FastAPI est en cours d'exécution.
        * `changeOrigin: true` est important pour que le backend reçoive les requêtes comme si elles provenaient de la même origine.
    * Dans votre code frontend (par exemple, dans `src/utils/fetchWithAuth.js` ou les actions de React Router), les appels API doivent être faits vers des chemins relatifs commençant par le préfixe du proxy (par exemple, `/api/v1/auth/me`) pour que le proxy Vite les intercepte. La constante `API_BASE_URL` dans `fetchWithAuth.js` est définie à `http://localhost:8000`, ce qui signifie que les appels sont directs et le proxy Vite n'est pas utilisé pour ces appels spécifiques. Si vous souhaitez utiliser le proxy Vite, `API_BASE_URL` devrait être une chaîne vide ou `/` et les appels devraient être faits à `/api/v1/...`. Cependant, votre configuration actuelle de `fetchWithAuth` avec `API_BASE_URL = "http://localhost:8000"` et le `CORSMiddleware` du backend devraient fonctionner correctement ensemble sans nécessiter que les appels passent par le proxy Vite. Le proxy Vite est plus une commodité pour certains setups ou pour éviter des configurations CORS complexes.

4.  **Variables d'Environnement Frontend (Optionnel)**:
    * Si votre frontend utilise des variables d'environnement (par exemple, pour une clé API publique pour un service tiers, ou pour configurer l'URL de base de l'API si elle n'est pas gérée par le proxy), celles-ci seraient généralement dans un fichier `.env` à la racine de `Code_Source/frontend/`.
    * Les variables d'environnement accessibles par Vite doivent être préfixées par `VITE_` (par exemple, `VITE_API_BASE_URL`).
    * D'après votre structure actuelle, `API_BASE_URL` est codée en dur dans `UserContext.jsx` et `fetchWithAuth.js`, donc cette étape n'est peut-être pas immédiatement nécessaire à moins que vous ne souhaitiez la rendre configurable.

5.  **Lancer le Serveur de Développement Frontend**:
    * Une fois les dépendances installées et la configuration vérifiée, vous pouvez lancer le serveur de développement Vite.
    * Depuis la racine du dossier `Code_Source/frontend/` :
        * Avec npm :
          ```bash
          npm run dev
          ```
        * Ou avec Yarn :
          ```bash
          yarn dev
          ```
    * Cela démarrera le serveur de développement frontend, généralement accessible à `http://localhost:3000` (ou le port spécifié dans `vite.config.js`).
    * Le serveur se rechargera automatiquement lorsque vous apporterez des modifications aux fichiers sources du frontend.

Votre frontend devrait maintenant être en mesure de communiquer avec le backend (qui doit être en cours d'exécution sur `http://localhost:8000`). Vous pouvez ouvrir `http://localhost:3000` dans votre navigateur pour accéder à l'application.

---

Avec le backend et le frontend configurés pour le développement local, nous aborderons ensuite la configuration des [Services Externes (PostgreSQL, Redis)](./external-services.md) s'ils ne sont pas gérés via Docker.