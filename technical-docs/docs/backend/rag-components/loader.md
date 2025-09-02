---
sidebar_position: 2
title: Chargement et Traitement des Documents (src/rag/loader.py)
---

# Chargement et Traitement des Documents (`src/rag/loader.py`)

Le fichier `src/rag/loader.py` est crucial pour la phase d'ingestion des données dans le pipeline RAG. Il est responsable du chargement des documents à partir d'un répertoire source, de la gestion de différents formats de fichiers (y compris un traitement spécifique pour l'arabe), et du découpage des documents chargés en segments (chunks) plus petits, prêts à être vectorisés.

## Imports et Dépendances

Le module importe les loaders spécialisés de Langchain pour différents types de fichiers :

```python
from langchain_community.document_loaders import (
    DirectoryLoader,
    CSVLoader,
    PyPDFLoader,
    UnstructuredHTMLLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Importe le chargeur arabe personnalisé
from .utils import ArabicTextLoader
```

**Note importante :** `TextLoader` n'est pas importé directement dans ce module, mais utilisé via `ArabicTextLoader` défini dans `utils.py`.

## Fonction `charger_documents`

Cette fonction prend en entrée un chemin vers un répertoire (`source_directory`) et retourne une liste d'objets `Document` de Langchain.

```python
def charger_documents(source_directory: str) -> List[Document]:
    logger.info(f"Chargement des documents depuis : {source_directory}")
    documents = []

    # Définir les chargeurs pour chaque type de fichier
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
            logger.error(f"Erreur lors du chargement des fichiers {config['glob']} depuis {source_directory}: {e}", exc_info=True)

    if not documents:
        logger.warning(f"Aucun document n'a pu être chargé depuis {source_directory}")
    else:
        logger.info(f"Total de {len(documents)} documents chargés.")

    return documents
```

### Configuration des Loaders (loader_configs)

Une liste `loader_configs` définit les types de fichiers à charger et les classes de Loader Langchain correspondantes.

**Formats supportés et leurs loaders :**
- **`.csv`**: `CSVLoader` avec encodage UTF-8 explicite
- **`.html`**: `UnstructuredHTMLLoader` pour le contenu HTML
- **`.pdf`**: `PyPDFLoader` pour l'extraction de texte des PDF
- **`.txt`**: `ArabicTextLoader` (loader personnalisé défini dans `src/rag/utils.py`) qui applique un prétraitement spécifique au texte arabe, avec encodage UTF-8

### DirectoryLoader

Pour chaque configuration, un `DirectoryLoader` de Langchain est utilisé avec les paramètres suivants :

**Paramètres clés :**
- **`glob`**: Spécifie le pattern des fichiers à inclure (par exemple, `**/*.pdf` pour tous les PDF dans le répertoire et ses sous-dossiers)
- **`loader_cls`**: La classe de loader à utiliser pour ces fichiers
- **`loader_kwargs`**: Arguments spécifiques à passer au constructeur du loader (comme l'encodage UTF-8)
- **`recursive=True`**: Permet de chercher les fichiers dans les sous-dossiers
- **`show_progress=True`**: Affiche une barre de progression pendant le chargement (utile pour les grands volumes)
- **`use_multithreading=True`**: Tente d'utiliser plusieurs threads pour accélérer le chargement
- **`silent_errors=True`**: Ignore les fichiers qu'il ne peut pas charger et continue le processus, en loguant les erreurs

### Gestion d'Erreurs et Logging

- **Gestion gracieuse des erreurs** : Chaque type de fichier est traité indépendamment. Si un type échoue, les autres continuent
- **Logging détaillé** : Information sur le nombre de documents chargés par type, avertissements pour les types sans documents, et erreurs détaillées
- **Agrégation** : Les documents chargés par chaque `DirectoryLoader` sont ajoutés à la liste `documents`

## Fonction `split_documents`

Une fois les documents chargés, cette fonction les découpe en plus petits segments (chunks) en utilisant `RecursiveCharacterTextSplitter` de Langchain.

```python
def split_documents(documents: List[Document]) -> List[Document]:
    logger.info(f"Découpage de {len(documents)} documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
        separators=["\n\n", "\n", ". ", "، ", "؛ ", " ", ""]
    )
    texts = text_splitter.split_documents(documents)
    logger.info(f"Découpage terminé : {len(texts)} morceaux créés.")
    return texts
```

### RecursiveCharacterTextSplitter

**Paramètres de configuration :**
- **`chunk_size=1000`**: Définit la taille maximale (en nombre de caractères, via `length_function=len`) de chaque segment
- **`chunk_overlap=100`**: Spécifie le nombre de caractères de chevauchement entre les segments consécutifs. Cela aide à maintenir le contexte entre les chunks et évite la perte d'information aux frontières
- **`length_function=len`**: Utilise la fonction Python `len()` pour mesurer la taille des segments
- **`is_separator_regex=False`**: Traite les séparateurs comme des chaînes littérales (pas d'expressions régulières)
- **`separators=["\n\n", "\n", ". ", "، ", "؛ ", " ", ""]`**: Liste de chaînes de caractères utilisées pour découper le texte, par ordre de priorité décroissant

### Séparateurs Multilingues

Les séparateurs sont spécialement adaptés pour du contenu arabe et français/anglais :
- **`"\n\n"`** : Double retour à la ligne (priorité la plus haute) - sépare les paragraphes
- **`"\n"`** : Simple retour à la ligne - sépare les lignes
- **`". "`** : Point suivi d'espace - fin de phrase en latin
- **`"، "`** : Virgule arabe suivie d'espace
- **`"؛ "`** : Point-virgule arabe suivi d'espace
- **`" "`** : Espace simple - dernier recours avant les mots individuels
- **`""`** : Chaîne vide - découpage caractère par caractère si nécessaire

### Processus de Découpage

**Fonctionnement :**
- `split_documents(documents)` : Applique le découpage à la liste des documents Langchain chargés
- **Stratégie récursive** : Le splitter essaie d'abord de découper selon les séparateurs de priorité haute (paragraphes), puis descend dans la hiérarchie si les chunks sont encore trop grands
- **Préservation des métadonnées** : Chaque chunk hérite des métadonnées du document original
- **Logging** : Le nombre de documents initiaux et le nombre de segments créés sont logués

## Workflow Complet

Le processus complet d'ingestion des données suit cette séquence :

1. **Chargement** : `charger_documents()` parcourt le répertoire source et charge tous les fichiers supportés
2. **Prétraitement** : Pour les fichiers `.txt`, `ArabicTextLoader` applique un prétraitement spécialisé du texte arabe
3. **Découpage** : `split_documents()` divise les longs documents en segments de taille appropriée
4. **Vectorisation** : Les chunks sont ensuite transmis à `vectorstore.py` pour être transformés en embeddings

## Avantages de cette Architecture

### Modularité
- **Séparation des responsabilités** : Chargement et découpage sont des étapes distinctes
- **Extensibilité** : Facile d'ajouter de nouveaux formats de fichiers
- **Testabilité** : Chaque fonction peut être testée indépendamment

### Robustesse
- **Gestion d'erreurs** : Les échecs sur certains fichiers n'arrêtent pas le processus global
- **Logging complet** : Traçabilité complète du processus d'ingestion
- **Traitement multithread** : Performance améliorée pour les gros volumes

### Spécialisation Linguistique
- **Traitement arabe** : Utilisation d'`ArabicTextLoader` pour le prétraitement spécialisé
- **Séparateurs adaptés** : Découpage optimisé pour le contenu multilingue arabe/latin
- **Encodage correct** : UTF-8 explicite pour tous les formats textuels

## Conclusion

Ce module constitue la première étape critique du pipeline RAG, transformant des fichiers bruts en segments de texte prêts à être vectorisés. Le choix des loaders, des paramètres du splitter, et du traitement spécialisé pour l'arabe a un impact direct sur la qualité de la récupération d'informations dans les étapes ultérieures.

---

Après le chargement et le découpage, les documents sont prêts pour être stockés et interrogés. La prochaine étape logique est la [Gestion du Vector Store](../rag-components/vectorstore.md) (src/rag/vectorstore.py) qui transforme ces segments en embeddings vectoriels.