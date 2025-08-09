---
sidebar_position: 5
title: Comprendre le Contexte Documentaire du Système
---

# Comprendre le Contexte Documentaire de l'Assistant RAG Fiqh

L'Assistant RAG Fiqh utilise les documents que vous et d'autres utilisateurs téléversez pour enrichir sa base de connaissances et fournir des réponses informées à vos questions sur le Fiqh Maliki. Il est important de comprendre comment ces documents sont utilisés.

## Une Base de Connaissances Partagée

* **Contribution Collective :** Lorsque vous [téléversez des documents](../documents/how-to-upload.md), ils sont ajoutés à une base de connaissances centrale et partagée. Cela signifie que les documents téléversés par tous les utilisateurs contribuent à enrichir les informations que l'IA peut utiliser.
* **Accès Global aux Informations :** Quand vous posez une question, l'IA peut potentiellement s'appuyer sur des informations provenant de n'importe quel document téléversé dans le système par n'importe quel utilisateur, si ces informations sont jugées pertinentes pour répondre à votre question.

    ![Diagramme simple illustrant une base de connaissance globale](/img/screenshot-global-knowledge-base-diagram.png)
    ## Qu'est-ce que cela signifie pour vos discussions ?

1.  **Réponses Potentiellement Enrichies :** Votre question peut recevoir une réponse qui bénéficie d'informations issues de documents que vous n'avez pas personnellement téléversés, mais qui ont été ajoutés par d'autres utilisateurs et sont pertinents.
2.  **Pas d'Isolation Stricte des Documents par Conversation ou Utilisateur (Actuellement) :**
    * Contrairement à un système où les documents seraient strictement limités à une seule de vos discussions, ici, la pertinence par rapport à votre question prime.
    * Si vous téléversez un document dans une "Discussion A", et qu'un autre utilisateur (ou vous-même dans une "Discussion B") pose une question à laquelle ce document peut répondre, l'IA pourrait l'utiliser.
3.  **L'Historique de vos Questions/Réponses Reste Privé :**
    * Il est important de noter que **vos conversations individuelles (la suite de vos questions et des réponses de l'IA) restent associées à votre compte et à cette discussion spécifique**. D'autres utilisateurs ne voient pas vos échanges.
    * C'est le *contenu informationnel* des documents téléversés qui est partagé au niveau de la base de connaissances de l'IA, pas vos discussions personnelles.

## Comment Gérer Vos Téléversements dans ce Contexte ?

* **Pertinence :** Téléversez des documents qui sont directement liés au Fiqh Maliki et qui peuvent être utiles à une compréhension plus large du sujet.
* **Confidentialité des Documents :** Étant donné que les informations des documents peuvent potentiellement informer les réponses pour d'autres utilisateurs (même si ce n'est pas direct), **ne téléversez pas de documents contenant des informations personnelles, sensibles ou confidentielles que vous ne souhaiteriez pas voir indirectement utilisées pour répondre à des requêtes générales sur le Fiqh.**
* **La [Liste des Documents Chargés](../interface-overview/document-management-pane.md#3-liste-des-documents-chargés-documents-chargés-point-341) visible dans votre interface, lorsque vous téléversez, vous montre les fichiers que *vous* avez ajoutés lors de vos sessions et qui ont été soumis au système.**

**Note Importante sur l'Évolution du Système :**
*L'architecture actuelle utilise une base de connaissances partagée. Des évolutions futures pourraient introduire des contextes documentaires plus isolés par utilisateur ou par discussion. Cette documentation reflète le fonctionnement actuel.*

---

Maintenant que vous comprenez comment les documents contribuent au système, passons à la section suivante : [Poser des Questions et Obtenir des Réponses](../rag-usage/formulating-questions.md).