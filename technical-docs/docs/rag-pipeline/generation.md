---
sidebar_position: 2
title: Phase de Génération de Réponse
---

# Phase de Génération de Réponse

Après la phase d'ingestion, où les documents sont traités et stockés dans la base de données vectorielle, la phase de génération de réponse est activée lorsqu'un utilisateur soumet un prompt (une question) via l'interface de chat. Cette phase implique la récupération d'informations pertinentes à partir des documents indexés et la génération d'une réponse textuelle par le modèle de langage (LLM).

Ce processus est principalement orchestré par la méthode `generate_rag_response` dans `ConversationService`, qui utilise la `ConversationalRetrievalChain` configurée dans `src/rag/chain.py`.

## Étapes Clés de la Génération de Réponse

Lorsqu'un utilisateur envoie un prompt via l'endpoint POST `/conversations/{conversation_uid}/messages`:

1.  **Récupération de l'Historique de la Conversation**:
    * Le `ConversationService` commence par récupérer l'historique formaté des messages précédents de la conversation active en appelant `self.get_formatted_history(conversation_uid, session)`.
    * Cet historique est une liste de tuples `(prompt_utilisateur, reponse_IA)`.

2.  **Invocation de la Chaîne RAG (`ConversationalRetrievalChain`)**:
    * L'instance de `ConversationalRetrievalChain` (obtenue via `get_rag_chain()` depuis `src/rag/chain.py`) est invoquée de manière asynchrone (`await rag_chain.ainvoke(...)`).
    * Les principaux arguments passés à la chaîne sont :
        * `question`: Le prompt actuel de l'utilisateur.
        * `chat_history`: L'historique formaté de la conversation.

3.  **Fonctionnement Interne de `ConversationalRetrievalChain`**:
    * **a. Condensation de la Question (Question Condensing)**:
        * La chaîne utilise d'abord un LLM (distinct ou le même LLM principal, selon la configuration de Langchain) pour "condenser" la question actuelle de l'utilisateur et l'historique du chat en une question unique et autonome. Cette nouvelle question est formulée de manière à pouvoir être comprise sans le contexte de l'historique précédent.
        * Par exemple, si l'historique est : `Utilisateur: "Qu'est-ce que le Zakat?"`, `IA: "C'est..."`, et que la nouvelle question est `Utilisateur: "Et quelles sont ses conditions ?"`, la question condensée pourrait devenir quelque chose comme : `"Quelles sont les conditions du Zakat ?"`.
    * **b. Récupération des Documents (Retrieval)**:
        * La question condensée est ensuite passée au `retriever` configuré dans la chaîne (qui est une instance de `Chroma` agissant comme retriever, provenant de `src/rag/vectorstore.py`).
        * Le `retriever` effectue une recherche de similarité sémantique dans la base de données vectorielle (ChromaDB) pour trouver les segments de documents (chunks) les plus pertinents par rapport à la question condensée. Le nombre de documents retournés est défini par `search_kwargs={"k": 7}`.
    * **c. Combinaison et Génération (Stuffing/Generation)**:
        * Les segments de documents récupérés (le "contexte") sont combinés avec la question originale de l'utilisateur (pas la question condensée pour cette étape).
        * Ces informations (contexte + question originale) sont formatées en utilisant le `QA_PROMPT` (le `template_arabe` défini dans `src/rag/chain.py`).
        * Ce prompt final, contenant les instructions, le contexte et la question, est envoyé au LLM principal (`ChatGoogleGenerativeAI` - Gemini).
        * Le LLM génère la réponse textuelle en se basant sur les informations fournies.

4.  **Récupération de la Réponse et des Sources**:
    * Le résultat de `rag_chain.ainvoke` est un dictionnaire.
    * `ai_response_text = result.get("answer", "Désolé, une erreur est survenue.")` extrait la réponse textuelle générée par le LLM.
    * `source_documents = result.get("source_documents")` récupère la liste des documents sources (segments) que le retriever a identifiés comme pertinents et qui ont été utilisés pour construire le contexte pour le LLM. Cette option est activée par `return_source_documents=True` lors de l'initialisation de la chaîne.

5.  **Sauvegarde en Base de Données**:
    * La paire prompt utilisateur / réponse IA est ensuite sauvegardée dans la base de données PostgreSQL (table `Message`) via la méthode `ConversationService.save_message_pair`.
    * La date de dernière mise à jour de la conversation (`update_at`) est également actualisée.

6.  **Renvoi de la Réponse au Frontend**:
    * L'objet `Message` nouvellement créé (contenant le prompt, la réponse, et d'autres métadonnées) est retourné au frontend, qui l'affiche ensuite à l'utilisateur.

Ce processus permet à l'application de fournir des réponses contextuelles en s'appuyant sur une base de connaissances spécialisée, tout en maintenant la fluidité d'une conversation grâce à la prise en compte de l'historique.

---

Pour finaliser la documentation du pipeline RAG, nous aborderons le [Script d'Indexation Initiale (`indexer_rag.py`)](./initial-indexing.md) qui permet de peupler la base vectorielle avant la première utilisation ou avec des corpus de documents prédéfinis.