---
sidebar_position: 10 # Ajustez si nécessaire, mais 10 semble correct après styling
title: Dépendances Clés du Frontend
---

# Dépendances Clés du Frontend (`package.json`)

Le fichier `package.json` à la racine du projet frontend (`Code_Source/frontend/`) liste toutes les bibliothèques et outils JavaScript nécessaires au développement, au build et au fonctionnement de l'application React. Voici une description des dépendances les plus importantes :

## Dépendances de Production (`dependencies`)

Ces bibliothèques sont incluses dans le build final de l'application et sont nécessaires à son exécution dans le navigateur de l'utilisateur.

* **`react`**: La bibliothèque principale pour construire l'interface utilisateur avec des composants.
* **`react-dom`**: Fournit les méthodes spécifiques au DOM pour React (par exemple, `ReactDOM.createRoot`).
* **`react-router-dom`**: Utilisée pour gérer la navigation et le routage côté client dans l'application.
* **`prop-types`**: Utilisé pour la validation des types des props passées aux composants React, ce qui aide à la détection précoce des erreurs et à la documentation des composants.
* **`react-dropzone`**: Une bibliothèque React pour créer facilement une zone de glisser-déposer (drag'n'drop) pour les fichiers. Utilisée dans `DocumentUploadArea.jsx` pour une expérience de téléversement de fichiers améliorée.
* **`react-helmet`**: Un composant réutilisable pour gérer les modifications du `head` du document HTML (par exemple, pour définir dynamiquement le titre de la page).
* **`motion`**: (Semble être `framer-motion` basé sur l'usage commun, ou une autre bibliothèque d'animation nommée "motion"). Utilisée pour créer des animations fluides et des transitions dans l'interface utilisateur.
* **`@google/generative-ai`**: Bibliothèque client JavaScript pour interagir avec l'API Google Generative AI. Bien que la logique RAG principale soit côté backend, cette dépendance pourrait être utilisée pour des fonctionnalités côté client ou des expérimentations futures. (Note: son usage direct dans le code frontend actuel n'est pas immédiatement apparent dans les composants principaux, le backend gérant les appels LLM.)

## Dépendances de Développement (`devDependencies`)

Ces outils et bibliothèques sont utilisés uniquement pendant le processus de développement et de build, et ne sont pas inclus dans le bundle de production final.

* **`@types/react`**, **`@types/react-dom`**: Fournissent les définitions de types TypeScript pour React et ReactDOM (utile même dans un projet JavaScript pour une meilleure autocomplétion dans les IDEs).
* **`@vitejs/plugin-react`**: Le plugin Vite qui utilise SWC par défaut (ou Babel en option) pour compiler le code React. (Note: `vite.config.js` mentionne `@vitejs/plugin-react-swc`, tandis que `package.json` liste `@vitejs/plugin-react`. La version avec SWC est souvent préférée pour la vitesse.)
* **`autoprefixer`**: Un plugin PostCSS qui ajoute automatiquement les préfixes vendeurs aux règles CSS pour une meilleure compatibilité entre navigateurs.
* **`eslint`**, **`@eslint/js`**, **`eslint-plugin-react-hooks`**, **`eslint-plugin-react-refresh`**:
    * Outils pour le linting du code JavaScript/JSX. ESLint aide à identifier et à corriger les problèmes de style de code, les erreurs potentielles, et à faire respecter les bonnes pratiques. (Note: `eslint.config.js` est le fichier de configuration moderne d'ESLint).
* **`globals`**: Fournit des informations sur les variables globales prédéfinies dans différents environnements (par exemple, navigateur, Node.js) pour ESLint.
* **`postcss`**: Un outil pour transformer les styles CSS avec des plugins JavaScript. Utilisé par Tailwind CSS.
* **`prettier`**: Un formateur de code automatique qui assure un style de code cohérent à travers le projet.
* **`tailwindcss`**: Le framework CSS utility-first utilisé pour le styling principal de l'application. (Note: l'utilisation de DaisyUI comme plugin Tailwind n'est pas listée dans le `package.json` fourni. Si DaisyUI est utilisé comme décrit dans `tailwind.config.js`, il devrait être une `devDependency`).
* **`vite`**: L'outil de build et le serveur de développement utilisé pour le projet frontend.

La gestion de ces dépendances via `package.json` et `npm` (ou `yarn`) assure que l'environnement de développement est reproductible et que le build de production contient uniquement le code nécessaire.

---

Nous avons maintenant couvert l'ensemble des aspects importants du frontend. La prochaine section de la documentation technique concerne la [Documentation Utilisateur](./../user-documentation/overview.md) et comment elle est structurée.