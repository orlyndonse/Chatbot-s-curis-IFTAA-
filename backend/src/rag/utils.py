# src/rag/utils.py
import arabic_reshaper
from bidi.algorithm import get_display
from camel_tools.utils.normalize import normalize_unicode
from langchain_community.document_loaders import TextLoader # On garde TextLoader ici pour ArabicTextLoader
from typing import List
from langchain.schema import Document

# Fonction pour prétraiter le texte arabe (directement depuis le notebook)
def pretraiter_texte_arabe(text: str) -> str:
    """
    Normalise, reshape et réordonne le texte arabe pour un affichage correct.
    """
    text = normalize_unicode(text)
    text = arabic_reshaper.reshape(text)
    text = get_display(text)
    return text

# Classe personnalisée pour charger les textes arabes (directement depuis le notebook)
# Note: Cette classe hérite de TextLoader, donc l'import est nécessaire ici.
class ArabicTextLoader(TextLoader):
    """
    Chargeur de documents texte qui applique un prétraitement spécifique à l'arabe.
    """
    def load(self) -> List[Document]:
        """Charge et prétraite le contenu du fichier."""
        try:
            with open(self.file_path, 'r', encoding=self.encoding or 'utf-8') as f:
                text = f.read()
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la lecture du fichier {self.file_path}: {e}") from e

        # Appliquer le prétraitement arabe
        processed_text = pretraiter_texte_arabe(text)

        metadata = {"source": self.file_path}
        return [Document(page_content=processed_text, metadata=metadata)]