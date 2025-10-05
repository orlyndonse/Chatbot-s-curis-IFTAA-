---
sidebar_position: 4
title: Le Panneau Context Hub
---

# Le Panneau Context Hub

L'Assistant RAG Fiqh vous donne accès à une collection de documents relatifs au Fiqh Maliki qui vous ont été assignés par l'administrateur. Le **Panneau Context Hub** (Context Hub Panel) est l'interface dédiée à la gestion et à la sélection de ces documents. Il s'affiche comme un panneau latéral sur la droite de l'écran et est accessible en cliquant sur l'icône "Context Hub" dans la barre d'application supérieure.

![Vue générale du Panneau Context Hub (Conceptuel)](/img/screenshot-document-pane-overview.png)

## Ce que vous trouverez dans ce panneau :

### 1. En-tête du Panneau

* **Titre :** Le titre du panneau est généralement "**Context Hub**". Il peut aussi afficher le nom de la conversation active (par exemple, "Docs: NomDeLaConversation...") pour indiquer à quel contexte les documents sont liés.
* **Bouton de fermeture :** Une icône pour fermer le panneau.

### 2. Zone d'Upload (Pour les Administrateurs)

Si vous avez les privilèges d'administrateur, une zone d'upload des documents s'affiche en haut du panneau, vous permettant d'ajouter de nouveaux documents à la collection.

![Zone d'upload des documents pour administrateurs](/img/screenshot-document-upload-area.png)

### 3. Recherche et Filtres des Documents

* **Champ de recherche :** Une barre de recherche "Rechercher des documents" vous permet de filtrer rapidement les documents par leur nom parmi votre collection personnelle.
* **Options de tri :** Un menu déroulant "Trier par:" offre plusieurs options pour organiser la liste des documents:
    * Date d'ajout (Plus récent d'abord / Plus ancien d'abord)
    * Nom (A-Z / Z-A)
    * Taille (Plus volumineux d'abord / Plus petit d'abord)

    ![Zone de recherche et filtres de documents](/img/screenshot-document-filter-area.png)

### 4. Liste des Documents Assignés et Actions

* **Affichage :** Tous les documents qui vous ont été assignés par l'administrateur sont listés ici sous forme de cartes.
* **Informations par document :** Chaque carte de document affiche:
    * Une **icône** représentant le type de fichier (ex: `picture_as_pdf`, `description`, `article`, `csv`).
    * Le **nom du fichier** (tronqué s'il est trop long, avec le nom complet visible au survol).
    * La **taille du fichier** en Ko.
    * La **date d'ajout** à votre collection.
* **Actions par document :** Des boutons d'icônes permettent d'interagir avec chaque document:
    * **Sélectionner/Désélectionner pour le contexte** : Permet d'inclure ou d'exclure le document de la base de connaissances utilisée par l'IA pour la conversation actuelle. Un document sélectionné est visuellement mis en évidence (par exemple, avec un anneau de couleur).
    * **Aperçu** (icône `visibility`) : Ouvre une modale pour visualiser le contenu du document (si le format est supporté).
    * **Supprimer de la sélection** : Retire le document de la conversation actuelle (mais il reste disponible dans votre collection pour d'autres conversations).

* **Messages contextuels :**
    * Si le chargement des documents est en cours : "Chargement des documents..." avec un indicateur de progression.
    * Si aucun document ne correspond à la recherche : "Aucun document ne correspond à votre recherche pour "terme_recherche".".
    * Si aucun document ne vous a été assigné : "Aucun document disponible. Contactez votre administrateur pour l'assignation de documents.".
    * Si aucune conversation n'est sélectionnée : "Sélectionnez une conversation pour voir ses documents.".

    ![Liste des documents assignés avec détails et actions](/img/screenshot-document-list-items.png)

### 5. Pied de Page du Panneau

* Un résumé indique le nombre de documents actifs par rapport au nombre total de documents disponibles. Par exemple : "X sur Y document(s) actif(s) (affichage de Y sur Z total).".

Ce panneau est essentiel car les documents que vous y sélectionnez définissent la base de connaissances spécifique que l'IA utilisera pour répondre à vos questions dans la conversation en cours. Votre collection personnelle de documents est gérée par l'administrateur qui peut ajouter ou retirer des documents selon vos besoins.

---

**Prochaine étape :** Découvrez [La Barre Supérieure (Top Bar)](./top-bar.md) pour une navigation optimale.