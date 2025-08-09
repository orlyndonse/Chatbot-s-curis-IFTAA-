---
sidebar_position: 2
title: Configuration et Build (Vite)
---

# Configuration et Processus de Build du Frontend (Vite)

Le frontend de l'Assistant RAG Fiqh est construit et servi en développement à l'aide de [Vite](https://vitejs.dev/), un outil de build moderne qui offre un serveur de développement rapide et un processus de build optimisé pour la production. La configuration principale se trouve dans `vite.config.js`.

## Fichier de Configuration `vite.config.js`

Le fichier `vite.config.js` à la racine du projet frontend (`Code_Source/frontend/`) contrôle le comportement de Vite.

```javascript
// Extrait de Code_Source/frontend/vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc' // Utilise SWC pour une compilation React plus rapide

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()], // Plugin React pour Vite
  server: {
    port: 3000,       // Port pour le serveur de développement
    proxy: {
      // Configuration du proxy pour les appels API vers le backend
      '/api/v1': {
        target: 'http://localhost:8000', // URL du backend FastAPI
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist', // Répertoire de sortie pour les fichiers de production
  },
})
```

### Détails de la configuration

#### `plugins: [react()]`
- Utilise `@vitejs/plugin-react-swc`. Ce plugin permet à Vite de comprendre et de compiler le code JSX de React
- SWC (Speedy Web Compiler) est utilisé à la place de Babel pour une compilation plus rapide en développement et en production

#### `server.port: 3000`
- Définit le port sur lequel le serveur de développement Vite écoutera
- L'application frontend sera donc accessible à `http://localhost:3000` en mode développement

#### `server.proxy`
- Configure un proxy pour les requêtes API. Ceci est utile en développement pour éviter les problèmes de CORS (Cross-Origin Resource Sharing) lorsque le frontend (sur localhost:3000) appelle le backend (sur localhost:8000)
- Les requêtes du frontend dont le chemin commence par `/api/v1` seront automatiquement redirigées par le serveur de développement Vite vers `http://localhost:8000/api/v1/...`
- `changeOrigin: true` est important pour que le serveur backend reçoive les requêtes comme si elles provenaient de la même origine

> **Note**: La configuration actuelle de `fetchWithAuth.js` utilise une URL de base absolue pour l'API (`http://localhost:8000`), ce qui signifie que le proxy Vite n'est pas directement utilisé par ces appels. Le proxy reste utile si des appels relatifs étaient faits ou pour d'autres configurations. Le CORSMiddleware du backend gère les requêtes cross-origin pour les appels directs.

#### `build.outDir: 'dist'`
- Spécifie que les fichiers générés lors du build de production seront placés dans un répertoire nommé `dist` à la racine du projet frontend

## Serveur de Développement

### Commande de démarrage
```bash
npm run dev
# ou
yarn dev
```

### Fonctionnalités
- Lorsque vous exécutez `npm run dev` (ou `yarn dev`), Vite démarre un serveur de développement local
- Ce serveur utilise le HMR (Hot Module Replacement) pour des mises à jour quasi instantanées dans le navigateur lorsque vous modifiez le code source, sans nécessiter un rechargement complet de la page
- Il sert l'application depuis la mémoire et ne génère pas de fichiers dans le dossier `dist`

## Processus de Build pour la Production

### Commande de build
```bash
npm run build
# ou
yarn build
```

### Optimisations effectuées
La commande `npm run build` (ou `yarn build`) déclenche le processus de build de Vite pour la production. Vite effectue plusieurs optimisations :

1. **Compilation**: Compile le code React/JSX en JavaScript standard
2. **Bundling**: Regroupe les modules JavaScript en un nombre réduit de fichiers (bundles) pour optimiser le chargement
3. **Minification**: Réduit la taille des fichiers JavaScript et CSS en supprimant les caractères inutiles
4. **Tree Shaking**: Élimine le code inutilisé des dépendances
5. **Optimisation des Assets**: Traite les assets statiques (images, polices)
6. **Génération de Fichiers Statiques**: Crée les fichiers HTML, CSS, et JavaScript optimisés dans le répertoire spécifié par `build.outDir` (par défaut `dist/`)

### Déploiement
Le contenu du dossier `dist/` est ensuite ce qui est déployé sur un serveur web statique ou une plateforme d'hébergement pour servir l'application frontend en production.

## Avantages de Vite

Vite offre ainsi une expérience de développement fluide et un build optimisé pour des applications React performantes grâce à :

- **Démarrage rapide**: Serveur de développement qui démarre instantanément
- **Hot Module Replacement**: Mises à jour en temps réel sans rechargement de page
- **Build optimisé**: Utilisation d'outils modernes pour des bundles performants
- **Compatibilité ESM**: Support natif des modules ES6
- **Plugin ecosystem**: Large écosystème de plugins disponibles

---

Le point d'entrée de l'application React et le rendu initial sont gérés dans [src/main.jsx](../frontend/entry-point.md).