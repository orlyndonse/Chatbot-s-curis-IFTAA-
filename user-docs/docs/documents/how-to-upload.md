---
sidebar_position: 2
title: Comment Téléverser des Documents
---

# Comment Téléverser (Uploader) des Documents

Pour que l'Assistant RAG Fiqh puisse utiliser vos textes de Fiqh Maliki, vous devez d'abord les téléverser (uploader) dans le contexte de la discussion active. Voici les méthodes disponibles :

**Important Avant de Commencer :**
* Assurez-vous d'avoir une [discussion active sélectionnée](../conversations/starting-new.md) ou [basculez vers une discussion existante](../conversations/switching.md). Les documents sont téléversés dans le contexte de la discussion actuellement ouverte.
* Les documents que vous téléversez contribuent à une [base de connaissances partagée](../conversations/conversation-context.md) utilisée par l'IA.

## Méthode 1 : Utiliser le Bouton "Uploader" dans le Champ de Prompt (Point 6.2.1)

Cette méthode est pratique pour ajouter rapidement des documents pendant que vous formulez vos questions.

1.  Localisez le [Champ de Saisie de Prompt](../interface-overview/prompt-field.md) en bas de la zone de chat.
2.  À côté de la zone de texte où vous tapez votre question, vous trouverez un bouton "Uploader des documents". Il est souvent représenté par une icône de trombone ou de nuage.

    ![Bouton "Uploader des documents" dans le champ de prompt](/img/screenshot-prompt-upload-button.png)
    3.  Cliquez sur ce bouton "Uploader des documents".
4.  Une fenêtre de dialogue de votre ordinateur s'ouvrira, vous invitant à sélectionner les fichiers que vous souhaitez téléverser.
5.  Naviguez jusqu'à l'emplacement de vos fichiers, sélectionnez un ou plusieurs fichiers (maintenez la touche Ctrl ou Cmd enfoncée pour en sélectionner plusieurs), puis cliquez sur "Ouvrir" ou "Choisir".
6.  Les fichiers sélectionnés seront alors téléversés et traités. Un indicateur de chargement peut s'afficher sur le bouton d'upload pendant cette opération.

    ![Fenêtre de dialogue pour sélectionner des fichiers à téléverser](/img/screenshot-file-dialog-upload.png)
    ## Méthode 2 : Utiliser la Zone de Gestion des Documents (Point 6.2.2)

Le [Panneau de Gestion des Documents](../interface-overview/document-management-pane.md) offre également une zone dédiée au téléversement, souvent avec une fonctionnalité de glisser-déposer.

1.  Identifiez la zone de téléversement dans le Panneau de Gestion des Documents. Elle peut comporter un message comme "Glissez des fichiers ici ou cliquez pour parcourir".

    ![Zone de téléversement dans le Panneau de Gestion des Documents](/img/screenshot-document-upload-area.png)
    2.  **Option A : Cliquer pour Parcourir**
    * Cliquez n'importe où dans cette zone.
    * Une fenêtre de dialogue de votre ordinateur s'ouvrira (similaire à la méthode 1).
    * Sélectionnez vos fichiers et validez.

3.  **Option B : Glisser-Déposer (Drag-and-Drop)**
    * Ouvrez l'explorateur de fichiers de votre ordinateur et localisez les documents que vous souhaitez ajouter.
    * Sélectionnez le(s) fichier(s).
    * Cliquez et maintenez le bouton de la souris enfoncé sur les fichiers sélectionnés, puis faites-les glisser jusque sur la zone de téléversement dans l'application.
    * Relâchez le bouton de la souris. Les fichiers seront téléversés. La zone peut changer d'apparence (par exemple, devenir en surbrillance) lorsque vous faites glisser des fichiers dessus.

    ![Animation ou image illustrant le glisser-déposer de fichiers](/img/screenshot-drag-and-drop-files.gif)
    ## Formats de Fichiers Supportés (Point 6.2.3)

L'Assistant RAG Fiqh accepte les formats de fichiers suivants pour le téléversement :
* PDF (`.pdf`)
* Texte brut (`.txt`)
* Microsoft Word (`.doc`, `.docx`)
* CSV (`.csv`)
* HTML (`.html`)



Assurez-vous que vos documents sont dans l'un de ces formats pour qu'ils puissent être traités correctement.

## Téléversement de Plusieurs Fichiers (Point 6.2.4)

Vous pouvez téléverser plusieurs documents à la fois en utilisant l'une ou l'autre des méthodes décrites ci-dessus.
* Lorsque vous utilisez la fenêtre de dialogue de fichiers, vous pouvez sélectionner plusieurs fichiers en maintenant la touche **Ctrl** (Windows) ou **Cmd** (Mac) enfoncée tout en cliquant sur les fichiers.
* Avec le glisser-déposer, vous pouvez sélectionner plusieurs fichiers dans votre explorateur et les faire glisser ensemble.

Une fois téléversés, les documents apparaîtront dans la [Liste des Documents Chargés](../interface-overview/document-management-pane.md#3-liste-des-documents-chargés-documents-chargés-point-341) pour la discussion active.

---

Après avoir téléversé vos documents, il est utile de savoir comment les [Visualiser et Comprendre les Informations Affichées](./viewing-uploaded.md).