# src/rag/loader.py
import os
import logging
from typing import List
from langchain_community.document_loaders import (
    DirectoryLoader,
    CSVLoader,
    PyPDFLoader,
    UnstructuredHTMLLoader,
    # TextLoader n'est plus importé ici, mais utilisé via ArabicTextLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Importez le chargeur arabe personnalisé
from .utils import ArabicTextLoader

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def charger_documents(source_directory: str) -> List[Document]:
    """
    Charge les documents depuis un dossier source spécifié.
    Supporte .txt (avec traitement arabe), .pdf, .csv, .html.
    """
    logger.info(f"Chargement des documents depuis : {source_directory}")
    documents = []

    # Définir les chargeurs pour chaque type de fichier
    # Note : On utilise ArabicTextLoader pour les .txt
    loader_configs = [
        {"glob": "**/*.csv", "loader_cls": CSVLoader, "loader_kwargs": {'encoding': 'utf-8'}}, # Spécifier l'encoding si nécessaire
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
                recursive=True, # Cherche dans les sous-dossiers
                show_progress=True,
                use_multithreading=True, # Peut accélérer le chargement
                silent_errors=True # Ignore les fichiers qu'il ne peut pas charger
            )
            loaded_docs = loader.load()
            if loaded_docs:
                logger.info(f"Chargé {len(loaded_docs)} document(s) de type {config['glob']}")
                documents.extend(loaded_docs)
            else:
                 logger.warning(f"Aucun document trouvé pour le type {config['glob']}")
        except Exception as e:
            # Log l'erreur mais continue avec les autres types de fichiers
            logger.error(f"Erreur lors du chargement des fichiers {config['glob']} depuis {source_directory}: {e}", exc_info=True)

    if not documents:
        logger.warning(f"Aucun document n'a pu être chargé depuis {source_directory}")
    else:
        logger.info(f"Total de {len(documents)} documents chargés.")

    return documents

# Fonction pour découper les documents (directement depuis le notebook)
def split_documents(documents: List[Document]) -> List[Document]:
    """
    Découpe les documents chargés en plus petits morceaux.
    """
    logger.info(f"Découpage de {len(documents)} documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,        # Taille des morceaux
        chunk_overlap=100,         # Chevauchement entre les morceaux
        length_function=len,
        is_separator_regex=False, # Utiliser les séparateurs comme des chaînes littérales
        separators=["\n\n", "\n", ". ", "، ", "؛ ", " ", ""] # Séparateurs pour l'arabe/français
    )
    texts = text_splitter.split_documents(documents)
    logger.info(f"Découpage terminé : {len(texts)} morceaux créés.")
    return texts