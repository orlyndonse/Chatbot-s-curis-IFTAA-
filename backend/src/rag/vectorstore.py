# src/rag/vectorstore.py
import os
import logging
from typing import List, Dict, Any, Optional
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from chromadb import PersistentClient
from chromadb.config import Settings

# Configuration des constantes pour la base de données vectorielle
CHROMA_DB_PATH = os.path.join(os.getcwd(), "chroma_db_fiqh") # Chemin de stockage de la base ChromaDB
COLLECTION_NAME = "fiqh_maliki" # Nom de la collection pour les documents de fiqh maliki
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2" # Modèle multilingue pour l'arabe et français

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variables globales pour les instances partagées (pattern singleton simple)
_chroma_client = None
_embedding_function = None

def get_embedding_function():
    """
    Initialise et retourne le modèle d'embedding multilingue.
    Utilise un pattern singleton pour éviter les réinitialisations multiples.
    
    Returns:
        Instance du modèle HuggingFace pour la génération d'embeddings
    """
    global _embedding_function
    if _embedding_function is None:
        logger.info(f"Initialisation du modèle d'embedding: {EMBEDDING_MODEL_NAME}")
        try:
            _embedding_function = HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL_NAME,
                # model_kwargs={'device': 'cuda'} # Décommentez si GPU disponible
                # encode_kwargs={'normalize_embeddings': False}
            )
            logger.info("Modèle d'embedding initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du modèle d'embedding: {e}", exc_info=True)
            raise
    return _embedding_function

def get_chroma_client():
    """
    Initialise et retourne le client ChromaDB persistant.
    Configure la base de données pour la persistance sur disque.
    
    Returns:
        Instance du client ChromaDB persistant
    """
    global _chroma_client
    if _chroma_client is None:
        logger.info(f"Initialisation du client ChromaDB persistant à : {CHROMA_DB_PATH}")
        try:
            # Création du dossier de stockage si nécessaire
            os.makedirs(os.path.dirname(CHROMA_DB_PATH), exist_ok=True)
            
            # Initialisation du client avec persistance et télémétrie désactivée
            _chroma_client = PersistentClient(
                path=CHROMA_DB_PATH, 
                settings=Settings(anonymized_telemetry=False)
            )
            logger.info("Client ChromaDB initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du client ChromaDB: {e}", exc_info=True)
            raise
    return _chroma_client

def get_vectorstore():
    """
    Retourne une instance du wrapper Langchain pour ChromaDB.
    Combine le client ChromaDB et le modèle d'embedding dans un wrapper Langchain.
    
    Returns:
        Instance du vectorstore Chroma configuré
    """
    # Récupération des instances des composants nécessaires
    _chroma_client_instance = get_chroma_client()
    _embedding_function_instance = get_embedding_function()

    # Vérification que les composants sont correctement initialisés
    if _chroma_client_instance is None or _embedding_function_instance is None:
         logger.error("Erreur: Le client ChromaDB ou la fonction d'embedding n'a pas pu être initialisé.")
         raise RuntimeError("Impossible d'initialiser ChromaDB ou l'embedding.")

    try:
        # Création du wrapper Langchain avec les composants initialisés
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

def get_filtered_retriever(active_document_uids: List[str], k: int = 7):
    """
    Crée un retriever qui recherche uniquement dans les documents spécifiés.
    Utilise le filtrage par UID de document pour limiter la recherche.
    
    Args:
        active_document_uids: Liste des identifiants uniques des documents à inclure
        k: Nombre de fragments de documents à récupérer
    
    Returns:
        Retriever configuré avec filtrage par documents
    """
    logger.info(f"Création d'un retriever filtré pour {len(active_document_uids)} documents actifs")
    
    vectorstore = get_vectorstore()
    
    # Gestion du cas où aucun document n'est spécifié
    if not active_document_uids:
        logger.warning("Aucun document actif fourni - création d'un retriever vide")
        return vectorstore.as_retriever(
            search_kwargs={
                "k": k,
                "filter": {"document_uid": {"$in": ["invalid_id_placeholder"]}}  # Ne correspondra à rien
            }
        )
    
    # Création du filtre pour ChromaDB utilisant les UIDs spécifiés
    filter_criteria = {"document_uid": {"$in": active_document_uids}}
    logger.debug(f"Critères de filtre: {filter_criteria}")
    
    return vectorstore.as_retriever(
        search_kwargs={
            "k": k,
            "filter": filter_criteria,
            # Option : Ajouter un seuil de score si nécessaire
            # "score_threshold": 0.7
        }
    )

def add_documents_to_vectorstore(documents: List[Document], document_uid: str = None):
    """
    Ajoute une liste de documents (découpés) au Vector Store ChromaDB.
    Enrichit les métadonnées avec l'UID du document pour permettre le filtrage.
    
    Args:
        documents: Liste des fragments de documents à ajouter
        document_uid: Identifiant unique du document source (pour le filtrage)
    """
    if not documents:
        logger.warning("Aucun document à ajouter au vectorstore.")
        return

    try:
        # Récupération du vectorstore configuré
        vectorstore = get_vectorstore()
        logger.info(f"Ajout de {len(documents)} fragments de documents à la collection '{COLLECTION_NAME}'...")

        # Enrichissement des métadonnées pour le filtrage par document
        for i, doc in enumerate(documents):
            if document_uid:
                if not doc.metadata:
                    doc.metadata = {}
                # Ajout de l'UID du document dans les métadonnées pour le filtrage
                doc.metadata['document_uid'] = document_uid
                logger.debug(f"Fragment {i}: ajout document_uid={document_uid} dans les métadonnées")
        
        # Génération d'identifiants uniques pour chaque fragment
        ids = [f"{doc.metadata.get('document_uid', 'unknown')}_{i}" for i, doc in enumerate(documents)]
        
        # Ajout des documents au vectorstore (l'embedding est géré automatiquement)
        vectorstore.add_documents(documents=documents, ids=ids)
        
        # Information sur le nombre total d'éléments dans la collection
        logger.info(f"Ajout terminé. La collection contient maintenant {vectorstore._collection.count()} éléments.")

    except Exception as e:
        logger.error(f"Erreur lors de l'ajout des documents au vectorstore: {e}", exc_info=True)
        raise