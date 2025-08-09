---
sidebar_position: 4
title: Supprimer une Discussion
---

# Supprimer une Discussion (Conversation)

Si vous avez des discussions que vous ne souhaitez plus conserver dans votre historique, l'Assistant RAG Fiqh vous permet de les supprimer.

## Comment Supprimer une Discussion ?

### Étape 1 : Localiser la Discussion et l'Icône de Suppression (Point 4.4.1)

1.  Ouvrez la [Barre Latérale (Sidebar)](../interface-overview/sidebar.md) où votre "**Historique**" de discussions est listé.
2.  Passez le curseur de votre souris sur la discussion que vous souhaitez supprimer. Des icônes d'action devraient apparaître (généralement à droite du titre de la discussion).
3.  Repérez l'icône de suppression, qui ressemble à une poubelle (dans votre application, c'est l'icône `delete`).

    ![Icône de suppression au survol d'une discussion dans la sidebar](/img/screenshot-sidebar-delete-icon-hover.png)
    ### Étape 2 : Cliquer sur l'Icône de Suppression (Point 4.4.2)

1.  Cliquez sur l'icône de suppression (`delete`).
2.  **Important :** Dans la version actuelle de l'application, la suppression est directe et **ne demande pas de confirmation** supplémentaire. Soyez donc certain de vouloir supprimer la discussion avant de cliquer.
    *(Note : Une future mise à jour pourrait ajouter une étape de confirmation.)*
3.  Un indicateur de chargement (`CircularProgress`) peut apparaître brièvement sur l'élément de la discussion pendant sa suppression.

## Que se passe-t-il après la suppression ? (Point 4.4.3)

* **La discussion est retirée de l'historique :** La discussion supprimée n'apparaîtra plus dans la liste de la barre latérale.
* **Changement de discussion active :**
    * Si la discussion que vous avez supprimée était celle activement affichée dans la zone de chat, le système sélectionnera automatiquement la discussion suivante dans la liste (généralement la plus récente restante).
    * Si aucune autre discussion n'existe, la zone de chat reviendra à l'état initial, affichant potentiellement le [message de bienvenue](../interface-overview/main-chat-area.md#1-message-de-bienvenue-point-232-de-loutline-réf-greetingsjsx).
* **Les messages et documents associés :** La suppression d'une discussion entraîne également la suppression de tous les messages qu'elle contenait et du contexte des documents qui y étaient spécifiquement associés (du point de vue de l'application).

**Soyez prudent lorsque vous supprimez des discussions, car cette action est généralement irréversible.**

---

Après avoir géré la suppression, il est important de bien comprendre le [Contexte des Conversations](./conversation-context.md) et comment les documents y sont liés.