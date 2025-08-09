---
sidebar_position: 1
title: Orchestration de la Chaîne RAG (src/rag/chain.py)
---

# Orchestration de la Chaîne RAG (`src/rag/chain.py`)

Le fichier `src/rag/chain.py` est responsable de la configuration et de l'initialisation de la chaîne de traitement RAG (Retrieval Augmented Generation). C'est ici que le modèle de langage (LLM), le système de récupération de documents (retriever), et les prompts sont assemblés pour former la `ConversationalRetrievalChain` de Langchain.

## Composants Clés

### 1. Modèle de Langage (LLM)

**Initialisation (`get_llm`) :**

- Utilise `ChatGoogleGenerativeAI` de `langchain_google_genai` pour interagir avec l'API Gemini de Google.
- Le modèle spécifié est "gemini-1.5-flash".
- La clé API est récupérée depuis `Config.GEMINI_API_KEY`.
- La température est fixée à `0.2` pour des réponses plus factuelles et moins aléatoires.
- `convert_system_message_to_human=True` est activé pour une meilleure compatibilité avec certains modèles Gemini.
- Une instance unique du LLM (`_llm_instance`) est maintenue pour éviter des réinitialisations multiples.

### 2. VectorStore et Retriever

**Obtention du VectorStore (`get_vectorstore`) :**

- La fonction `get_vectorstore` (importée de `src.rag.vectorstore`) est appelée pour obtenir une instance de la base de données vectorielle (ChromaDB) configurée avec les embeddings.

**Création du Retriever :**

- Le VectorStore est transformé en un `retriever` en utilisant la méthode `as_retriever()`.
- `search_kwargs={"k": 7}` est configuré, signifiant que le retriever cherchera les 7 segments de documents les plus pertinents par rapport à la question.

### 3. Template de Prompt (`template_arabe`)

Un template de prompt spécifique en arabe est défini pour guider le LLM dans la génération de ses réponses.

```python
# Extrait du template_arabe
template_arabe = """أنت خبير في الفقه المالكي.

مهمتك هي الإجابة على الأسئلة المتعلقة بالفقه المالكي. يجب أن تكون جميع إجاباتك باللغة العربية الفصحى حصراً.

في حالة وجود إجابة في النصوص المتوفرة:
- قم بتقديم الإجابة مع ذكر المصدر
- اذكر الدليل إن وجد
- اذكر أقوال العلماء إن وجدت

في حالة عدم وجود إجابة في النصوص المتوفرة:
- قم بالتصريح بوضوح قائلاً: "هذه الإجابة من معرفة النموذج اللغوي وليست من النصوص المتوفرة"
- ثم قدم إجابة بناءً على معرفتك العامة بالمذهب المالكي

ملاحظة: يجب أن تكون جميع الإجابات باللغة العربية فقط.

السؤال: {question}
النصوص المتعلقة بالموضوع: {context}

الإجابة:"""
```

**Caractéristiques du template :**

- Ce template instruit le LLM sur son rôle (expert en Fiqh Maliki), le format de réponse attendu, et comment gérer les cas où l'information est trouvée dans le contexte fourni (`{context}`) versus les cas où elle ne l'est pas.
- Il prend en entrée la question de l'utilisateur (`{question}`) et le contexte récupéré par le retriever (`{context}`).

### 4. Initialisation de la Chaîne RAG (`initialize_rag_chain`)

Cette fonction est appelée au démarrage de l'application (via le lifespan dans `src/__init__.py`) pour préparer la chaîne RAG.

**Processus d'initialisation :**

- Elle récupère les instances du LLM et du VectorStore (via leurs fonctions `get_...` respectives).
- Crée un `PromptTemplate` (`QA_PROMPT`) basé sur `template_arabe` pour la partie question/contexte.
- Assemble la `ConversationalRetrievalChain` en utilisant `ConversationalRetrievalChain.from_llm`.

**Paramètres de configuration :**

- **`llm`** : L'instance du LLM Gemini.
- **`retriever`** : Le retriever configuré à partir de ChromaDB.
- **`return_source_documents=True`** : Configure la chaîne pour qu'elle retourne également les documents sources qui ont été utilisés pour générer la réponse.
- **`combine_docs_chain_kwargs={"prompt": QA_PROMPT}`** : Spécifie le prompt à utiliser pour combiner les documents récupérés et la question avant de les envoyer au LLM.

L'instance de la chaîne RAG initialisée est stockée dans une variable globale `_rag_chain_instance`.

### 5. Accès à la Chaîne RAG (`get_rag_chain`)

```python
# Extrait de Code_Source/backend/src/rag/chain.py
def get_rag_chain() -> ConversationalRetrievalChain:
    if _rag_chain_instance is None:
        logger.error("La chaîne RAG n'a pas été initialisée correctement au démarrage !")
        raise RuntimeError("La chaîne RAG n'est pas disponible...")
    return _rag_chain_instance
```

**Fonctionnalité :**

- Cette fonction permet aux autres parties de l'application (notamment `ConversationService`) d'obtenir l'instance unique et initialisée de la `ConversationalRetrievalChain`.
- Elle lève une exception si la chaîne n'a pas été correctement initialisée au démarrage, pour éviter des erreurs d'exécution.

## Fonctionnement de la Chaîne RAG

Lorsqu'une question est posée par l'utilisateur (via `ConversationService.generate_rag_response` qui appelle `get_rag_chain().ainvoke()`), la `ConversationalRetrievalChain` effectue les étapes suivantes :

### 1. Condensation de la Question
- Si un historique de chat existe, la question actuelle et l'historique du chat sont combinés pour former une question autonome et contextuelle.

### 2. Récupération (Retrieval)
- La question condensée est envoyée au retriever, qui recherche dans ChromaDB les documents (chunks) les plus pertinents.
- Le système récupère les 7 segments de documents les plus similaires sémantiquement à la question.

### 3. Génération de la Réponse
- Les documents récupérés (contexte) et la question originale sont formatés en utilisant `QA_PROMPT`.
- Le prompt formaté est envoyé au LLM (Gemini) pour génération.

### 4. Réponse Finale
- Le LLM génère la réponse selon les instructions du template.
- La réponse est retournée avec les documents sources utilisés (si `return_source_documents=True`).

## Architecture et Avantages

### Singleton Pattern
- **Instance unique** : Une seule instance de la chaîne RAG est maintenue en mémoire
- **Efficacité** : Évite les réinitialisations coûteuses à chaque requête
- **Cohérence** : Garantit la même configuration pour toutes les requêtes

### Modularité
- **Séparation des préoccupations** : Chaque composant (LLM, VectorStore, Prompt) est géré indépendamment
- **Facilité de maintenance** : Modification possible de chaque composant sans affecter les autres
- **Testabilité** : Chaque composant peut être testé isolément

### Spécialisation Linguistique
- **Template spécialisé** : Optimisé pour le contenu en arabe et le domaine du Fiqh Maliki
- **Instructions claires** : Le LLM reçoit des directives précises sur le format et le style de réponse
- **Gestion de la transparence** : Distinction claire entre les réponses basées sur les documents et celles basées sur la connaissance générale du modèle

Ce module est donc essentiel pour connecter la base de connaissances vectorielle avec la puissance de génération du LLM, tout en guidant le processus avec des instructions spécifiques via le prompt.

---

L'étape suivante dans la compréhension du pipeline RAG est de voir comment les documents sont initialement chargés et préparés, ce qui nous mène au [Chargement et Traitement des Documents](../rag-components/loader.md) (src/rag/loader.py).