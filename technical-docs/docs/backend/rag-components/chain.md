---
sidebar_position: 1
title: Orchestration de la Chaîne RAG (src/rag/chain.py)
---

# Orchestration de la Chaîne RAG (`src/rag/chain.py`)

Le fichier `src/rag/chain.py` est responsable de la configuration et de l'initialisation de la chaîne de traitement RAG (Retrieval Augmented Generation). Ce module implémente une **architecture RAG contextualisée** qui permet de créer des chaînes de traitement dynamiques pour des conversations spécifiques avec des ensembles de documents filtrés.

## Architecture Contextualisée

Contrairement à une approche globale avec une instance unique, ce système crée des chaînes RAG **à la demande** pour chaque conversation, permettant de filtrer les documents par `document_uid` actifs pour cette conversation spécifique.

## Composants Clés

### 1. Modèle de Langage (LLM)

**Initialisation (`get_llm`) :**

- Utilise `ChatGoogleGenerativeAI` de `langchain_google_genai` pour interagir avec l'API Gemini de Google.
- Le modèle spécifié est "gemini-1.5-flash".
- La clé API est récupérée depuis `Config.GEMINI_API_KEY`.
- La température est fixée à `0.2` pour des réponses plus factuelles et moins aléatoires.
- `convert_system_message_to_human=True` est activé pour une meilleure compatibilité avec certains modèles Gemini.
- Une instance unique du LLM (`_llm_instance`) est maintenue pour éviter des réinitialisations multiples.

```python
def get_llm():
    """Initialise (si nécessaire) et retourne l'instance du LLM."""
    global _llm_instance
    if _llm_instance is None:
        logger.info("Initialisation du LLM Google Generative AI (gemini-1.5-flash)...")
        if not Config.GEMINI_API_KEY:
            logger.error("La clé API Google (GEMINI_API_KEY) n'est pas configurée.")
            raise ValueError("Clé API Google manquante.")
        try:
            _llm_instance = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0.2,
                convert_system_message_to_human=True,
                google_api_key=Config.GEMINI_API_KEY
            )
            logger.info("LLM initialisé avec succès.")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du LLM: {e}", exc_info=True)
            _llm_instance = None
            raise
    return _llm_instance
```

### 2. Retriever Filtré

**Création du Retriever (`get_filtered_retriever`) :**

- Importe la fonction `get_filtered_retriever` du module `vectorstore`
- Cette fonction crée un retriever qui ne recherche que dans les documents spécifiés par leurs `document_uid`
- Paramètre `k=7` : récupère les 7 segments de documents les plus pertinents

### 3. Template de Prompt (`template_arabe`)

Un template de prompt spécifique en arabe est défini pour guider le LLM dans la génération de ses réponses.

```python
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
- Instruit le LLM sur son rôle (expert en Fiqh Maliki)
- Définit le format de réponse attendu en arabe uniquement
- Gère les cas où l'information est trouvée dans le contexte versus les cas où elle ne l'est pas
- Prend en entrée la question (`{question}`) et le contexte récupéré (`{context}`)

### 4. Initialisation au Démarrage (`initialize_rag_chain`)

Cette fonction est appelée au démarrage de l'application pour initialiser **uniquement le LLM**.

```python
def initialize_rag_chain():
    """
    Initialise seulement le LLM au démarrage de l'application.
    Cette fonction remplace l'ancienne initialize_rag_chain().
    """
    logger.info("Initialisation du LLM au démarrage de l'application...")
    try:
        llm = get_llm()
        if llm is None:
            raise RuntimeError("Impossible d'initialiser le LLM.")
        logger.info("LLM prêt pour l'utilisation.")
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation du LLM au démarrage: {e}", exc_info=True)
        raise
```

**Processus simplifié :**
- Initialise uniquement le LLM (pas de création de chaîne globale)
- Valide que le LLM est correctement configuré
- Les chaînes RAG sont créées dynamiquement selon les besoins

### 5. Création de Chaînes RAG Contextualisées (`create_contextual_rag_chain`)

Cette fonction crée une chaîne RAG spécifique pour une conversation donnée.

```python
def create_contextual_rag_chain(
    active_document_uids: List[str], 
    chat_history: List[Tuple[str, str]]
) -> Tuple[ConversationalRetrievalChain, int]:
    """
    Crée une chaîne RAG contextualisée pour une conversation spécifique.
    
    Args:
        active_document_uids: Liste des UIDs des documents actifs pour cette conversation
        chat_history: Historique de la conversation
    
    Returns:
        Tuple contenant la chaîne RAG et le nombre de documents actifs
    """
