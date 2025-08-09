# src/rag/vectorstore.py
import os
import logging
from typing import List, Dict, Any, Optional
from langchain.schema import Document
# Utiliser les nouveaux imports après installation
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from chromadb import PersistentClient # Pour la persistance
from chromadb.config import Settings

# --- Constantes de Configuration (Pourraient aller dans config.py) ---
# Mettez le chemin où vous voulez stocker la DB Chroma sur votre serveur
CHROMA_DB_PATH = os.path.join(os.getcwd(), "chroma_db_fiqh")
COLLECTION_NAME = "fiqh_maliki"
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
# -------------------------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variable globale pour le client Chroma (gestion simple, pourrait être améliorée)
# avec un vrai singleton ou via l'injection de dépendances FastAPI
_chroma_client = None
_embedding_function = None

def get_embedding_function():
    """Initialise et retourne le modèle d'embedding."""
    global _embedding_function
    if _embedding_function is None:
        # --- AJOUT DEBUG ---
        print("DEBUG: vectorstore.py - Entrée dans get_embedding_function")
        # -------------------
        logger.info(f"Initialisation du modèle d'embedding: {EMBEDDING_MODEL_NAME}")
        try:
            _embedding_function = HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL_NAME,
                # model_kwargs={'device': 'cuda'} # Décommentez si vous avez un GPU et CUDA configuré
                # encode_kwargs={'normalize_embeddings': False}
            )
            # --- AJOUT DEBUG ---
            print("DEBUG: vectorstore.py - HuggingFaceEmbeddings initialisé")
            # -------------------
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du modèle d'embedding: {e}", exc_info=True)
            # --- AJOUT DEBUG ---
            print(f"DEBUG: vectorstore.py - ERREUR dans get_embedding_function: {e}")
            # -------------------
            raise
    return _embedding_function

def get_chroma_client():
    """Initialise et retourne le client ChromaDB persistant."""
    global _chroma_client
    if _chroma_client is None:
        logger.info(f"Initialisation du client ChromaDB persistant à : {CHROMA_DB_PATH}")
        try:
            # S'assure que le dossier parent existe si besoin, bien que os.getcwd() existe toujours
            os.makedirs(os.path.dirname(CHROMA_DB_PATH), exist_ok=True)
            # Initialise le client persistant
            _chroma_client = PersistentClient(path=CHROMA_DB_PATH, settings=Settings(anonymized_telemetry=False))
            logger.info("Client ChromaDB initialisé.")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du client ChromaDB: {e}", exc_info=True)
            raise # Relance l'erreur pour arrêter le processus si Chroma ne peut être initialisé
    return _chroma_client

def get_vectorstore():
    """Retourne une instance du wrapper Langchain Chroma."""
    # --- AJOUT DEBUG ---
    print("DEBUG: vectorstore.py - Entrée dans get_vectorstore")
    # -------------------
    _chroma_client_instance = get_chroma_client()
    # --- AJOUT DEBUG ---
    print("DEBUG: vectorstore.py - get_chroma_client OK dans get_vectorstore")
    # -------------------
    _embedding_function_instance = get_embedding_function()
    # --- AJOUT DEBUG ---
    print("DEBUG: vectorstore.py - get_embedding_function OK dans get_vectorstore")
    # -------------------

    if _chroma_client_instance is None or _embedding_function_instance is None:
         logger.error("Erreur: Le client ChromaDB ou la fonction d'embedding n'a pas pu être initialisé.")
         print("DEBUG: vectorstore.py - ERREUR: Client Chroma ou Embedding func est None dans get_vectorstore") # <--- AJOUTER
         raise RuntimeError("Impossible d'initialiser ChromaDB ou l'embedding.")

    try:
        vectorstore = Chroma(
            client=_chroma_client_instance,
            collection_name=COLLECTION_NAME,
            embedding_function=_embedding_function_instance # Passer la fonction chargée
        )
        logger.info("Wrapper VectorStore LangChain Chroma initialisé.")
        # --- AJOUT DEBUG ---
        print("DEBUG: vectorstore.py - Chroma wrapper initialisé")
        # -------------------
        return vectorstore
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation du wrapper Chroma Langchain: {e}", exc_info=True)
        print(f"DEBUG: vectorstore.py - ERREUR lors de l'init Chroma wrapper: {e}") # <--- AJOUTER
        raise

