---
sidebar_position: 4
title: Prévisualiser le Contenu des Documents
---

# Prévisualiser le Contenu des Documents Téléversés

Après avoir [téléversé vos documents](./how-to-upload.md) et les avoir vus listés dans le [Panneau de Gestion des Documents](../interface-overview/document-management-pane.md), vous pourriez vouloir vérifier rapidement leur contenu sans avoir à les ouvrir dans une application externe. L'Assistant RAG Fiqh offre une fonction d'aperçu pour cela.

## Comment Accéder à l'Aperçu d'un Document ?

1.  Dans la [Liste des Documents Chargés](../interface-overview/document-management-pane.md#3-liste-des-documents-chargés-documents-chargés-point-341), localisez le document dont vous souhaitez voir un aperçu.
2.  À droite des informations du document, cliquez sur le bouton "**Aperçu**" (Preview). Il est généralement représenté par une icône en forme d'œil (`visibility`).

    ![Bouton "Aperçu" à côté d'un document dans la liste](/img/screenshot-document-preview-button.png)

## L'Interface d'Aperçu

Après avoir cliqué sur "Aperçu", une fenêtre modale (pop-up) s'ouvrira, affichant le contenu du document si le format est supporté pour l'aperçu.

* **Titre du Document :** Le nom du fichier est généralement affiché en haut de la fenêtre d'aperçu.
* **Indicateur de Chargement :** Si le contenu du document doit être récupéré (comme pour les PDF, les fichiers texte ou les images), un message "Chargement de l'aperçu..." ou une animation de chargement (`CircularProgress`) peut apparaître brièvement.
* **Contenu du Document :**
    * **Fichiers Texte (.txt, .csv, etc.) :** Le contenu textuel du document sera récupéré depuis le serveur et affiché directement dans une zone de texte formatée (`<pre>`), vous permettant de le lire. Il peut y avoir une barre de défilement si le texte est long.
    * **Fichiers PDF (.pdf) :** Un visualiseur PDF intégré tentera d'afficher le contenu de votre document PDF (récupéré sous forme de Blob depuis le serveur) dans un `<iframe>`. Vous pourrez généralement faire défiler les pages et utiliser les contrôles du visualiseur PDF.
    * **Fichiers Image (par exemple, .png, .jpg) :** Si le type MIME correspond à une image, l'image sera récupérée (sous forme de Blob) et affichée.
    * **Autres Formats (par exemple, .doc, .docx, .html non traité comme texte brut) :** Pour les formats de fichiers qui ne sont pas explicitement gérés pour l'aperçu (comme les documents Word), un message s'affichera, tel que : "Aperçu non disponible pour '[nom du document]' (type de fichier)".
    * **En cas d'erreur de chargement :** Si le système ne parvient pas à charger le contenu pour l'aperçu (par exemple, une erreur réseau), un message d'erreur s'affichera.

    ![Fenêtre modale affichant l'aperçu d'un document PDF](/img/screenshot-document-preview-modal-pdf.png)
    ![Fenêtre modale affichant l'aperçu d'un document texte](/img/screenshot-document-preview-modal-text.png)


## Actions dans la Fenêtre d'Aperçu

* **Bouton d'Action Contextuelle :**
    * Un bouton en bas de la modale indiquera si le document est actuellement "Actif dans le Contexte" ou "Inactif". Le texte du bouton changera en conséquence (par exemple, "Désactiver du Contexte" ou "Activer dans le Contexte").
    * Cliquer sur ce bouton modifiera l'état actif/inactif du document pour la discussion en cours.

* **Bouton "Fermer" :**
    * Situé en bas de la fenêtre d'aperçu.
    * Permet de fermer la fenêtre d'aperçu et de retourner à la vue principale de la discussion.

* **Icône de Fermeture (X) :**
    * Généralement en haut à droite de la fenêtre modale.
    * Permet également de fermer l'aperçu.

    ![Boutons d'action et de fermeture dans la fenêtre d'aperçu](/img/screenshot-document-preview-action-buttons.png)
    

L'aperçu est un moyen pratique de vérifier rapidement le contenu d'un fichier sans interrompre votre flux de travail et de gérer son état actif dans le contexte.

---

Après avoir visualisé vos documents, vous pourriez avoir besoin de les gérer. Voyons comment [Supprimer des Documents du Contexte](./deleting-documents.md).