```

**Processus de création :**

1. **Obtention du LLM** : Récupère l'instance du LLM via `get_llm()`
2. **Création du retriever filtré** : Appelle `get_filtered_retriever(active_document_uids, k=7)`
3. **Configuration du prompt** : Crée un `PromptTemplate` basé sur `template_arabe`
4. **Assemblage de la chaîne** : Utilise `ConversationalRetrievalChain.from_llm()`

**Paramètres de configuration :**
- **`llm`** : L'instance du LLM Gemini
- **`retriever`** : Le retriever filtré sur les documents actifs
- **`return_source_documents=True`** : Retourne les documents sources utilisés
- **`combine_docs_chain_kwargs={"prompt": QA_PROMPT}`** : Utilise le template arabe

### 6. Génération de Réponses Contextualisées (`generate_contextual_rag_response`)

Cette fonction génère une réponse RAG en utilisant uniquement les documents actifs.

```python
async def generate_contextual_rag_response(
    question: str,
    active_document_uids: List[str],
    chat_history: List[Tuple[str, str]]
) -> Tuple[str, Optional[List[LangchainDocument]], int]:
    """
    Génère une réponse RAG en utilisant uniquement les documents actifs de la conversation.
    
    Args:
        question: La question de l'utilisateur
        active_document_uids: Liste des UIDs des documents actifs
        chat_history: Historique de la conversation
    
    Returns:
        Tuple contenant (réponse, documents_sources, nombre_documents_actifs)
    """
```

**Processus de génération :**

1. **Création de la chaîne** : Appelle `create_contextual_rag_chain()`
2. **Invocation asynchrone** : Utilise `rag_chain.ainvoke()` avec la question et l'historique
3. **Extraction des résultats** : Récupère la réponse et les documents sources
4. **Gestion d'erreurs** : Retourne un message d'erreur générique en cas de problème

## Fonctionnement de la Chaîne RAG Contextualisée

Lorsqu'une question est posée par l'utilisateur, le processus suivant se déroule :

### 1. Création Dynamique
- Une nouvelle chaîne RAG est créée spécifiquement pour cette conversation
- Seuls les documents avec les `document_uid` actifs sont inclus dans le retriever

### 2. Condensation de la Question
- Si un historique de chat existe, la question actuelle et l'historique sont combinés pour former une question autonome

### 3. Récupération Filtrée
- La question condensée est envoyée au retriever filtré
- Récupération des 7 segments les plus pertinents parmi les documents actifs uniquement

### 4. Génération de la Réponse
- Les documents récupérés et la question sont formatés avec `template_arabe`
- Le prompt formaté est envoyé au LLM Gemini

### 5. Réponse Finale
- Le LLM génère la réponse selon les instructions du template
- La réponse est retournée avec les documents sources et le nombre de documents actifs

## Architecture et Avantages

### Filtrage Contextuel
- **Précision** : Recherche uniquement dans les documents pertinents pour la conversation
- **Performance** : Réduit l'espace de recherche et améliore la vitesse
- **Pertinence** : Améliore la qualité des réponses en évitant le bruit des documents non pertinents

### Création Dynamique
- **Flexibilité** : Chaque conversation peut avoir son propre ensemble de documents
- **Isolation** : Les conversations sont indépendantes les unes des autres
- **Évolutivité** : Facilite l'ajout/suppression de documents par conversation

### Modularité
- **Séparation des préoccupations** : LLM, VectorStore et Prompt sont gérés indépendamment
- **Réutilisabilité** : Le LLM est partagé entre toutes les conversations
- **Maintenabilité** : Modification possible de chaque composant sans affecter les autres

### Spécialisation Linguistique
- **Template spécialisé** : Optimisé pour le contenu en arabe et le domaine du Fiqh Maliki
- **Instructions claires** : Le LLM reçoit des directives précises sur le format de réponse
- **Gestion de la transparence** : Distinction claire entre les réponses basées sur les documents et celles basées sur la connaissance générale

Ce module représente donc le cœur de l'orchestration RAG, permettant de créer des expériences de conversation personnalisées et contextualisées pour chaque ensemble de documents actifs.

---

L'étape suivante dans la compréhension du pipeline RAG est de voir comment les documents sont initialement chargés et préparés, ce qui nous mène au [Chargement et Traitement des Documents](../rag-components/loader.md) (src/rag/loader.py).