def get_filtered_retriever(active_document_uids: List[str], k: int = 7):
    """
    Creates a retriever that only searches within specified documents.
    
    Args:
        active_document_uids: List of document UIDs to include in search
        k: Number of document chunks to retrieve
    
    Returns:
        Configured retriever with document filtering
    """
    logger.info(f"Creating filtered retriever for {len(active_document_uids)} active documents")
    
    vectorstore = get_vectorstore()
    
    if not active_document_uids:
        logger.warning("No active documents provided - creating empty retriever")
        return vectorstore.as_retriever(
            search_kwargs={
                "k": k,
                "filter": {"document_uid": {"$in": ["invalid_id_placeholder"]}}  # Will match nothing
            }
        )
    
    # Create filter for ChromaDB
    filter_criteria = {"document_uid": {"$in": active_document_uids}}
    logger.debug(f"Filter criteria: {filter_criteria}")
    
    return vectorstore.as_retriever(
        search_kwargs={
            "k": k,
            "filter": filter_criteria,
            # Optional: Add score threshold if needed
            # "score_threshold": 0.7
        }
    )

def add_documents_to_vectorstore(documents: List[Document], document_uid: str = None):
    """
    Ajoute une liste de documents (découpés) au Vector Store ChromaDB.
    MODIFIÉ: Ajoute le document_uid dans les métadonnées pour le filtrage.
    """
    # --- AJOUT DEBUG ---
    print("DEBUG: vectorstore.py - Entrée dans add_documents_to_vectorstore")
    # -------------------
    if not documents:
        logger.warning("Aucun document à ajouter au vectorstore.")
        print("DEBUG: vectorstore.py - Aucun document reçu dans add_documents_to_vectorstore") # <--- AJOUTER
        return

    # --- AJOUT DEBUG ---
    print("DEBUG: vectorstore.py - Appel de get_vectorstore...")
    # -------------------
    try:
        vectorstore = get_vectorstore() # Récupère le wrapper Langchain
        # --- AJOUT DEBUG ---
        print("DEBUG: vectorstore.py - get_vectorstore terminé avec succès.")
        # -------------------
    except Exception as e:
         logger.error(f"Erreur lors de la récupération du vectorstore: {e}", exc_info=True)
         print(f"DEBUG: vectorstore.py - ERREUR dans get_vectorstore : {e}") # <--- AJOUTER
         raise # Arrête si on ne peut pas obtenir le vectorstore

    # --- AJOUT DEBUG ---
    # Cette revérification est redondante si get_vectorstore a réussi, mais ajoutons un print
    print("DEBUG: vectorstore.py - Appel de get_embedding_function (vérification)...")
    # -------------------
    try:
        embedding_function = get_embedding_function() # S'assure que le modèle est chargé
         # --- AJOUT DEBUG ---
        print("DEBUG: vectorstore.py - get_embedding_function (vérification) terminé.")
        # -------------------
    except Exception as e:
         logger.error(f"Erreur lors de la récupération de embedding_function: {e}", exc_info=True)
         print(f"DEBUG: vectorstore.py - ERREUR dans get_embedding_function (vérification) : {e}") # <--- AJOUTER
         raise # Arrête si on ne peut pas obtenir l'embedding function

    logger.info(f"Ajout de {len(documents)} morceaux de documents à la collection '{COLLECTION_NAME}'...")
    # --- AJOUT DEBUG ---
    print(f"DEBUG: vectorstore.py - Prêt à ajouter {len(documents)} morceaux...")
    # -------------------

    try:
        # --- AJOUT DEBUG ---
        print("DEBUG: vectorstore.py - Génération des IDs...")
        # -------------------
        
        # MODIFICATION IMPORTANTE: Enrichir les métadonnées
        for i, doc in enumerate(documents):
            if document_uid:
                # Ajouter l'UID du document dans les métadonnées
                if not doc.metadata:
                    doc.metadata = {}
                doc.metadata['document_uid'] = document_uid
                logger.debug(f"Document chunk {i}: ajout document_uid={document_uid} dans metadata")
        
        # Générer des IDs uniques pour chaque morceau
        ids = [f"{doc.metadata.get('document_uid', 'unknown')}_{i}" for i, doc in enumerate(documents)]
        # --- AJOUT DEBUG ---
        print(f"DEBUG: vectorstore.py - IDs générés (exemple premier ID: {ids[0] if ids else 'N/A'})")
        print("DEBUG: vectorstore.py - Appel de vectorstore.add_documents...")
        # -------------------

        # Utiliser add_documents qui gère l'embedding en interne
        vectorstore.add_documents(documents=documents, ids=ids) # embedding_function est déjà dans l'objet vectorstore
        # --- AJOUT DEBUG ---
        print("DEBUG: vectorstore.py - vectorstore.add_documents terminé.")
        # -------------------
        logger.info(f"Ajout terminé. La collection contient maintenant {vectorstore._collection.count()} éléments.")

    except Exception as e:
        # --- AJOUT DEBUG ---
        print(f"DEBUG: vectorstore.py - ERREUR lors de l'ajout: {e}")
        # -------------------
        logger.error(f"Erreur lors de l'ajout des documents au vectorstore: {e}", exc_info=True)
        raise # Relancer l'exception pour que indexer_rag.py la capture