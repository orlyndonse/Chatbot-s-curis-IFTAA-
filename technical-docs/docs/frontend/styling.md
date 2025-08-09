---
sidebar_position: 9
title: Styling (Tailwind CSS et CSS Personnalisé)
---

# Styling (Tailwind CSS et CSS Personnalisé)

L'apparence visuelle du frontend de l'Assistant RAG Fiqh est gérée principalement par [Tailwind CSS](https://tailwindcss.com/), un framework CSS "utility-first", complété par des styles CSS personnalisés pour des ajustements plus spécifiques ou globaux.

## Tailwind CSS

Tailwind CSS est l'outil principal pour le stylisme des composants React. Il permet d'appliquer des styles directement dans le JSX en utilisant des classes utilitaires prédéfinies, ce qui accélère le développement et maintient la cohérence visuelle.

* **Configuration (`tailwind.config.js`)**:
    * Le fichier `Code_Source/frontend/tailwind.config.js` configure Tailwind CSS pour le projet.
    * **`content`**: Spécifie les fichiers que Tailwind doit analyser pour y trouver les classes utilitaires utilisées (par exemple, tous les fichiers `.html`, `.js`, `.jsx` dans `src/` et `index.html`). Cela permet à Tailwind de générer uniquement le CSS nécessaire en production (tree-shaking).
    * **`theme.extend`**: Permet d'étendre ou de surcharger le thème par défaut de Tailwind. Dans ce projet, des couleurs personnalisées sont définies pour correspondre à la charte graphique de l'application :
        * `primary`, `secondary`, `accent`, `neutral`, `base-100`, `info`, `success`, `warning`, `error`. Ces couleurs sont utilisées pour les arrière-plans, les textes, les bordures, etc. (par exemple, `bg-primary`, `text-secondary-content`).
    * **`darkMode: "class"`**: Active le mode sombre basé sur une classe (`dark`) ajoutée à l'élément `<html>`. Le changement de thème (clair/sombre) est géré par le hook `useColorMode` de Docusaurus pour la documentation, et une logique similaire pourrait être implémentée ou est gérée par le navigateur/OS pour l'application React elle-même.
    * **`plugins: [require('daisyui')]`**:
        * Utilise le plugin [DaisyUI](https://daisyui.com/) pour Tailwind CSS.
        * DaisyUI ajoute des classes pour des composants d'interface utilisateur pré-stylisés (comme les boutons, cartes, modales, etc.) qui peuvent être utilisés par-dessus les utilitaires de Tailwind, tout en restant hautement personnalisables.
        * La configuration `daisyui.themes` spécifie les thèmes personnalisés "lightTheme" et "darkTheme" qui utilisent les couleurs définies dans `theme.extend.colors`.

* **Intégration avec PostCSS (`postcss.config.js`)**:
    * Le fichier `Code_Source/frontend/postcss.config.js` configure PostCSS, un outil pour transformer le CSS avec des plugins JavaScript.
    * Il inclut `tailwindcss` et `autoprefixer` comme plugins. `autoprefixer` ajoute automatiquement les préfixes vendeurs (par exemple, `-webkit-`, `-moz-`) aux règles CSS pour assurer la compatibilité entre les navigateurs.

## Styles CSS Globaux et Personnalisés (`src/index.css`)

* Le fichier `Code_Source/frontend/src/index.css` est le point d'entrée principal pour les styles CSS.
* **Directives Tailwind**:
    * Il inclut les directives `@tailwind base;`, `@tailwind components;`, et `@tailwind utilities;`. Ces directives injectent les styles de base de Tailwind, les classes de composants (principalement de DaisyUI ici), et les classes utilitaires.
* **Styles Globaux Personnalisés**:
    * Des styles globaux peuvent être ajoutés dans ce fichier pour des éléments qui ne sont pas facilement ciblés par des classes utilitaires ou pour définir des styles de base pour l'ensemble de l'application.
    * Exemple de styles personnalisés présents :
        * Application d'une police personnalisée (`'DM Sans', sans-serif`) au `body`. La police `DM Sans` est importée dans `index.html`.
        * Styles pour la barre de défilement (scrollbar) pour la personnaliser sur les navigateurs basés sur WebKit.
        * Styles spécifiques pour les avatars de message (`.message-avatar`), les bulles de message (`.message-bubble`), les indicateurs de frappe, etc.
        * Ajustements pour les éléments de formulaire comme les inputs et les textareas pour correspondre au design.
        * Styles pour le `Toastify__toast-container` et `Toastify__toast`, suggérant l'utilisation (ou l'intention d'utiliser) `react-toastify` pour les notifications, bien que `SnackbarContext` soit également implémenté.

## Application des Styles

* **Classes Utilitaires**: La majorité du styling est appliquée en ajoutant des classes Tailwind (et DaisyUI) directement aux éléments JSX dans les composants React.
    * Exemple : `<button className="btn btn-primary">Mon Bouton</button>`
* **CSS Modules (Non utilisé de manière prédominante)**: Bien que Vite supporte les CSS Modules (`.module.css`), cette approche n'est pas la principale méthode de styling observée, au profit de Tailwind CSS.
* **Styles en ligne (Inline Styles)**: Utilisés avec parcimonie, généralement pour des styles dynamiques basés sur l'état du composant qui ne sont pas facilement gérables par des classes.

Cette approche combinant la puissance de Tailwind CSS/DaisyUI pour un développement rapide et la flexibilité du CSS personnalisé pour les ajustements fins permet de créer une interface utilisateur cohérente et esthétique.

---

Après avoir vu le styling, nous allons documenter les [Dépendances Clés du Frontend](./dependencies.md) listées dans `package.json`.