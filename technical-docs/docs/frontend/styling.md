---
sidebar_position: 9
title: Styling (Tailwind CSS et CSS Personnalisé)
---

# Styling (Tailwind CSS et CSS Personnalisé)

L'apparence visuelle du frontend de l'Assistant RAG Fiqh est gérée principalement par [Tailwind CSS](https://tailwindcss.com/), un framework CSS "utility-first", complété par des styles CSS personnalisés pour des ajustements plus spécifiques et la création d'un système de design cohérent.

## Configuration Tailwind CSS

### **Fichier `tailwind.config.js`**
La configuration Tailwind constitue le cœur du système de design de l'application :

#### **Mode Sombre**
```javascript
darkMode: 'class'
```
- Active le mode sombre basé sur une classe `dark` ajoutée à l'élément `<html>`
- La gestion du basculement thématique est orchestrée dans `TopAppBar.jsx`
- Détection automatique des préférences utilisateur avec fallback système

#### **Extension du Thème (`theme.extend`)**
Le thème par défaut de Tailwind est largement étendu pour implémenter un système de design complet inspiré de Material Design 3 :

**Palette de Couleurs Sémantiques :**
- **Modes duels** : Définitions complètes pour les thèmes `light` et `dark`
- **Couleurs principales** : `primary`, `secondary`, `accent` avec leurs variantes
- **Couleurs de surface** : `surface`, `surface-variant`, `background`
- **Couleurs sémantiques** : `success`, `warning`, `error`, `info`
- **Couleurs de contenu** : Variantes automatiques pour chaque couleur de base

**Système d'Espacement Personnalisé :**
- Échelle étendue pour un contrôle précis des marges et paddings
- Valeurs supplémentaires pour les composants spécialisés
- Cohérence avec les principes de design system

**Ombres et Élévations (`boxShadow`) :**
- Système d'ombres à 5 niveaux pour la hiérarchie visuelle
- Adaptation automatique aux thèmes clair/sombre
- Ombres spécialisées pour les composants interactifs

**Rayons de Bordure (`borderRadius`) :**
- Gamme étendue de rayons pour différents types de composants
- Cohérence avec les standards Material Design
- Valeurs spécialisées pour les éléments de navigation

**Typographie Personnalisée :**
- Échelles de tailles harmonieuses
- Hauteurs de ligne optimisées pour la lisibilité
- Poids de police contextuels

**Transitions et Animations :**
- Durées standardisées pour les micro-interactions
- Courbes d'animation personnalisées
- Cohérence temporelle à travers l'interface

#### **Plugins**
```javascript
plugins: []
```
- **Approche minimaliste** : Aucune dépendance externe comme DaisyUI
- **Contrôle total** : Implémentation personnalisée via `@apply` et classes utilitaires
- **Performance optimisée** : CSS généré uniquement pour les classes utilisées

### **Intégration PostCSS (`postcss.config.js`)**
Configuration pour le traitement CSS avancé :
- **`tailwindcss`** : Plugin principal pour la génération CSS
- **`autoprefixer`** : Ajout automatique des préfixes vendeurs (-webkit-, -moz-, etc.)
- **Compatibilité navigateurs** : Support étendu selon les spécifications du projet

## Styles CSS Globaux et Architecture

### **Point d'Entrée (`src/index.css`)**
Le fichier `src/index.css` orchestre l'ensemble du système de styles :

#### **Directives Tailwind**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```
- **Base** : Reset CSS et styles fondamentaux
- **Components** : Classes de composants personnalisés définis via `@layer`
- **Utilities** : Classes utilitaires générées par Tailwind

#### **Système de Composants Personnalisés (`@layer components`)**
Définition extensive de classes de composants via la directive `@apply` :

**Composants de Base :**
- **`.btn`** : Système de boutons avec variantes (filled, outlined, text)
- **`.text-field`** : Champs de texte avec labels flottants et états
- **`.card`** : Conteneurs avec élévations et rayons cohérents

**Composants de Navigation :**
- **`.sidebar`** : Styles pour la barre latérale avec transitions fluides
- **`.top-app-bar`** : Barre de navigation supérieure responsive
- **`.menu`** : Système de menus déroulants avec positionnement intelligent

**Composants de Feedback :**
- **`.snackbar`** : Notifications toast avec animations et couleurs sémantiques
- **`.progress`** : Indicateurs de progression circulaires et linéaires
- **`.loading`** : États de chargement avec animations

**Composants Spécialisés :**
- **`.document-card`** : Cartes de documents avec actions et états
- **`.context-hub`** : Styles pour le panneau de gestion documentaire
- **`.upload-area`** : Zone de téléversement avec états interactifs

### **Polices et Typographie**
- **Police principale** : 'DM Sans' importée dans `index.html`
- **Hiérarchie typographique** : Classes personnalisées pour titres, corps et métadonnées
- **Lisibilité optimisée** : Contraste et espacement ajustés selon les standards d'accessibilité

### **Personnalisations Avancées**
- **Barres de défilement** : Styles personnalisés pour les navigateurs WebKit
- **États de focus** : Indicateurs visuels cohérents pour l'accessibilité clavier
- **Animations micro** : Transitions subtiles pour améliorer l'expérience utilisateur
- **Responsive breakpoints** : Adaptations spécifiques pour mobile, tablette et desktop

## Méthodologie d'Application des Styles

### **Classes Utilitaires (Approche Principale)**
La majorité du styling utilise les classes Tailwind et personnalisées directement dans le JSX :
```jsx
<button className="btn btn-primary hover:btn-primary-hover transition-colors">
  Action
</button>
```

### **Avantages de cette Approche :**
- **Performance** : CSS minimal généré uniquement pour les classes utilisées
- **Cohérence** : Système de design centralisé dans la configuration
- **Maintenabilité** : Changements visuels via modification de la configuration
- **Développement rapide** : Pas de CSS séparé à maintenir pour chaque composant

### **CSS Modules (Usage Minimal)**
Réservé aux cas spéciaux nécessitant des styles dynamiques ou des calculs CSS complexes :
- Animations personnalisées complexes
- Styles basés sur des propriétés JavaScript
- Intégrations de bibliothèques tierces

### **Styles Inline (Usage Exceptionnel)**
Utilisés uniquement pour :
- Styles dynamiques basés sur l'état des composants
- Valeurs calculées en JavaScript
- Propriétés CSS non couvertes par Tailwind

## Gestion des Thèmes

### **Basculement Clair/Sombre**
- **Déclenchement** : Via le `TopAppBar.jsx` avec persistance des préférences
- **Implémentation** : Classe `dark` sur l'élément racine `<html>`
- **Cascade** : Toutes les couleurs définies s'adaptent automatiquement

### **Personnalisation Thématique**
- **Variables CSS** : Utilisation de propriétés personnalisées pour la flexibilité
- **Adaptation contextuelle** : Couleurs et contrastes optimisés par contexte
- **Accessibilité** : Respect des standards WCAG pour les contrastes

## Performance et Optimisation

### **Tree Shaking CSS**
- **Analyse statique** : Seules les classes utilisées sont incluses dans le build final
- **Optimisation automatique** : Purge des styles inutilisés en production
- **Bundle minimal** : CSS final optimisé pour les performances

### **Stratégies de Cache**
- **CSS critique** : Styles essentiels inline dans le HTML
- **Lazy loading** : Chargement différé des styles non critiques
- **Compression** : Minification et compression gzip/brotli

Cette architecture de styling robuste permet de maintenir une interface utilisateur cohérente, performante et facilement évolutive, tout en offrant la flexibilité nécessaire pour les personnalisations futures et l'adaptation aux besoins spécifiques du domaine de la jurisprudence islamique.

---

Le système de styling s'intègre parfaitement avec les [Composants UI réutilisables](./ui-components.md) et s'appuie sur les [Dépendances frontend optimisées](./dependencies.md) pour une expérience de développement fluide.

---

Après avoir vu le styling, nous allons documenter les [Dépendances Clés du Frontend](./dependencies.md) listées dans `package.json`.