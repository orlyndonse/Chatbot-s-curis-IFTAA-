import logging
from typing import List, Optional, Tuple
import asyncio

from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document as LangchainDocument
from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import Config
from .vectorstore import get_filtered_retriever

import re 

# Configuration du système de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Template de prompt pour le modèle en langue arabe
# Template de prompt pour le modèle en langue arabe AVEC FORMATAGE MARKDOWN
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

# Instance globale du modèle LLM (pattern singleton)
_llm_instance = None

def get_llm():
    """Initialise et retourne l'instance du LLM (pattern singleton)."""
    global _llm_instance
    if _llm_instance is None:
        logger.info("Initialisation du LLM Google Generative AI (gemini-1.5-flash)...")
        if not Config.GEMINI_API_KEY:
            raise ValueError("Clé API Google (GEMINI_API_KEY) manquante.")
        try:
            _llm_instance = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0.2,
                convert_system_message_to_human=True,
                google_api_key=Config.GEMINI_API_KEY,
                streaming=True  # Activer explicitement
            )
            logger.info("LLM initialisé avec succès.")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du LLM: {e}", exc_info=True)
            raise
    return _llm_instance

def initialize_rag_chain():
    """Initialise le LLM au démarrage de l'application."""
    logger.info("Pré-initialisation du LLM...")
    get_llm()

def create_contextual_rag_chain(
    active_document_uids: List[str]
) -> Tuple[ConversationalRetrievalChain, int]:
    """
    Crée une chaîne RAG contextualisée pour une conversation spécifique.
    
    Args:
        active_document_uids: Liste des identifiants uniques des documents à utiliser
    
    Returns:
        Tuple contenant la chaîne RAG configurée et le nombre de documents actifs
    """
    logger.info(f"Création d'une chaîne RAG avec {len(active_document_uids)} documents actifs")
    try:
        llm = get_llm()
        retriever = get_filtered_retriever(active_document_uids, k=7)
        QA_PROMPT = PromptTemplate(template=template_arabe, input_variables=["context", "question"])

        rag_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": QA_PROMPT},
        )
        
        logger.info("Chaîne RAG contextualisée créée avec succès")
        return rag_chain, len(active_document_uids)
    except Exception as e:
        logger.error(f"Erreur lors de la création de la chaîne RAG: {e}", exc_info=True)
        raise

async def generate_contextual_rag_response(
    question: str,
    active_document_uids: List[str],
    chat_history: List[Tuple[str, str]]
) -> Tuple[str, Optional[List[LangchainDocument]], int]:
    """
    Génère une réponse RAG en utilisant uniquement les documents actifs de la conversation.
    
    Args:
        question: La question posée par l'utilisateur
        active_document_uids: Liste des identifiants des documents à consulter
        chat_history: Historique des échanges précédents
    
    Returns:
        Tuple contenant (réponse_générée, documents_sources_utilisés, nombre_documents_actifs)
    """
    logger.info(f"Génération d'une réponse RAG contextualisée")
    logger.info(f"Question: {question[:100]}...")
    logger.info(f"Documents actifs: {len(active_document_uids)}")
    logger.info(f"Historique: {len(chat_history)} échanges")
    
    try:
        rag_chain, doc_count = create_contextual_rag_chain(active_document_uids)
        
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
        logger.error(f"Erreur lors de la génération de la réponse RAG: {e}", exc_info=True)
        return "Désolé, je n'ai pas pu traiter votre demande.", None, len(active_document_uids)

def simulate_streaming(text: str, chunk_size: int = 80, delay: float = 0.08):
    """
    Version améliorée qui préserve la structure Markdown.
    """
    # Trouver les points naturels de rupture (fin de phrase, après ponctuation)
    sentences = re.split(r'([.!?]+\s+)', text)
    
    current_chunk = ""
    for i in range(0, len(sentences), 2):
        if i + 1 < len(sentences):
            sentence = sentences[i] + sentences[i + 1]
        else:
            sentence = sentences[i]
            
        if not sentence.strip():
            continue
            
        if len(current_chunk + sentence) > chunk_size and current_chunk:
            yield current_chunk.strip()
            current_chunk = sentence
        else:
            current_chunk += sentence
    
    if current_chunk.strip():
        yield current_chunk.strip()


async def stream_contextual_rag_response(
    question: str,
    active_document_uids: List[str],
    chat_history: List[Tuple[str, str]]
):
    """
    Génère une réponse RAG avec simulation de streaming.
    
    Args:
        question: La question posée par l'utilisateur
        active_document_uids: Liste des identifiants des documents à consulter
        chat_history: Historique des échanges précédents
    
    Yields:
        str: Chunks de la réponse simulant un streaming
    """
    logger.info(f"Début du streaming RAG pour la question: {question[:50]}...")
    
    try:
        # Génération de la réponse complète d'abord
        rag_chain, _ = create_contextual_rag_chain(active_document_uids)
        
        result = await rag_chain.ainvoke({
            "question": question,
            "chat_history": chat_history
        })
        
        ai_response_text = result.get("answer", "Désolé, une erreur est survenue.")
        logger.info(f"Réponse complète générée ({len(ai_response_text)} caractères)")
        
        # Simulation du streaming par chunks
        chunk_count = 0
        for chunk in simulate_streaming(ai_response_text, chunk_size=20, delay=0.05):
            chunk_count += 1
            logger.info(f"Streaming chunk {chunk_count}: '{chunk}' (length: {len(chunk)})")
            yield chunk
            await asyncio.sleep(0.05)  # Petit délai pour simuler le streaming
            
        logger.info(f"Streaming terminé - {chunk_count} chunks envoyés")
                    
    except Exception as e:
        logger.error(f"Erreur pendant le streaming de la réponse RAG: {e}", exc_info=True)
        yield "Désolé, une erreur interne est survenue."