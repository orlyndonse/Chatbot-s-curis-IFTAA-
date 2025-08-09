# indexer_rag.py
import os
import logging
import time

# Importez les fonctions nécessaires depuis vos modules RAG
from src.rag.loader import charger_documents, split_documents
from src.rag.vectorstore import add_documents_to_vectorstore, CHROMA_DB_PATH, COLLECTION_NAME

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Chemin vers le dossier contenant vos documents source
# Assurez-vous qu'il correspond à l'endroit où vous avez mis les fichiers
SOURCE_DOCS_PATH = os.path.join("data", "fiqh_docs")

def indexer():
    """
    Charge, découpe et indexe les documents dans ChromaDB.
    """
    logger.info("--- Démarrage du processus d'indexation RAG ---")

    # Vérifier si le dossier source existe
    if not os.path.isdir(SOURCE_DOCS_PATH):
        logger.error(f"Le dossier source '{SOURCE_DOCS_PATH}' n'existe pas. Veuillez créer ce dossier et y ajouter vos documents.")
        return

    # 1. Charger les documents
    start_time = time.time()
    logger.info(f"Étape 1/3 : Chargement des documents depuis '{SOURCE_DOCS_PATH}'...")
    try:
        documents = charger_documents(SOURCE_DOCS_PATH)
    except Exception as e:
        logger.error(f"Erreur lors du chargement des documents: {e}", exc_info=True)
        return
    if not documents:
        logger.warning("Aucun document n'a été chargé. Vérifiez le contenu du dossier source et les types de fichiers supportés.")
        return
    logger.info(f"Chargement terminé en {time.time() - start_time:.2f} secondes. {len(documents)} document(s) trouvé(s).")

    # 2. Découper les documents
    start_time = time.time()
    logger.info("Étape 2/3 : Découpage des documents...")
    try:
        split_docs = split_documents(documents)
    except Exception as e:
        logger.error(f"Erreur lors du découpage des documents: {e}", exc_info=True)
        return

    # --- AJOUT DEBUG ---
    logger.info(f"DEBUG: Nombre de morceaux après découpage: {len(split_docs)}")
    # -------------------

    if not split_docs:
         logger.warning("Aucun morceau n'a été généré après découpage.")
         return
    logger.info(f"Découpage terminé en {time.time() - start_time:.2f} secondes. {len(split_docs)} morceau(x) créé(s).") # Modifié pour correspondre au log DEBUG

    # 3. Ajouter les documents au Vector Store (ChromaDB)
    start_time = time.time()
    logger.info(f"Étape 3/3 : Ajout des documents au Vector Store ChromaDB (Collection: {COLLECTION_NAME}, Path: {CHROMA_DB_PATH})...")
    logger.warning("Cette étape peut prendre plusieurs minutes en fonction du volume de documents et de la puissance de votre machine...")

    # --- AJOUT DEBUG ---
    print("DEBUG: Juste avant d'appeler add_documents_to_vectorstore...")
    # -------------------
    try:
        add_documents_to_vectorstore(split_docs)
        # --- AJOUT DEBUG ---
        print("DEBUG: Appel à add_documents_to_vectorstore terminé.")
        # -------------------
    except Exception as e:
         # --- AJOUT DEBUG ---
         print(f"DEBUG: ERREUR interceptée dans indexer: {e}")
         # -------------------
         logger.error(f"Erreur lors de l'ajout des documents au vectorstore: {e}", exc_info=True)
         return
    # --- AJOUT DEBUG ---
    print("DEBUG: Après le bloc try/except de add_documents_to_vectorstore.")
    # -------------------
    logger.info(f"Ajout au vectorstore terminé en {time.time() - start_time:.2f} secondes.")

    logger.info("--- Processus d'indexation RAG terminé avec succès ! ---")
    logger.info(f"La base de données vectorielle devrait se trouver dans : {os.path.abspath(CHROMA_DB_PATH)}")

if __name__ == "__main__":
    # Assurez-vous que les variables d'environnement nécessaires (comme GOOGLE_API_KEY si nécessaire pour l'embedding) sont chargées
    # Si vous utilisez python-dotenv, vous pouvez le charger ici :
    # from dotenv import load_dotenv
    # load_dotenv()
    # --- AJOUT DEBUG ---
    print("DEBUG: Lancement du script indexer_rag.py")
    # -------------------
    indexer()
    # --- AJOUT DEBUG ---
    print("DEBUG: Fin du script indexer_rag.py")
    # -------------------