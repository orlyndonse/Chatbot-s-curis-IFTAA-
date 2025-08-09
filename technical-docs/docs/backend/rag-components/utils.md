---
sidebar_position: 4
title: Utilitaires RAG (src/rag/utils.py)
---

# Utilitaires RAG (`src/rag/utils.py`)

Le fichier `src/rag/utils.py` contient des fonctions utilitaires et des classes spécifiques qui supportent le fonctionnement du pipeline RAG, notamment le prétraitement du texte arabe pour l'améliorer avant l'indexation et la recherche.

## Classe `ArabicTextLoader`

Cette classe hérite de `BaseLoader` de Langchain et est conçue pour charger le contenu de fichiers texte (`.txt`) tout en appliquant un prétraitement spécifique au texte arabe.

```python
# Extrait de Code_Source/backend/src/rag/utils.py
from langchain_community.document_loaders.base import BaseLoader
from langchain_core.documents import Document
from typing import List, Iterator
import logging

# ... (fonctions de prétraitement) ...

class ArabicTextLoader(BaseLoader):
    """Charge un fichier texte en arabe et applique le prétraitement."""

    def __init__(self, file_path: str, encoding: str = "utf-8"):
        self.file_path = file_path
        self.encoding = encoding

    def lazy_load(self) -> Iterator[Document]:
        try:
            with open(self.file_path, "r", encoding=self.encoding) as f:
                text = f.read()
            
            # Appliquer le prétraitement au texte
            processed_text = preprocess_arabic_text_for_search(text) # Fonction de prétraitement
            
            metadata = {"source": self.file_path}
            yield Document(page_content=processed_text, metadata=metadata)
        except Exception as e:
            logging.error(f"Erreur lors du chargement du fichier {self.file_path}: {e}", exc_info=True)
            # Retourne un itérateur vide en cas d'erreur pour ne pas bloquer le processus
            # pour les autres fichiers si silent_errors=True est utilisé dans DirectoryLoader.
            return iter([])

    def load(self) -> List[Document]:
        return list(self.lazy_load())
```

### Héritage et Initialisation

- **Héritage** : Hérite de `BaseLoader` pour s'intégrer avec les mécanismes de chargement de documents de Langchain (comme `DirectoryLoader`)
- **Constructeur** : Prend le chemin du fichier (`file_path`) et l'encodage (par défaut `utf-8`)

### Méthodes principales

**`lazy_load()`** :
- Lit le contenu du fichier texte
- Appelle la fonction `preprocess_arabic_text_for_search(text)` pour nettoyer et normaliser le texte arabe
- Crée un objet `Document` de Langchain avec le texte prétraité et des métadonnées (la source étant le chemin du fichier)
- Gère les exceptions lors de la lecture du fichier et retourne un itérateur vide en cas d'erreur pour permettre à `DirectoryLoader` de continuer avec d'autres fichiers si `silent_errors` est activé

**`load()`** :
- Implémentation standard qui convertit l'itérateur de `lazy_load()` en une liste de `Document`

**Utilisation** : Cette classe est utilisée par `DirectoryLoader` dans `src/rag/loader.py` pour charger les fichiers `.txt`.

## Fonctions de Prétraitement du Texte Arabe

Le cœur de ce fichier réside dans ses fonctions de nettoyage et de normalisation du texte arabe, conçues pour améliorer la qualité des embeddings et de la recherche sémantique.

### 1. `normalize_arabic_text(text)`

```python
# Extrait de Code_Source/backend/src/rag/utils.py
def normalize_arabic_text(text: str) -> str:
    # ... (implémentation détaillée avec expressions régulières) ...
    text = re.sub(r"[إأآا]", "ا", text)
    text = re.sub(r"ى", "ي", text)
    text = re.sub(r"ة", "ه", text)
    text = re.sub(r"ـ", "", text) # Suppression des tatweel/kashida
    # ... (autres normalisations) ...
    return text
```

**Objectif** : Unifier différentes formes de caractères arabes pour une représentation standard.

**Opérations typiques** :
- Normalisation des variantes de l'Alef (إ, أ, آ) en Alef simple (ا)
- Normalisation du Alef Maqsura (ى) en Ya (ي)
- Normalisation du Ta Marbuta (ة) en Ha (ه) (peut être contextuel, à utiliser avec prudence selon le besoin)
- Suppression des kashida/tatweel (caractères d'allongement)

### 2. `remove_diacritics(text)`

```python
# Extrait de Code_Source/backend/src/rag/utils.py
def remove_diacritics(text: str) -> str:
    arabic_diacritics = re.compile(r"""
                                 ّ    | # Shadda
                                 َ    | # Fatha
                                 ً    | # Tanwin Fath
                                 ُ    | # Damma
                                 ٌ    | # Tanwin Damm
                                 ِ    | # Kasra
                                 ٍ    | # Tanwin Kasr
                                 ْ    | # Sukun
                                 ـ     # Tatweel/Kashida (peut aussi être géré dans normalize)
                             """, re.VERBOSE)
    text = re.sub(arabic_diacritics, '', text)
    return text
```

**Objectif** : Supprimer les signes diacritiques (harakat) du texte arabe. Cela peut aider à la recherche car la présence ou l'absence de diacritiques peut varier.

**Fonctionnement** : Utilise une expression régulière pour identifier et supprimer les diacritiques courants.

### 3. `remove_punctuations(text)`

```python
# Extrait de Code_Source/backend/src/rag/utils.py
def remove_punctuations(text: str) -> str:
    arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!"…"–ـ'''
    english_punctuations = string.punctuation
    punctuations_list = arabic_punctuations + english_punctuations
    translator = str.maketrans('', '', punctuations_list)
    return text.translate(translator)
```

**Objectif** : Supprimer les signes de ponctuation arabes et anglais.

**Fonctionnement** : Définit des listes de ponctuations et utilise `str.translate` pour les supprimer.

### 4. `remove_extra_spaces(text)`

```python
# Extrait de Code_Source/backend/src/rag/utils.py
def remove_extra_spaces(text: str) -> str:
    text = re.sub(r'\s+', ' ', text).strip()
    return text
```

**Objectif** : Remplacer les séquences d'espaces multiples par un seul espace et supprimer les espaces en début et fin de chaîne.

### 5. `preprocess_arabic_text_for_search(text)`

Cette fonction orchestre l'application des étapes de prétraitement précédentes dans un ordre logique.

```python
# Extrait de Code_Source/backend/src/rag/utils.py
def preprocess_arabic_text_for_search(text: str) -> str:
    if not text:
        return ""
    text = remove_diacritics(text)
    text = normalize_arabic_text(text)
    # La suppression de la ponctuation est commentée dans le code source fourni.
    # Si elle était activée : text = remove_punctuations(text)
    text = remove_extra_spaces(text)
    return text
```

**Pipeline de traitement** :
1. Appelle `remove_diacritics`
2. Appelle `normalize_arabic_text`
3. Appelle `remove_extra_spaces`

**Note importante** : Dans le code source fourni, l'appel à `remove_punctuations` est commenté. Si cette étape est souhaitée, elle devrait être décommentée.

## Conclusion

Ces utilitaires, en particulier `ArabicTextLoader` et `preprocess_arabic_text_for_search`, sont essentiels pour assurer que les données textuelles en arabe sont dans un format optimal avant d'être utilisées par le modèle d'embedding et le système de recherche sémantique.

---
On va passer directement à la section [Pipeline RAG Détaillé](../).