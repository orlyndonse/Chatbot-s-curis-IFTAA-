---
sidebar_position: 4
title: Modifier Votre Dernier Prompt
---

# Modifier Votre Dernier Prompt (Question)

Si vous avez fait une faute de frappe, oublié un détail, ou si vous souhaitez simplement reformuler votre dernière question pour obtenir une meilleure réponse de l'IA, l'Assistant RAG Fiqh vous permet de la modifier.

**Important :** En général, vous ne pouvez modifier que le **dernier prompt utilisateur** que vous avez envoyé dans la discussion active, et seulement si l'IA n'est pas déjà en train de générer une réponse ou si une autre action (comme le renommage d'une discussion) n'est pas en cours.

## Comment Modifier Votre Dernier Prompt ?

### Étape 1 : Localiser l'Icône de Modification (Point 5.4.1)

1.  Assurez-vous que la discussion contenant le prompt que vous souhaitez modifier est active dans la [Zone de Chat Principale](../interface-overview/main-chat-area.md).
2.  Repérez votre dernier message (prompt) dans la discussion.
3.  Passez le curseur de votre souris sur la bulle de votre message. Une icône "Modifier" (généralement un crayon - `edit` icon) devrait apparaître, souvent à côté de la bulle du message.

    ![Icône Modifier apparaissant au survol du dernier prompt utilisateur](/img/screenshot-chat-edit-prompt-icon-hover.png)
    ### Étape 2 : Activer le Mode Édition (Point 5.4.2)

1.  Cliquez sur l'icône "Modifier" (`edit`).
2.  La bulle de votre message se transformera en une zone de texte modifiable, contenant le texte original de votre prompt. Des boutons pour "Sauvegarder" et "Annuler" les modifications apparaîtront également.
    * Le curseur sera généralement placé dans la zone de texte, et le texte existant pourrait être sélectionné.
    * La hauteur de la zone de texte s'ajustera automatiquement si votre prompt modifié est plus long.

    ![Interface d'édition du prompt avec texte et boutons Sauvegarder/Annuler](/img/screenshot-chat-editing-prompt-interface.png)
    ### Étape 3 : Modifier Votre Texte (Point 5.4.2)

1.  Dans la zone de texte, apportez les corrections ou modifications souhaitées à votre prompt.

### Étape 4 : Sauvegarder ou Annuler les Modifications (Points 5.4.3 & 5.4.4)

Une fois que vous avez modifié votre texte :

* **Pour Sauvegarder les Modifications :**
    1.  Cliquez sur le bouton "**Sauvegarder**".
    2.  Vous pouvez également appuyer sur **Entrée** (sans la touche Maj/Shift) si le curseur est dans la zone de texte.
    3.  L'interface d'édition se fermera. Votre prompt modifié s'affichera.
    4.  **Important (Point 5.4.3) :** Après la sauvegarde, l'IA **régénérera sa réponse** en se basant sur votre prompt modifié. Si des messages suivaient votre prompt original dans la discussion, ceux-ci seront généralement **supprimés et remplacés** par la nouvelle suite d'interactions à partir de votre prompt édité. Un indicateur de chargement (`CircularProgress`) peut apparaître pendant la sauvegarde et la régénération.

        ![Bouton Sauvegarder lors de l'édition d'un prompt](/img/screenshot-chat-edit-save-button.png) * **Pour Annuler les Modifications :**
    1.  Cliquez sur le bouton "**Annuler**".
    2.  Vous pouvez également appuyer sur la touche **Échap (Escape)** de votre clavier.
    3.  L'interface d'édition se fermera, et votre prompt original restera inchangé. Aucune nouvelle réponse ne sera générée.

        ![Bouton Annuler lors de l'édition d'un prompt](/img/screenshot-chat-edit-cancel-button.png) **À Noter :**
* L'édition d'un prompt est une manière puissante d'affiner votre dialogue avec l'IA.
* Soyez conscient que cela modifie le cours de la conversation à partir de ce point.

---

Vous maîtrisez maintenant les interactions de base avec l'IA ! La section suivante se concentrera sur la [Gestion des Documents pour le Contexte](../documents/why-upload.md), un aspect fondamental du système RAG.