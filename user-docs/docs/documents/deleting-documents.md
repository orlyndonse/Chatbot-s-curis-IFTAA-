---
sidebar_position: 5
title: Supprimer des Documents du Contexte
---

# Supprimer des Documents du Contexte d'une Discussion

Si vous avez téléversé un document par erreur, s'il n'est plus pertinent pour votre discussion actuelle, ou si vous souhaitez simplement alléger le contexte documentaire pour l'intelligence artificielle (IA), vous pouvez le retirer de la liste des documents associés à la conversation active.

## Comment Supprimer un Document ? (Point 6.5.1)

1.  Assurez-vous que la discussion pour laquelle vous souhaitez supprimer un document est active.
2.  Dans le [Panneau de Gestion des Documents](../interface-overview/document-management-pane.md), localisez le document que vous souhaitez supprimer dans la liste des "**Documents chargés**".
3.  À droite des informations du document, cliquez sur le bouton "**Supprimer**" (Delete). Il est généralement représenté par une icône de corbeille.

    ![Bouton "Supprimer" à côté d'un document dans la liste](/img/screenshot-document-delete-button.png)
    ## Que se passe-t-il après avoir cliqué sur "Supprimer" ? (Point 6.5.2)

* **Retrait de la Liste :** Le document disparaîtra immédiatement de la liste des "Documents chargés" pour la conversation active dans votre interface utilisateur.
* **Mise à Jour de la Taille du Contexte :** L'indicateur de [Taille du Contexte](../interface-overview/document-management-pane.md#2-indicateur-de-taille-du-contexte-point-342) sera mis à jour pour refléter la suppression du fichier et la réduction de la quantité de données contextuelles affichées.
* **Effet sur les Réponses de l'IA (pour la discussion en cours) :** Une fois qu'un document est retiré de la liste de la discussion active, l'IA **ne devrait plus considérer activement ce document spécifique comme source principale d'information pour les nouvelles questions que vous poserez *dans cette même discussion***.

    ![Liste des documents mise à jour après suppression](/img/screenshot-document-list-after-delete.png)
    **Note Importante sur la Suppression et la Base de Connaissances :**

* **Comportement Actuel :** Dans la version actuelle du système, supprimer un document de la liste d'une discussion le retire de la vue et de la considération immédiate pour *cette discussion spécifique dans votre interface*.
* **Base de Connaissances Globale :** Comme expliqué dans [Comprendre le Contexte Documentaire du Système](../conversations/conversation-context.md), les documents téléversés contribuent à une base de connaissances partagée. Le fait de retirer un document de la liste d'une de vos discussions **ne garantit pas actuellement sa suppression immédiate et définitive de la base de données vectorielle globale de l'IA sur le serveur**.
* **Implication :** Bien que le document n'apparaisse plus dans votre liste pour cette conversation, les informations qu'il contenait *pourraient* théoriquement encore influencer de manière indirecte des réponses futures de l'IA (pour vous ou d'autres utilisateurs) si ces informations sont fortement présentes dans la base globale et qu'une question les sollicite. La fonctionnalité de suppression définitive de la base de données centrale est un aspect qui pourrait être amélioré dans les futures versions.

Pour le moment, considérez l'action "Supprimer" comme un moyen de gérer la liste des documents activement présentés et pris en compte pour *votre session de discussion en cours*.

---

Pour finir cette section sur la gestion des documents, abordons la question des [Limites des Documents](./document-limits.md).