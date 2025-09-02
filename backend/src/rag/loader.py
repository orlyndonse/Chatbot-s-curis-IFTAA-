import os
import logging
from typing import List
from langchain_community.document_loaders import (
    DirectoryLoader,
    CSVLoader,
    PyPDFLoader,
    UnstructuredHTMLLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Import du chargeur de texte arabe personnalisé
from .utils import ArabicTextLoader

# Configuration du système de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def charger_documents(source_directory: str) -> List[Document]:
    """
    Charge tous les documents depuis un dossier source spécifié.
    Supporte les formats : .txt (avec traitement spécialisé pour l'arabe), .pdf, .csv, .html
    
    Args:
        source_directory: Chemin vers le dossier contenant les documents à charger
        
    Returns:
        Liste des documents chargés avec leurs métadonnées
    """
    logger.info(f"Chargement des documents depuis : {source_directory}")
    documents = []

    # Configuration des chargeurs pour chaque type de fichier supporté
    loader_configs = [
        {"glob": "**/*.csv", "loader_cls": CSVLoader, "loader_kwargs": {'encoding': 'utf-8'}},
        {"glob": "**/*.html", "loader_cls": UnstructuredHTMLLoader},
        {"glob": "**/*.pdf", "loader_cls": PyPDFLoader},
        {"glob": "**/*.txt", "loader_cls": ArabicTextLoader, "loader_kwargs": {'encoding': 'utf-8'}} # Chargeur spécialisé pour l'arabe
    ]

    # Traitement de chaque type de fichier
    for config in loader_configs:
        try:
            loader = DirectoryLoader(
                source_directory,
                glob=config["glob"],
                loader_cls=config["loader_cls"],
                loader_kwargs=config.get("loader_kwargs", {}),
                recursive=True, # Recherche dans les sous-dossiers
                show_progress=True, # Affichage de la progression
                use_multithreading=True, # Traitement parallèle pour accélérer le chargement
                silent_errors=True # Ignore les fichiers qui ne peuvent pas être chargés
            )
            loaded_docs = loader.load()
            if loaded_docs:
                logger.info(f"Chargé {len(loaded_docs)} document(s) de type {config['glob']}")
                documents.extend(loaded_docs)
            else:
                 logger.warning(f"Aucun document trouvé pour le type {config['glob']}")
        except Exception as e:
            # Enregistre l'erreur mais continue le traitement des autres types
            logger.error(f"Erreur lors du chargement des fichiers {config['glob']} depuis {source_directory}: {e}", exc_info=True)

    # Vérification du résultat final
    if not documents:
        logger.warning(f"Aucun document n'a pu être chargé depuis {source_directory}")
    else:
        logger.info(f"Total de {len(documents)} documents chargés.")

    return documents

def split_documents(documents: List[Document]) -> List[Document]:
    """
    Découpe les documents chargés en plus petits fragments pour optimiser la recherche.
    Utilise des séparateurs adaptés aux textes arabes et français.
    
    Args:
        documents: Liste des documents à découper
        
    Returns:
        Liste des fragments de documents créés
    """
    logger.info(f"Découpage de {len(documents)} documents...")
    
    # Configuration du découpeur de texte
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,        # Taille maximale de chaque fragment
        chunk_overlap=100,      # Chevauchement entre fragments pour maintenir le contexte
        length_function=len,    # Fonction de calcul de la longueur
        is_separator_regex=False, # Utilise les séparateurs comme chaînes littérales
        separators=["\n\n", "\n", ". ", "، ", "؛ ", " ", ""] # Séparateurs adaptés à l'arabe et au français
    )
    
    # Découpage des documents
    texts = text_splitter.split_documents(documents)
    logger.info(f"Découpage terminé : {len(texts)} fragments créés.")
    return texts