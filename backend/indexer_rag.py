# indexer_rag.py
import os
import logging
import time

# Importation des modules RAG pour le traitement des documents
from src.rag.loader import charger_documents, split_documents
from src.rag.vectorstore import add_documents_to_vectorstore, CHROMA_DB_PATH, COLLECTION_NAME

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Chemin vers le dossier contenant les documents sources à indexer
SOURCE_DOCS_PATH = os.path.join("data", "fiqh_docs")

def indexer():
    """
    Processus complet d'indexation des documents :
    1. Charge les documents depuis le dossier source
    2. Découpe les documents en fragments pour optimiser la recherche
    3. Indexe les fragments dans la base de données vectorielle ChromaDB
    """
    logger.info("--- Démarrage du processus d'indexation RAG ---")

    # Vérification de l'existence du dossier source
    if not os.path.isdir(SOURCE_DOCS_PATH):
        logger.error(f"Le dossier source '{SOURCE_DOCS_PATH}' n'existe pas. Veuillez créer ce dossier et y ajouter vos documents.")
        return

    # Étape 1 : Chargement des documents depuis le système de fichiers
    start_time = time.time()
    logger.info(f"Étape 1/3 : Chargement des documents depuis '{SOURCE_DOCS_PATH}'...")
    try:
        documents = charger_documents(SOURCE_DOCS_PATH)
    except Exception as e:
        logger.error(f"Erreur lors du chargement des documents: {e}", exc_info=True)
        return
    
    # Vérification que des documents ont été trouvés
    if not documents:
        logger.warning("Aucun document n'a été chargé. Vérifiez le contenu du dossier source et les types de fichiers supportés.")
        return
    logger.info(f"Chargement terminé en {time.time() - start_time:.2f} secondes. {len(documents)} document(s) trouvé(s).")

    # Étape 2 : Découpage des documents en fragments plus petits
    start_time = time.time()
    logger.info("Étape 2/3 : Découpage des documents...")
    try:
        split_docs = split_documents(documents)
    except Exception as e:
        logger.error(f"Erreur lors du découpage des documents: {e}", exc_info=True)
        return

    logger.info(f"Nombre de fragments après découpage: {len(split_docs)}")

    # Vérification que le découpage a produit des résultats
    if not split_docs:
         logger.warning("Aucun fragment n'a été généré après découpage.")
         return
    logger.info(f"Découpage terminé en {time.time() - start_time:.2f} secondes. {len(split_docs)} fragment(s) créé(s).")

    # Étape 3 : Indexation dans la base de données vectorielle
    start_time = time.time()
    logger.info(f"Étape 3/3 : Ajout des documents au Vector Store ChromaDB (Collection: {COLLECTION_NAME}, Path: {CHROMA_DB_PATH})...")
    logger.warning("Cette étape peut prendre plusieurs minutes en fonction du volume de documents et de la puissance de votre machine...")

    try:
        # Ajout des fragments au vectorstore avec génération automatique des embeddings
        add_documents_to_vectorstore(split_docs)
    except Exception as e:
         logger.error(f"Erreur lors de l'ajout des documents au vectorstore: {e}", exc_info=True)
         return
    
    logger.info(f"Ajout au vectorstore terminé en {time.time() - start_time:.2f} secondes.")

    logger.info("--- Processus d'indexation RAG terminé avec succès ! ---")
    logger.info(f"La base de données vectorielle se trouve dans : {os.path.abspath(CHROMA_DB_PATH)}")

if __name__ == "__main__":
    # Point d'entrée du script d'indexation
    # Note : Assurez-vous que les variables d'environnement nécessaires sont configurées
    # (comme GOOGLE_API_KEY si requis pour les embeddings)
    # Pour charger un fichier .env, décommentez les lignes suivantes :
    # from dotenv import load_dotenv
    # load_dotenv()
    
    indexer()