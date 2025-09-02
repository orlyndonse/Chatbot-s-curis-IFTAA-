---
sidebar_position: 3
title: Script d'Indexation Initiale (indexer_rag.py)
---

# Script d'Indexation Initiale (`indexer_rag.py`)

Le fichier `indexer_rag.py`, situé à la racine du projet backend (`Code_Source/backend/`), est un script autonome conçu pour effectuer une indexation initiale (ou une réindexation complète) des documents sources dans la base de données vectorielle ChromaDB.

## Objectif et Utilisation

* **Peuplement Initial**: Ce script est particulièrement utile pour peupler la base de données vectorielle avec un corpus de documents prédéfini avant la première mise en service de l'application, ou pour ajouter un grand volume de documents de base.
* **Maintenance/Mise à Jour**: Il peut également être utilisé pour réindexer l'ensemble des documents si des modifications majeures sont apportées aux modèles d'embedding, aux fonctions de prétraitement, ou si la base de données vectorielle doit être reconstruite.
* **Exécution Manuelle**: Contrairement à l'indexation qui se produit lorsqu'un utilisateur téléverse un fichier via l'API, ce script est destiné à être exécuté manuellement par un administrateur ou un développeur depuis la ligne de commande.

## Fonctionnement du Script (`indexer`)

La fonction principale `indexer()` dans le script orchestre le processus :

```python
# Extrait de Code_Source/backend/indexer_rag.py
import os
import logging
import time

from src.rag.loader import charger_documents, split_documents
from src.rag.vectorstore import add_documents_to_vectorstore, CHROMA_DB_PATH, COLLECTION_NAME

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SOURCE_DOCS_PATH = os.path.join("data", "fiqh_docs") # Chemin vers les documents sources

def indexer():
    logger.info("--- Démarrage du processus d'indexation RAG ---")

    if not os.path.isdir(SOURCE_DOCS_PATH):
        logger.error(f"Le dossier source '{SOURCE_DOCS_PATH}' n'existe pas...")
        return

    # 1. Charger les documents
    logger.info(f"Étape 1/3 : Chargement des documents depuis '{SOURCE_DOCS_PATH}'...")
    documents = charger_documents(SOURCE_DOCS_PATH)
    if not documents:
        logger.warning("Aucun document n'a été chargé...")
        return
    # ... logging du temps ...

    # 2. Découper les documents
    logger.info("Étape 2/3 : Découpage des documents...")
    split_docs = split_documents(documents)
    if not split_docs:
         logger.warning("Aucun morceau n'a été généré après découpage.")
         return
    # ... logging du temps et du nombre de morceaux ...

    # 3. Ajouter les documents au Vector Store (ChromaDB)
    logger.info(f"Étape 3/3 : Ajout des documents au Vector Store ChromaDB (Collection: {COLLECTION_NAME}, Path: {CHROMA_DB_PATH})...")
    try:
        add_documents_to_vectorstore(split_docs)
    except Exception as e:
         logger.error(f"Erreur lors de l'ajout des documents au vectorstore: {e}", exc_info=True)
         return
    # ... logging du temps ...

    logger.info("--- Processus d'indexation RAG terminé avec succès ! ---")

if __name__ == "__main__":
    indexer()
```

### Détails du processus

#### Configuration du Logging
Un logger basique est configuré pour afficher les informations du processus avec horodatage et niveau de log.

#### Chemin des Documents Sources (SOURCE_DOCS_PATH)
- Une constante `SOURCE_DOCS_PATH` est définie, pointant par défaut vers `data/fiqh_docs` (relatif à la racine du projet backend)
- C'est dans ce dossier que le script s'attend à trouver les documents à indexer
- Le script vérifie si ce dossier existe avant de continuer

#### Étapes du processus

1. **Chargement des Documents**:
   - Appelle `charger_documents(SOURCE_DOCS_PATH)` (depuis `src.rag.loader`) pour charger tous les fichiers supportés depuis le dossier source

2. **Découpage des Documents**:
   - Appelle `split_documents(documents)` (depuis `src.rag.loader`) pour découper les documents chargés en segments plus petits

3. **Ajout au Vector Store**:
   - Appelle `add_documents_to_vectorstore(split_docs)` (depuis `src.rag.vectorstore`) pour générer les embeddings des segments et les stocker dans la collection ChromaDB spécifiée
   - Utilise les constantes `COLLECTION_NAME` et `CHROMA_DB_PATH` importées depuis `src.rag.vectorstore`

#### Gestion des erreurs
- Des messages d'avertissement sont loggués si aucune erreur n'est levée mais qu'aucun document n'est traité, ou si le découpage ne produit aucun segment
- Les erreurs potentielles durant ces étapes sont interceptées et logguées
- Le script s'arrête en cas d'erreur critique

## Exécution du Script

Pour exécuter le script, il faut se placer à la racine du projet backend (`Code_Source/backend/`) et lancer :

```bash
python indexer_rag.py
```

### Prérequis
Il est recommandé de s'assurer que les variables d'environnement nécessaires sont disponibles dans l'environnement d'exécution du script. Notez que `GEMINI_API_KEY` n'est pas directement requise pour ce script (qui utilise HuggingFace pour les embeddings), mais elle pourrait l'être pour des dépendances indirectes liées au LLM dans d'autres modules du système.

## Conclusion

Ce script est un outil d'administration essentiel pour la préparation initiale de la base de connaissances RAG. Il permet une indexation en lot efficace et contrôlée des documents sources dans le système.


---

Nous avons maintenant couvert en détail le pipeline RAG. La prochaine grande section de l'outline est "7. Installation et Configuration de l'Environnement de Développement". Nous commencerons par les [Prérequis d'Installation](../setup-installation/prerequisites.md).

