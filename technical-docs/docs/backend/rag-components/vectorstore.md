---
sidebar_position: 3
title: Gestion du Vector Store (src/rag/vectorstore.py)
---

# Gestion du Vector Store (`src/rag/vectorstore.py`)

Le fichier `src/rag/vectorstore.py` est responsable de la création, de la configuration et de la gestion de la base de données vectorielle (Vector Store). Cette base de données stocke les embeddings (représentations vectorielles numériques) des segments de documents, permettant ainsi une recherche sémantique efficace pour le pipeline RAG. Le système utilise [ChromaDB](https://www.trychroma.com/) comme solution de Vector Store et [HuggingFace Embeddings](https://huggingface.co/sentence-transformers) pour générer les vecteurs.

## Configuration et Constantes

Plusieurs constantes sont définies au début du fichier pour configurer le Vector Store :

- **`CHROMA_DB_PATH`**: Chemin vers le répertoire où la base de données ChromaDB sera persistée. Il est défini comme `os.path.join(os.getcwd(), "chroma_db_fiqh")`, ce qui signifie qu'il sera dans un dossier `chroma_db_fiqh` à la racine du projet backend.
- **`COLLECTION_NAME`**: Nom de la collection au sein de ChromaDB où les embeddings seront stockés (par exemple, `"fiqh_maliki"`).
- **`EMBEDDING_MODEL_NAME`**: Nom du modèle d'embedding à utiliser depuis la bibliothèque Sentence Transformers de HuggingFace (par exemple, `"sentence-transformers/paraphrase-multilingual-mpnet-base-v2"`). Ce modèle est adapté pour générer des embeddings multilingues, ce qui est pertinent pour des textes en arabe et des questions potentiellement formulées dans d'autres langues.

Des variables globales (`_chroma_client`, `_embedding_function`) sont utilisées pour mettre en cache les instances du client ChromaDB et de la fonction d'embedding, évitant ainsi des réinitialisations coûteuses.

## Initialisation de la Fonction d'Embedding (`get_embedding_function`)

Cette fonction initialise et retourne le modèle d'embedding.

```python
# Extrait de Code_Source/backend/src/rag/vectorstore.py
def get_embedding_function():
    global _embedding_function
    if _embedding_function is None:
        logger.info(f"Initialisation du modèle d'embedding: {EMBEDDING_MODEL_NAME}")
        try:
            _embedding_function = HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL_NAME,
            )
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du modèle d'embedding: {e}", exc_info=True)
            raise
    return _embedding_function
```

**Fonctionnement :**
- Elle utilise `HuggingFaceEmbeddings` de `langchain_huggingface` pour charger le modèle spécifié par `EMBEDDING_MODEL_NAME`
- L'instance est mise en cache dans `_embedding_function`

## Initialisation du Client ChromaDB (`get_chroma_client`)

Cette fonction initialise et retourne un client ChromaDB persistant.

```python
# Extrait de Code_Source/backend/src/rag/vectorstore.py
def get_chroma_client():
    global _chroma_client
    if _chroma_client is None:
        logger.info(f"Initialisation du client ChromaDB persistant à : {CHROMA_DB_PATH}")
        try:
            os.makedirs(os.path.dirname(CHROMA_DB_PATH), exist_ok=True) # S'assure que le dossier parent existe
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
# Extrait de Code_Source/backend/src/rag/vectorstore.py
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

## Ajout de Documents au VectorStore (`add_documents_to_vectorstore`)

Cette fonction est responsable de l'ajout des segments de documents (après chargement et découpage) dans ChromaDB.

```python
# Extrait de Code_Source/backend/src/rag/vectorstore.py
def add_documents_to_vectorstore(documents: List[Document]):
    if not documents:
        logger.warning("Aucun document à ajouter au vectorstore.")
        return

    try:
        vectorstore = get_vectorstore() # Récupère le wrapper Langchain
    except Exception as e:
         logger.error(f"Erreur lors de la récupération du vectorstore: {e}", exc_info=True)
         raise

    logger.info(f"Ajout de {len(documents)} morceaux de documents à la collection '{COLLECTION_NAME}'...")
    try:
        ids = [f"{doc.metadata.get('source', 'unknown')}_{i}" for i, doc in enumerate(documents)]
        vectorstore.add_documents(documents=documents, ids=ids)
        logger.info(f"Ajout terminé. La collection contient maintenant {vectorstore._collection.count()} éléments.")
    except Exception as e:
        logger.error(f"Erreur lors de l'ajout des documents au vectorstore: {e}", exc_info=True)
        raise
```

**Étapes du processus :**
- Elle prend une liste d'objets `Document` de Langchain (qui sont les segments découpés)
- Récupère l'instance du vectorstore Langchain
- Génère des identifiants uniques (`ids`) pour chaque segment de document, typiquement basés sur la source du document et un index
- Utilise la méthode `vectorstore.add_documents(documents=documents, ids=ids)` pour ajouter les documents. Langchain gère l'appel à la fonction d'embedding configurée pour vectoriser le contenu de chaque document avant de le stocker dans ChromaDB
- Loggue le nombre d'éléments dans la collection après l'ajout

## Conclusion

Ce module assure que les documents sont correctement transformés en vecteurs et stockés de manière persistante, rendant possible la recherche sémantique qui est au cœur du RAG.

---

Pour compléter la documentation du module RAG, nous allons maintenant nous pencher sur les [Utilitaires RAG](../rag-components/utils.md) (src/rag/utils.py), notamment pour le traitement du texte arabe.