---
sidebar_position: 3
title: Gestion du Vector Store (src/rag/vectorstore.py)
---

# Gestion du Vector Store (`src/rag/vectorstore.py`)

Le fichier `src/rag/vectorstore.py` est responsable de la création, de la configuration et de la gestion de la base de données vectorielle (Vector Store). Cette base de données stocke les embeddings (représentations vectorielles numériques) des segments de documents, permettant ainsi une recherche sémantique efficace pour le pipeline RAG. Le système utilise [ChromaDB](https://www.trychroma.com/) comme solution de Vector Store et [HuggingFace Embeddings](https://huggingface.co/sentence-transformers) pour générer les vecteurs.

## Configuration et Constantes

Plusieurs constantes sont définies au début du fichier pour configurer le Vector Store :

- **`CHROMA_DB_PATH`**: Chemin vers le répertoire où la base de données ChromaDB sera persistée. Il est défini comme `os.path.join(os.getcwd(), "chroma_db_fiqh")`, ce qui signifie qu'il sera dans un dossier `chroma_db_fiqh` à la racine du projet backend.
- **`COLLECTION_NAME`**: Nom de la collection au sein de ChromaDB où les embeddings seront stockés (`"fiqh_maliki"`).
- **`EMBEDDING_MODEL_NAME`**: Nom du modèle d'embedding à utiliser depuis la bibliothèque Sentence Transformers de HuggingFace (`"sentence-transformers/paraphrase-multilingual-mpnet-base-v2"`). Ce modèle est adapté pour générer des embeddings multilingues, ce qui est pertinent pour des textes en arabe et des questions potentiellement formulées dans d'autres langues.

Des variables globales (`_chroma_client`, `_embedding_function`) sont utilisées pour mettre en cache les instances du client ChromaDB et de la fonction d'embedding, évitant ainsi des réinitialisations coûteuses.

## Initialisation de la Fonction d'Embedding (`get_embedding_function`)

Cette fonction initialise et retourne le modèle d'embedding en utilisant un pattern singleton.

```python
def get_embedding_function():
    global _embedding_function
    if _embedding_function is None:
        logger.info(f"Initialisation du modèle d'embedding: {EMBEDDING_MODEL_NAME}")
        try:
            _embedding_function = HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL_NAME,
                # model_kwargs={'device': 'cuda'} # Décommentez si GPU disponible
                # encode_kwargs={'normalize_embeddings': False}
            )
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du modèle d'embedding: {e}", exc_info=True)
            raise
    return _embedding_function
```

**Fonctionnement :**
- Elle utilise `HuggingFaceEmbeddings` de `langchain_huggingface` pour charger le modèle spécifié par `EMBEDDING_MODEL_NAME`
- L'instance est mise en cache dans `_embedding_function` pour éviter les rechargements
- Des options commentées permettent l'utilisation d'un GPU si disponible

## Initialisation du Client ChromaDB (`get_chroma_client`)

Cette fonction initialise et retourne un client ChromaDB persistant.

```python
def get_chroma_client():
    global _chroma_client
    if _chroma_client is None:
        logger.info(f"Initialisation du client ChromaDB persistant à : {CHROMA_DB_PATH}")
        try:
            os.makedirs(os.path.dirname(CHROMA_DB_PATH), exist_ok=True)
            _chroma_client = PersistentClient(path=CHROMA_DB_PATH, settings=Settings(anonymized_telemetry=False))
            logger.info("Client ChromaDB initialisé.")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du client ChromaDB: {e}", exc_info=True)
            raise
    return _chroma_client
```

**Caractéristiques importantes :**
- Utilise `PersistentClient` de `chromadb` pour créer ou se connecter à une base de données stockée au chemin `CHROMA_DB_PATH`
- `settings=Settings(anonymized_telemetry=False)` désactive la télémétrie anonyme
- Le dossier parent pour `CHROMA_DB_PATH` est créé s'il n'existe pas
- L'instance du client est mise en cache dans `_chroma_client`

## Obtention de l'Instance du VectorStore Langchain (`get_vectorstore`)

Cette fonction assemble le client ChromaDB et la fonction d'embedding pour fournir une instance du wrapper Chroma de Langchain.

```python
def get_vectorstore():
    _chroma_client_instance = get_chroma_client()
    _embedding_function_instance = get_embedding_function()

    if _chroma_client_instance is None or _embedding_function_instance is None:
         logger.error("Erreur: Le client ChromaDB ou la fonction d'embedding n'a pas pu être initialisé.")
         raise RuntimeError("Impossible d'initialiser ChromaDB ou l'embedding.")

    try:
        vectorstore = Chroma(
            client=_chroma_client_instance,
            collection_name=COLLECTION_NAME,
            embedding_function=_embedding_function_instance
        )
        logger.info("Wrapper VectorStore LangChain Chroma initialisé.")
        return vectorstore
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation du wrapper Chroma Langchain: {e}", exc_info=True)
        raise
```

**Processus d'initialisation :**
- Elle appelle `get_chroma_client()` et `get_embedding_function()` pour s'assurer que les deux composants sont initialisés
- Crée une instance de `langchain_chroma.Chroma`, en lui passant le client, le nom de la collection et la fonction d'embedding
- Cette instance `vectorstore` est ensuite utilisée par le retriever dans `chain.py` pour effectuer les recherches de similarité

## Système de Filtrage Contextualisé (`get_filtered_retriever`)

Cette fonction crée un retriever qui ne recherche que dans des documents spécifiques, permettant un RAG contextualisé par conversation.

```python
def get_filtered_retriever(active_document_uids: List[str], k: int = 7):
    logger.info(f"Creating filtered retriever for {len(active_document_uids)} active documents")
    
    vectorstore = get_vectorstore()
    
    if not active_document_uids:
        logger.warning("No active documents provided - creating empty retriever")
        return vectorstore.as_retriever(
            search_kwargs={
                "k": k,
                "filter": {"document_uid": {"$in": ["invalid_id_placeholder"]}}
            }
        )
    
    # Create filter for ChromaDB
    filter_criteria = {"document_uid": {"$in": active_document_uids}}
    logger.debug(f"Filter criteria: {filter_criteria}")
    
    return vectorstore.as_retriever(
        search_kwargs={
            "k": k,
            "filter": filter_criteria,
        }
    )
```

**Fonctionnement :**
- Prend une liste d'UIDs de documents actifs pour une conversation donnée
- Crée un filtre ChromaDB qui ne recherche que dans ces documents spécifiques
- Retourne un retriever configuré avec ce filtre
- Si aucun document actif n'est fourni, crée un retriever qui ne trouvera aucun résultat

**Utilisation :** Cette fonction est appelée par `create_contextual_rag_chain()` dans `chain.py` pour créer des chaînes RAG spécifiques à chaque conversation.

## Ajout de Documents au VectorStore (`add_documents_to_vectorstore`)

Cette fonction est responsable de l'ajout des segments de documents (après chargement et découpage) dans ChromaDB, avec enrichissement des métadonnées pour le filtrage contextuel.

```python
def add_documents_to_vectorstore(documents: List[Document], document_uid: str = None):
    if not documents:
        logger.warning("Aucun document à ajouter au vectorstore.")
        return

    try:
        vectorstore = get_vectorstore()
    except Exception as e:
         logger.error(f"Erreur lors de la récupération du vectorstore: {e}", exc_info=True)
         raise

    logger.info(f"Ajout de {len(documents)} morceaux de documents à la collection '{COLLECTION_NAME}'...")
    
    try:
        # MODIFICATION IMPORTANTE: Enrichir les métadonnées
        for i, doc in enumerate(documents):
            if document_uid:
                if not doc.metadata:
                    doc.metadata = {}
                doc.metadata['document_uid'] = document_uid
                logger.debug(f"Document chunk {i}: ajout document_uid={document_uid} dans metadata")
        
        # Générer des IDs uniques pour chaque morceau
        ids = [f"{doc.metadata.get('document_uid', 'unknown')}_{i}" for i, doc in enumerate(documents)]
        
        # Utiliser add_documents qui gère l'embedding en interne
        vectorstore.add_documents(documents=documents, ids=ids)
        logger.info(f"Ajout terminé. La collection contient maintenant {vectorstore._collection.count()} éléments.")

    except Exception as e:
        logger.error(f"Erreur lors de l'ajout des documents au vectorstore: {e}", exc_info=True)
        raise
```

**Étapes du processus :**
- Prend une liste d'objets `Document` de Langchain et un `document_uid` optionnel
- **Enrichissement des métadonnées** : Ajoute le `document_uid` dans les métadonnées de chaque chunk pour permettre le filtrage ultérieur
- Génère des identifiants uniques basés sur le `document_uid` et un index
- Utilise `vectorstore.add_documents()` qui gère automatiquement la vectorisation via la fonction d'embedding configurée
- Loggue le nombre d'éléments dans la collection après l'ajout

**Importance du `document_uid` :** Cette métadonnée est cruciale pour le système de RAG contextualisé, permettant de filtrer les recherches par document lors des conversations.

## Architecture et Avantages

### Pattern Singleton
- **Instances uniques** : Le client ChromaDB et la fonction d'embedding sont maintenus en mémoire
- **Performance** : Évite les réinitialisations coûteuses à chaque requête
- **Cohérence** : Garantit la même configuration pour toutes les opérations

### Filtrage Contextuel
- **Recherche ciblée** : Chaque conversation peut limiter la recherche à des documents spécifiques
- **Isolation des données** : Les réponses sont générées uniquement à partir des documents pertinents
- **Flexibilité** : Permet de créer des expériences RAG personnalisées par utilisateur ou contexte

### Persistance
- **Stockage durable** : Les embeddings sont sauvegardés sur disque via ChromaDB
- **Redémarrage rapide** : Pas besoin de recalculer les embeddings après un redémarrage du serveur
- **Évolutivité** : La base peut grandir progressivement avec l'ajout de nouveaux documents

## Conclusion

Ce module assure que les documents sont correctement transformés en vecteurs et stockés de manière persistante, tout en supportant un système de filtrage sophistiqué qui permet un RAG contextualisé. L'architecture singleton garantit des performances optimales, tandis que l'enrichissement des métadonnées avec `document_uid` permet une recherche sémantique ciblée par conversation.

---

Pour compléter la compréhension du pipeline, le module suivant détaille les [Utilitaires RAG](../rag-components/utils.md) (src/rag/utils.py), notamment pour le traitement spécialisé du texte arabe.