import pytest
from unittest.mock import patch, mock_open
from src.rag.utils import pretraiter_texte_arabe, ArabicTextLoader
from langchain.schema import Document

def test_pretraiter_texte_arabe():
    """
    Teste le prétraitement du texte arabe avec différents cas.
    """
    # Cas normal
    texte_arabe = "مرحبا بكم في النظام"
    resultat = pretraiter_texte_arabe(texte_arabe)
    assert resultat is not None
    assert isinstance(resultat, str)
    assert len(resultat) > 0
    
    # Cas chaîne vide
    assert pretraiter_texte_arabe("") == ""
    
    # Cohérence (même entrée = même sortie)
    assert pretraiter_texte_arabe(texte_arabe) == pretraiter_texte_arabe(texte_arabe)

@patch("builtins.open", new_callable=mock_open, read_data="مرحبا بكم في النظام")
def test_arabic_text_loader_success(mock_file):
    """
    Teste le chargement réussi d'un fichier texte arabe.
    """
    loader = ArabicTextLoader("test_file.txt")
    documents = loader.load()
    
    assert isinstance(documents, list)
    assert len(documents) == 1
    assert isinstance(documents[0], Document)
    
    doc = documents[0]
    assert doc.page_content is not None
    assert isinstance(doc.page_content, str)
    assert doc.metadata["source"] == "test_file.txt"

@patch("builtins.open", side_effect=FileNotFoundError("File not found"))
def test_arabic_text_loader_error(mock_file):
    """
    Teste la gestion d'erreur du chargeur.
    """
    loader = ArabicTextLoader("missing_file.txt")
    
    with pytest.raises(RuntimeError) as excinfo:
        loader.load()
    
    assert "Erreur lors de la lecture du fichier" in str(excinfo.value)
    assert "missing_file.txt" in str(excinfo.value)