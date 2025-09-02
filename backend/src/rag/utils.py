import arabic_reshaper
from bidi.algorithm import get_display
from camel_tools.utils.normalize import normalize_unicode
from langchain_community.document_loaders import TextLoader
from typing import List
from langchain.schema import Document

def pretraiter_texte_arabe(text: str) -> str:
    """
    Applique un prétraitement complet au texte arabe pour un affichage et traitement corrects.
    
    Étapes du traitement :
    1. Normalisation Unicode pour standardiser les caractères
    2. Reshape des caractères arabes pour la liaison correcte des lettres
    3. Réorganisation bidirectionnelle pour l'affichage correct
    
    Args:
        text: Texte arabe brut à traiter
        
    Returns:
        Texte arabe prétraité et correctement formaté
    """
    # Normalisation des caractères Unicode arabes
    text = normalize_unicode(text)
    
    # Reshape pour la liaison correcte des lettres arabes
    text = arabic_reshaper.reshape(text)
    
    # Réorganisation bidirectionnelle pour l'affichage correct
    text = get_display(text)
    
    return text

class ArabicTextLoader(TextLoader):
    """
    Chargeur de documents texte spécialisé pour les fichiers contenant du texte arabe.
    Hérite de TextLoader et applique automatiquement le prétraitement arabe.
    """
    
    def load(self) -> List[Document]:
        """
        Charge le fichier texte et applique le prétraitement arabe au contenu.
        
        Returns:
            Liste contenant un document avec le texte prétraité et ses métadonnées
            
        Raises:
            RuntimeError: Si le fichier ne peut pas être lu
        """
        try:
            # Lecture du fichier avec l'encodage spécifié ou UTF-8 par défaut
            with open(self.file_path, 'r', encoding=self.encoding or 'utf-8') as f:
                text = f.read()
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la lecture du fichier {self.file_path}: {e}") from e

        # Application du prétraitement spécialisé pour l'arabe
        processed_text = pretraiter_texte_arabe(text)

        # Création des métadonnées avec le chemin source
        metadata = {"source": self.file_path}
        
        return [Document(page_content=processed_text, metadata=metadata)]