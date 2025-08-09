---
sidebar_position: 3
title: Comprendre les Réponses de l'IA
---

# Comprendre les Réponses de l'Intelligence Artificielle (IA)

Après avoir [envoyé votre question (prompt)](./sending-prompt.md), l'Assistant RAG Fiqh traitera votre demande et vous fournira une réponse. Voici comment interpréter ce que vous recevez :

## 1. Où la Réponse Apparaît-elle ? (Point 5.3.1)

* La réponse de l'IA s'affiche directement dans la [Zone de Chat Principale](../interface-overview/main-chat-area.md), généralement sous votre question.
* Elle est souvent présentée dans une bulle de discussion visuellement distincte de vos propres questions (par exemple, avec une couleur de fond ou un alignement différent).

    ![Exemple de réponse de l'IA dans la zone de chat](/img/screenshot-ai-response-bubble.png)
    ## 2. Types de Réponses et Provenance (Point 5.3.2)

L'Assistant RAG Fiqh est conçu pour utiliser les documents que vous téléversez comme principale source d'information. Cependant, il peut y avoir des nuances dans ses réponses :

* **Réponses Basées sur Vos Documents :** Idéalement, la majorité des réponses à vos questions spécifiques sur le Fiqh Maliki proviendront des informations contenues dans les fichiers que vous avez ajoutés au contexte de la discussion. L'IA essaiera d'extraire et de synthétiser l'information pertinente de ces textes.

* **Réponses Basées sur les Connaissances Générales de l'IA :**
    * Si l'IA ne trouve pas d'information pertinente dans les documents fournis pour répondre à votre question, ou si la question est de nature plus générale, elle pourrait utiliser ses connaissances préexistantes.
    * **Indicateur Important :** Dans de tels cas, le système est conçu pour (ou devrait idéalement) vous informer que la réponse ne provient pas directement de vos documents. Vous pourriez voir un message tel que :
        `"هذه الإجابة من معرفة النموذج اللغوي وليست من النصوص المتوفرة."`
        *(Traduction : "Cette réponse est issue de la connaissance du modèle linguistique et non des textes disponibles.").*
    * Si vous voyez ce message, considérez la réponse comme une information générale de l'IA, qui peut être utile mais n'est pas directement tirée des sources que vous avez spécifiquement téléversées pour cette conversation.

    ![Exemple de message indiquant une réponse basée sur les connaissances générales de l'IA](/img/screenshot-ai-general-knowledge-disclaimer.png)
    ## 3. Comprendre les Sources Utilisées (Attribution des Sources) (Point 5.3.3)

Savoir d'où l'IA tire ses informations est crucial, surtout pour des sujets comme le Fiqh. Voici comment comprendre les sources :

* **Documents Actifs dans la Discussion (Point 5.3.3.1) :**
    * La liste des "**Documents chargés**" affichée dans le [Panneau de Gestion des Documents](../interface-overview/document-management-pane.md) vous indique quels fichiers sont actuellement considérés comme faisant partie du contexte pour la discussion active.
    * L'IA utilisera **principalement ces documents** pour fonder ses réponses.

* **Mentions de Sources dans la Réponse (Point 5.3.3.2) :**
    * Dans certains cas, la réponse de l'IA peut directement mentionner les noms des fichiers sources d'où l'information a été tirée (par exemple, "Comme mentionné dans `nom_du_fichier.pdf`..."). Le système original sur lequel cette application est basée listait les fichiers sources sous la réponse.
    * **Votre interface actuelle :** Vérifiez si les réponses de l'IA dans votre application incluent de telles mentions explicites des noms de fichiers. Si oui, cela vous aide à tracer l'origine de l'information.
    * Si de telles mentions directes ne sont pas présentes dans la réponse de l'IA, référez-vous à la liste des documents chargés pour la conversation pour savoir quelles étaient les sources disponibles pour l'IA.

    *(Note : La capacité de l'IA à citer précisément des passages ou des pages spécifiques peut varier. L'indication des fichiers sources utilisés est déjà une information précieuse.)*

## 4. Qualité et Limites des Réponses

* **Pertinence :** L'IA s'efforce de fournir des réponses pertinentes. Si une réponse semble hors sujet, essayez de [reformuler votre question](./formulating-questions.md) ou de vérifier que les documents appropriés sont dans le contexte de la discussion.
* **Exactitude :** Bien que l'IA utilise vos documents, il est important de se rappeler que "Ce système RAG peut afficher des informations inexactes". Pour des sujets aussi importants que le Fiqh, il est toujours recommandé de **vérifier les informations critiques** en consultant les textes originaux ou des savants qualifiés.
* **Langue et Formatage :** Les réponses seront en arabe. Des problèmes mineurs de formatage ou de style peuvent parfois survenir.

En comprenant comment les réponses sont générées et d'où elles proviennent, vous pourrez mieux évaluer leur pertinence pour vos besoins.

---

Si une réponse n'est pas tout à fait ce que vous attendiez, vous pourriez vouloir [Modifier Votre Dernier Prompt](./editing-prompt.md) pour affiner votre question.