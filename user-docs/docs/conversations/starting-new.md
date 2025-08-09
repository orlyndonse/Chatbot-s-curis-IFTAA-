---
sidebar_position: 1
title: Démarrer une Nouvelle Discussion
---

# Démarrer une Nouvelle Discussion (Conversation)

Lorsque vous souhaitez aborder un nouveau sujet de Fiqh, interroger l'IA avec un nouveau jeu de documents, ou simplement organiser vos questions par thèmes, vous pouvez démarrer une nouvelle discussion (aussi appelée conversation).

## Comment Démarrer une Nouvelle Discussion ?

1.  Repérez la [Barre Latérale (Sidebar)](../interface-overview/sidebar.md) sur le côté gauche de votre écran. Sur les appareils mobiles ou si elle est masquée, ouvrez-la via l'icône menu (☰) dans la [Barre Supérieure](../interface-overview/top-bar.md).
2.  En haut de la barre latérale, vous trouverez un bouton bien visible, souvent accompagné d'une icône (comme un "+") et du texte "**Nouvelle Discussion**".

    ![Bouton "Nouvelle Discussion" dans la barre latérale](/img/screenshot-sidebar-new-chat-button.png)

3.  Cliquez sur le bouton "**Nouvelle Discussion**".

## Que se passe-t-il ensuite ?

Une fois que vous avez cliqué sur "Nouvelle Discussion" :

* **Réinitialisation de l'Interface :**
    * L'état de la conversation active est réinitialisé .
    * La [Zone de Chat Principale](../interface-overview/main-chat-area.md) s'efface, prête pour une nouvelle interaction. Si une conversation précédente était active, ses messages et documents ne seront plus affichés dans la zone principale.
    * Vous verrez généralement le [Message de Bienvenue](../interface-overview/main-chat-area.md) vous invitant à poser votre première question.
    * Le [Champ de Saisie de Prompt](../interface-overview/prompt-field.md) sera prêt pour que vous puissiez taper votre première question pour cette nouvelle discussion.

    ![Nouvelle Discussion](/img/new-chat-auto-titled.png)

* **Gestion du Renommage :** Si vous étiez en train de renommer une autre conversation, cette action sera annulée.

![Nouvelle Discussion bouton désactivé](/img/screenshot-rename-Button-Off.png)


* **Comportement sur Mobile/Tablette :** Si la barre latérale était ouverte sur un petit écran, elle se fermera pour laisser plus de place à la nouvelle discussion (`toggleSidebar()` est appelé si `window.innerWidth < 1024`).
![Nouvelle Discussion petit écran](/img/screenshot-nouvelle-discussion-SurMobile.png)



## Titre de la Nouvelle Discussion

* **Création Initiale :** Lorsque vous cliquez sur "Nouvelle Discussion" et que vous envoyez votre premier prompt (question), une nouvelle conversation est créée en arrière-plan par le système.
* **Titre Automatique :** Le titre de cette nouvelle conversation sera automatiquement généré à partir des premiers mots de votre premier prompt. Par exemple, si votre premier prompt est "ما حكم الصلاة للمسافر؟", le titre de la conversation dans l'[Historique](../interface-overview/sidebar.md) pourrait devenir quelque chose comme "ما حكم الصلاة للمساف...".
* **Personnalisation :** Vous pourrez [Renommer cette conversation](./renaming.md) plus tard si vous souhaitez lui donner un titre plus spécifique.

    ![Nouvelle discussion dans l'historique après le premier prompt](/img/screenshot-new-chat-auto-titled.png)
    

C'est aussi simple que cela de commencer une nouvelle session de questions-réponses avec l'Assistant RAG Fiqh !

---

Maintenant que vous savez démarrer une nouvelle discussion, voyons comment [Naviguer et Basculer Entre les Conversations](./switching.md).