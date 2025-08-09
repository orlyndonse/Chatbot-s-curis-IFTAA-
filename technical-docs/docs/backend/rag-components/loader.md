---
sidebar_position: 2
title: Chargement et Traitement des Documents (src/rag/loader.py)
---

# Chargement et Traitement des Documents (`src/rag/loader.py`)

Le fichier `src/rag/loader.py` est crucial pour la phase d'ingestion des données dans le pipeline RAG. Il est responsable du chargement des documents à partir d'un répertoire source, de la gestion de différents formats de fichiers (y compris un traitement spécifique pour l'arabe), et du découpage des documents chargés en segments (chunks) plus petits, prêts à être vectorisés.

## Fonction `charger_documents`

Cette fonction prend en entrée un chemin vers un répertoire (`source_directory`) et retourne une liste d'objets `Document` de Langchain.

```python
# Extrait de Code_Source/backend/src/rag/loader.py
def charger_documents(source_directory: str) -> List[Document]:
    logger.info(f"Chargement des documents depuis : {source_directory}")
    documents = []

    loader_configs = [
        {"glob": "**/*.csv", "loader_cls": CSVLoader, "loader_kwargs": {'encoding': 'utf-8'}},
        {"glob": "**/*.html", "loader_cls": UnstructuredHTMLLoader},
        {"glob": "**/*.pdf", "loader_cls": PyPDFLoader},
        {"glob": "**/*.txt", "loader_cls": ArabicTextLoader, "loader_kwargs": {'encoding': 'utf-8'}}
    ]

    for config in loader_configs:
        try:
            loader = DirectoryLoader(
                source_directory,
                glob=config["glob"],
                loader_cls=config["loader_cls"],
                loader_kwargs=config.get("loader_kwargs", {}),
                recursive=True,
                show_progress=True,
                use_multithreading=True,
                silent_errors=True
            )
            loaded_docs = loader.load()
            if loaded_docs:
                logger.info(f"Chargé {len(loaded_docs)} document(s) de type {config['glob']}")
                documents.extend(loaded_docs)
            else:
                 logger.warning(f"Aucun document trouvé pour le type {config['glob']}")
        except Exception as e:
            logger.error(f"Erreur lors du chargement des fichiers {config['glob']} ...: {e}", exc_info=True)

    # ...
    return documents
```

### Configuration des Loaders (loader_configs)

Une liste `loader_configs` définit les types de fichiers à charger et les classes de Loader Langchain correspondantes.

**Formats supportés et leurs loaders :**
- `.csv`: CSVLoader (avec encodage utf-8)
- `.html`: UnstructuredHTMLLoader
- `.pdf`: PyPDFLoader
- `.txt`: ArabicTextLoader (loader personnalisé défini dans `src/rag/utils.py` qui applique un prétraitement au texte arabe, avec encodage utf-8)

### DirectoryLoader

Pour chaque configuration, un `DirectoryLoader` de Langchain est utilisé.

**Paramètres clés :**
- `glob`: Spécifie le pattern des fichiers à inclure (par exemple, `**/*.pdf` pour tous les PDF dans le répertoire et ses sous-dossiers)
- `loader_cls`: La classe de loader à utiliser pour ces fichiers
- `loader_kwargs`: Arguments spécifiques à passer au constructeur du loader (comme l'encodage)
- `recursive=True`: Permet de chercher les fichiers dans les sous-dossiers
- `show_progress=True`: Affiche une barre de progression pendant le chargement (utile pour les grands volumes)
- `use_multithreading=True`: Tente d'utiliser plusieurs threads pour accélérer le chargement
- `silent_errors=True`: Ignore les fichiers qu'il ne peut pas charger et continue le processus, loguant une erreur

### Agrégation et Logging

- Les documents chargés par chaque `DirectoryLoader` sont ajoutés à la liste `documents`
- Des messages d'information et d'avertissement sont loggués concernant le nombre de documents chargés ou l'absence de documents pour un type donné

## Fonction `split_documents`

Une fois les documents chargés, cette fonction les découpe en plus petits segments (chunks) en utilisant `RecursiveCharacterTextSplitter` de Langchain.

```python
# Extrait de Code_Source/backend/src/rag/loader.py
def split_documents(documents: List[Document]) -> List[Document]:
    logger.info(f"Découpage de {len(documents)} documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
        separators=["\n\n", "\n", ". ", "، ", "؛ ", " ", ""],
    )
    texts = text_splitter.split_documents(documents)
    logger.info(f"Découpage terminé : {len(texts)} morceaux créés.")
    return texts
```

### RecursiveCharacterTextSplitter

**Paramètres de configuration :**
- `chunk_size=1000`: Définit la taille maximale (en nombre de caractères, via `length_function=len`) de chaque segment
- `chunk_overlap=100`: Spécifie le nombre de caractères de chevauchement entre les segments consécutifs. Cela aide à maintenir le contexte entre les chunks
- `is_separator_regex=False`: Traite les séparateurs comme des chaînes littérales
- `separators=["\n\n", "\n", ". ", "، ", "؛ ", " ", ""]`: Liste de chaînes de caractères utilisées pour découper le texte, par ordre de priorité. Ces séparateurs sont adaptés pour du texte en arabe et en français

**Fonctionnement :**
- `split_documents(documents)`: Applique le découpage à la liste des documents Langchain chargés
- **Logging**: Le nombre de documents initiaux et le nombre de segments créés sont loggués

## Conclusion

Ce module est une étape préliminaire essentielle pour préparer les données textuelles avant leur indexation dans la base de données vectorielle. Le choix des loaders et des paramètres du splitter a un impact direct sur la qualité de la récupération d'informations par la suite.

---

Après le chargement et le découpage, les documents sont prêts pour être stockés et interrogés. La prochaine étape logique est de documenter la [Gestion du Vector Store](../rag-components/vectorstore.md) (src/rag/vectorstore.py).