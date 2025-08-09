# src/rag/chain.py
import os
import logging
from typing import List, Tuple, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document as LangchainDocument

# Importe les fonctions/classes nécessaires depuis nos modules et config
from .vectorstore import get_filtered_retriever
from src.config import Config

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Template de Prompt (depuis le notebook) ---
# Ce template sera utilisé pour formuler la question finale au LLM avec le contexte trouvé
template_arabe = """أنت خبير في الفقه المالكي.

مهمتك هي الإجابة على الأسئلة المتعلقة بالفقه المالكي. يجب أن تكون جميع إجاباتك باللغة العربية الفصحى حصراً.

في حالة وجود إجابة في النصوص المتوفرة:
- قم بتقديم الإجابة مع ذكر المصدر
- اذكر الدليل إن وجد
- اذكر أقوال العلماء إن وجدت

في حالة عدم وجود إجابة في النصوص المتوفرة:
- قم بالتصريح بوضوح قائلاً: "هذه الإجابة من معرفة النموذج اللغوي وليست من النصوص المتوفرة"
- ثم قدم إجابة بناءً على معرفتك العامة بالمذهب المالكي

ملاحظة: يجب أن تكون جميع الإجابات باللغة العربية فقط.

السؤال: {question}
النصوص المتعلقة بالموضوع: {context}

الإجابة:"""

# --- Variable globale pour le LLM uniquement ---
_llm_instance = None

def get_llm():
    """Initialise (si nécessaire) et retourne l'instance du LLM."""
    global _llm_instance
    if _llm_instance is None:
        logger.info("Initialisation du LLM Google Generative AI (gemini-1.5-flash)...")
        if not Config.GEMINI_API_KEY:
            logger.error("La clé API Google (GEMINI_API_KEY) n'est pas configurée dans src/config.py ou les variables d'environnement.")
            raise ValueError("Clé API Google manquante.")
        try:
            _llm_instance = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0.2, # Faible température pour des réponses plus factuelles
                convert_system_message_to_human=True, # Bonne pratique pour certains modèles Gemini
                google_api_key=Config.GEMINI_API_KEY
            )
            logger.info("LLM initialisé avec succès.")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du LLM: {e}", exc_info=True)
            _llm_instance = None # Assure qu'on sait qu'il y a eu un échec
            raise # Relance l'erreur pour que l'appelant gère
    return _llm_instance

def initialize_rag_chain():
    """
    Initialise seulement le LLM au démarrage de l'application.
    Cette fonction remplace l'ancienne initialize_rag_chain().
    """
    logger.info("Initialisation du LLM au démarrage de l'application...")
    try:
        llm = get_llm()
        if llm is None:
            raise RuntimeError("Impossible d'initialiser le LLM.")
        logger.info("LLM prêt pour l'utilisation.")
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation du LLM au démarrage: {e}", exc_info=True)
        raise

def create_contextual_rag_chain(
    active_document_uids: List[str], 
    chat_history: List[Tuple[str, str]]
) -> Tuple[ConversationalRetrievalChain, int]:
    """
    Crée une chaîne RAG contextualisée pour une conversation spécifique.
    
    Args:
        active_document_uids: Liste des UIDs des documents actifs pour cette conversation
        chat_history: Historique de la conversation
    
    Returns:
        Tuple contenant la chaîne RAG et le nombre de documents actifs
    """
    logger.info(f"Création d'une chaîne RAG contextualisée avec {len(active_document_uids)} documents actifs")
    
    try:
        # 1. Obtenir le LLM
        llm = get_llm()
        if llm is None:
            raise RuntimeError("LLM non disponible.")

        # 2. Créer le retriever filtré
        retriever = get_filtered_retriever(active_document_uids, k=7)
        logger.info(f"Retriever filtré créé pour {len(active_document_uids)} documents")

        # 3. Créer le Prompt Template
        QA_PROMPT = PromptTemplate(
            template=template_arabe, 
            input_variables=["context", "question"]
        )

        # 4. Créer la Chaîne Conversationnelle RAG
        rag_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": QA_PROMPT},
            # verbose=True # Décommentez pour debug
        )
        
        logger.info("Chaîne RAG contextualisée créée avec succès")
        return rag_chain, len(active_document_uids)

    except Exception as e:
        logger.error(f"Erreur lors de la création de la chaîne RAG contextualisée: {e}", exc_info=True)
        raise

async def generate_contextual_rag_response(
    question: str,
    active_document_uids: List[str],
    chat_history: List[Tuple[str, str]]
) -> Tuple[str, Optional[List[LangchainDocument]], int]:
    """
    Génère une réponse RAG en utilisant uniquement les documents actifs de la conversation.
    
    Args:
        question: La question de l'utilisateur
        active_document_uids: Liste des UIDs des documents actifs
        chat_history: Historique de la conversation
    
    Returns:
        Tuple contenant (réponse, documents_sources, nombre_documents_actifs)
    """
    logger.info(f"Génération d'une réponse RAG contextualisée")
    logger.info(f"Question: {question[:100]}...")
    logger.info(f"Documents actifs: {len(active_document_uids)}")
    logger.info(f"Historique: {len(chat_history)} échanges")
    
    try:
        # Créer la chaîne RAG contextualisée
        rag_chain, doc_count = create_contextual_rag_chain(active_document_uids, chat_history)
        
        # Générer la réponse
        result = await rag_chain.ainvoke({
            "question": question,
            "chat_history": chat_history
        })
        
        ai_response_text = result.get("answer", "Désolé, une erreur est survenue.")
        source_documents = result.get("source_documents")
        
        logger.info(f"Réponse générée avec succès")
        if source_documents:
            logger.info(f"Sources utilisées: {len(source_documents)} documents")
            for i, doc in enumerate(source_documents):
                logger.debug(f"Source {i+1}: {doc.metadata}")
        
        return ai_response_text, source_documents, doc_count

    except Exception as e:
        logger.error(f"Erreur lors de la génération de la réponse RAG contextualisée: {e}", exc_info=True)
        error_message = "Désolé, je n'ai pas pu traiter votre demande en raison d'une erreur interne."
        return error_message, None, len(active_document_uids)