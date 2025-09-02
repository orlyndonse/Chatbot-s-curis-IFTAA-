---
sidebar_position: 7
title: Composants UI Principaux
---

# Composants UI Principaux (`src/components/`)

Le dossier `src/components/` contient une collection de composants React réutilisables qui constituent les blocs de construction de l'interface utilisateur de l'Assistant RAG Fiqh. Ces composants sont conçus pour être modulaires et sont orchestrés par le composant principal `App.jsx` à travers différentes sections de l'application.

## Composants d'Interface Principaux

### **`Sidebar.jsx`**
Panneau latéral gauche principal de l'application :
- Navigation complète entre les conversations utilisateur
- Interface de création via `ExtendedFab` ("Nouvelle Discussion")
- Fonctionnalités de renommage inline avec champ d'édition
- Actions de suppression avec confirmations et états de chargement
- Intégration du `Logo` et gestion responsive avec overlay mobile
- Coordination étroite avec `App.jsx` pour la gestion des états

### **`TopAppBar.jsx`**
Barre de navigation supérieure centrale :
- Affichage adaptatif du `Logo` (masqué sur desktop, visible sur mobile)
- Contrôles de basculement pour `Sidebar` et `ContextHub`
- Menu utilisateur intégrant `Avatar` et `MenuItem`
- Sélecteurs de thème et langue via `LanguageContext`
- Accès direct à la documentation externe
- Bouton de déconnexion avec gestion des tokens

### **`PromptField.jsx`**
Zone de saisie sophistiquée au cœur de l'interaction :
- Champ multiline avec redimensionnement automatique
- `UploadButton` intégré pour le téléversement de fichiers
- `IconBtn` d'envoi avec gestion des états (envoi/chargement)
- Support des raccourcis clavier (Enter, Shift+Enter)
- Validation et désactivation contextuelle
- Coordination avec `App.jsx` pour l'envoi de messages

### **`DocumentPreview.jsx`**
Modale complète de prévisualisation documentaire :
- Support multi-formats : PDF (iframe), texte brut, images
- Actions d'activation/désactivation du contexte
- Gestion des erreurs de chargement et des types non supportés
- Interface responsive avec `Button` et `IconBtn`
- Fermeture par overlay ou bouton explicite

## Composants de Base Réutilisables

### **`Avatar.jsx`**
Affiche un avatar utilisateur avec génération dynamique :
- Première lettre stylisée du nom utilisateur
- Couleur de fond générée par hash du nom pour consistance
- Style circulaire avec typographie cohérente
- Utilisé dans `TopAppBar` et potentiellement `Sidebar`

### **`Button.jsx`**
Composant polyvalent exportant plusieurs types de boutons :
- **`Button`** : Bouton principal avec variantes (`filled`, `outlined`, `text`)
- **`IconBtn`** : Bouton rond utilisant le composant `Icon`
- **`ExtendedFab`** : Floating Action Button avec `Icon` et texte
- **`UploadButton`** : Bouton spécialisé encapsulant une entrée de fichier
- Support des états désactivé et chargement avec `CircularProgress`
- Gestion des couleurs thématiques et animations Framer Motion

### **`Icon.jsx`**
Composant central pour le système d'icônes :
- Chargement dynamique d'icônes SVG locales via `useIcon` hook
- Fallback vers Material Symbols pour les icônes manquantes
- Stylisation flexible (taille, couleur, className)
- Optimisation des performances et gestion d'erreurs
- Utilisé massivement par `IconBtn`, `MenuItem`, `Sidebar`

### **`Logo.jsx`**
Composant logo avec adaptation thématique :
- Basculement automatique entre versions claire/sombre
- Intégration avec React Router (`Link` vers accueil)
- Dimensionnement responsive et cohérent
- Utilisé dans `Sidebar` et `TopAppBar`

### **`Menu.jsx` et `MenuItem.jsx`**
Système de menus modulaire :
- **`Menu`** : Conteneur avec gestion de positionnement et visibilité
- **`MenuItem`** : Élément cliquable avec `Icon` et actions personnalisées
- Support des actions destructives (suppression)
- Utilisés dans `TopAppBar` pour le menu utilisateur et `Sidebar` pour les actions de conversation

### **`Progress.jsx`**
Indicateurs de progression pour les états de chargement :
- **`CircularProgress`** : Utilisé dans `Sidebar`, `DocumentPreview`, `Button`
- **`LinearProgress`** : Pour les processus longs avec animations Framer Motion
- Variantes de taille (small, medium, large)
- Intégration thématique cohérente

