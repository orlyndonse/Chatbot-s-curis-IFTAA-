---
sidebar_position: 4
title: Le Panneau Context Hub
---

# Le Panneau Context Hub

L'Assistant RAG Fiqh vous permet de téléverser (uploader) des documents qui serviront de base de connaissances à l'intelligence artificielle (IA) pour répondre à vos questions. Le **Panneau Context Hub** (Context Hub Panel) est l'interface dédiée à la gestion de ces documents. Il s'affiche comme un panneau latéral sur la droite de l'écran et est accessible en cliquant sur l'icône "topic" (ou une icône similaire de gestion de documents) dans la barre d'application supérieure.

![Vue générale du Panneau Context Hub (Conceptuel)](/img/screenshot-document-pane-overview.png)

## Ce que vous trouverez dans ce panneau :

### 1. En-tête du Panneau

* **Titre :** Le titre du panneau est généralement "**Context Hub**". Il peut aussi afficher le nom de la conversation active (par exemple, "Docs: NomDeLaConversation...") pour indiquer à quel contexte les documents sont liés.
* **Bouton de fermeture :** Une icône pour fermer le panneau.

### 2. Indicateur de Taille du Contexte

* **Affichage :** Vous verrez une barre de progression et un texte indiquant la "Taille du contexte" (Context Size). Ce texte ressemblera à quelque chose comme : "**Context Size : _X_KB / _Y_KB**" (par exemple, "Context Size : 15.0KB / 5120.0KB").
    * La première valeur (_X_ KB) indique la taille cumulée des documents actuellement actifs dans le contexte.
    * La seconde valeur (_Y_ KB) indique la taille maximale autorisée pour le contexte de la conversation.
* **Couleurs de la barre :** La couleur de la barre de progression change (vert, jaune, rouge) pour indiquer l'imminence de l'atteinte de la limite.
* **Utilité :** Cet indicateur vous aide à gérer la quantité d'informations fournies à l'IA pour la conversation active, en respectant les limites du système.

    ![Indicateur de Taille du Contexte](/img/screenshot-document-context-size.png) 

### 3. Zone de Téléversement (Upload)

* **Fonction :** C'est ici que vous pouvez ajouter de nouveaux documents à la conversation active. Cette zone est désactivée si aucune conversation n'est active ou pendant un téléversement.
* **Méthodes :**
    * **Glisser-déposer (Drag-and-drop) :** Vous pouvez faire glisser des fichiers depuis votre ordinateur directement sur cette zone.
    * **Bouton "Browse Files" :** En cliquant sur ce bouton, une fenêtre de sélection de fichiers s'ouvrira pour que vous puissiez choisir les documents à téléverser.
* **Pendant le téléversement :** Un indicateur de progression circulaire et le message "Processing files..." s'affichent.
* **Formats Supportés :** Un message indique les types de fichiers acceptés (par défaut : .pdf, .txt, .docx, .csv, .html).

    ![Zone de Téléversement](/img/screenshot-document-upload-area.png)

### 4. Filtres des Documents

* **Condition d'affichage :** Cette section apparaît s'il y a des documents dans la conversation active.
* **Champ de recherche :** Une barre de recherche "Search documents by name..." vous permet de filtrer rapidement les documents par leur nom.
* **Options de tri :** Un menu déroulant "Sort by:" offre plusieurs options pour organiser la liste des documents:
    * Date Added (Newest First / Oldest First)
    * Name (A-Z / Z-A)
    * Size (Largest First / Smallest First)

    ![Zone de téléversement de documents (glisser-déposer)](/img/screenshot-document-filter-area.png)

### 5. Liste des Documents et Actions

* **Affichage :** Les documents téléversés et filtrés pour la conversation active sont listés ici sous forme de cartes.
* **Informations par document :** Chaque carte de document affiche:
    * Une **icône** représentant le type de fichier (ex: `picture_as_pdf`, `description`, `article`, `csv`).
    * Le **nom du fichier** (tronqué s'il est trop long, avec le nom complet visible au survol).
    * La **taille du fichier** en Ko.
    * La **date de téléversement**.
* **Actions par document :** Des boutons d'icônes permettent d'interagir avec chaque document:
    * **Activer/Désactiver dans le contexte** : Permet d'inclure ou d'exclure le document de la base de connaissances utilisée par l'IA pour la réponse actuelle, sans le supprimer. Un document actif est visuellement mis en évidence (par exemple, avec un anneau de couleur).
    * **Aperçu** (icône `visibility`) : Ouvre une modale pour visualiser le contenu du document (si le format est supporté).
    * **Supprimer** (icône `delete`) : Retire définitivement le document de la conversation. Un indicateur de chargement s'affiche pendant la suppression.
* **Messages contextuels :**
    * Si le chargement des documents est en cours : "Loading documents..." avec un indicateur de progression.
    * Si aucun document ne correspond à la recherche : "No documents match your search for "terme_recherche".".
    * Si la conversation est active mais ne contient aucun document : "No documents in this conversation yet. Drag and drop or browse to upload.".
    * Si aucune conversation n'est sélectionnée : "Select a conversation to view its documents.".

    ![Liste des documents chargés avec détails et actions](/img/screenshot-document-list-items.png)

### 6. Pied de Page du Panneau

* Un résumé indique le nombre de documents actifs par rapport au nombre total de documents filtrés et au nombre total de documents dans la conversation. Par exemple : "X of Y document(s) active (showing Y from Z total).".

Ce panneau est essentiel car les documents que vous y gérez et activez définissent la base de connaissances spécifique que l'IA utilisera pour répondre à vos questions dans la conversation en cours.

---

**Prochaine étape :** Découvrez [La Barre Supérieure (Top Bar)](./top-bar.md) pour une navigation optimale.