### **`Snackbar.jsx`**
Système de notifications toast :
- Consommation du `SnackbarContext` pour l'état global
- Types différenciés (success, error, info) avec animations
- Positioning fixe en bas d'écran
- Auto-fermeture configurable

### **`TextField.jsx`**
Champ de texte pour les formulaires d'authentification :
- Label et helper text intégrés
- Validation et messages d'erreur
- Styling cohérent avec le design system
- Utilisé dans les pages Login, Register, etc.

### **`ToggleIcons.jsx`**
Collection d'icônes SVG spécialisées :
- **`ToggleOnIcon`** et **`ToggleOffIcon`** : États de basculement
- **`ProgressActivityIcon`** : Spinner personnalisé
- Composants autonomes sans dépendances externes
- Styling modulaire et réutilisable

## Composants Spécifiques au ContextHub (`src/components/contextHub/`)

### **`ContextHubPanel.jsx`**
Panneau latéral droit pour la gestion documentaire :
- Orchestration complète des composants de gestion de documents
- États d'ouverture/fermeture synchronisés avec `App.jsx`
- Interface responsive avec glissement et overlay
- Intégration de tous les sous-composants du ContextHub

### **`ContextSizeIndicator.jsx`**
Indicateur visuel intelligent de l'utilisation du contexte :
- Barre de progression proportionnelle avec `Progress` components
- Seuils visuels pour les limites de contexte
- Métriques en temps réel (taille actuelle/maximale)
- Alertes de dépassement avec codes couleur

### **`DocumentFilters.jsx`**
Interface de recherche et filtrage documentaire :
- Champ de recherche en temps réel via `TextField`
- Menu déroulant de tri utilisant `Menu` et `MenuItem`
- Filtres par type de document
- Compteurs de résultats dynamiques

### **`DocumentItemCard.jsx`**
Carte d'affichage individuel optimisée :
- Métadonnées complètes avec formatage intelligent
- Boutons d'action utilisant `IconBtn` : activation, prévisualisation, suppression
- États visuels distincts (actif/inactif) avec `ToggleIcons`
- Prévisualisation miniature pour les images
- Gestion des erreurs et états de chargement

### **`DocumentUploadArea.jsx`**
Zone de téléversement sophistiquée :
- Interface glisser-déposer intuitive avec `react-dropzone`
- Support multi-fichiers avec validation des types
- Indicateurs de progression utilisant `CircularProgress`
- Messages d'erreur contextuels via `Snackbar`
- États visuels pour les zones de drop actives

## Composants Spécialisés pour le Streaming

### **`StreamingMarkdown.jsx`**
Composant avancé pour l'affichage de contenu Markdown avec streaming :
- Rendu progressif en temps réel du contenu streamé
- Support complet RTL pour l'arabe avec classes CSS adaptatives
- Gestion des états de chargement et d'erreur
- Intégration avec `react-markdown` et `remark-gfm`
- Animations fluides pour l'apparition du contenu

### **`LogsPanel.jsx`**
Panneau de débogage pour le développement :
- Affichage en temps réel des logs de streaming et d'API
- Interface de filtrage et de recherche dans les logs
- Niveaux de log différenciés (info, warning, error)
- Outils d'export et de nettoyage des logs

## Architecture et Intégration

Ces composants forment un écosystème cohérent où :

### **Coordination Centrale via App.jsx**
- `App.jsx` orchestre les interactions entre `Sidebar`, `PromptField`, `ContextHub`, et `TopAppBar`
- États partagés gérés centralement et propagés via props
- Communication bidirectionnelle via callbacks pour les actions utilisateur

### **Système d'Icônes Unifié**
- `Icon.jsx` centralise le chargement des icônes SVG locales
- Fallback intelligent vers Material Symbols
- Utilisation cohérente dans `IconBtn`, `MenuItem`, `Sidebar`

### **Gestion d'État Coordonnée**
- `Progress` components intégrés dans les opérations asynchrones
- `Snackbar` pour les notifications globales
- États de chargement propagés entre composants

### **Responsivité et Accessibilité**
- Adaptation automatique mobile/desktop
- Support RTL complet via `LanguageContext`
- Gestion des overlays et interactions tactiles

La communication avec le backend est gérée de manière centralisée via les utilitaires dans `src/utils/`, particulièrement `fetchWithAuth.js` pour les appels API authentifiés, permettant une architecture claire entre présentation et logique métier.

---

Ces composants UI s'intègrent harmonieusement avec le système de [Contextes React](../frontend/state-management.md) et communiquent avec le serveur via les [appels API sécurisés](./api-communication.md).