---
sidebar_position: 4
title: Utilitaires RAG (src/rag/utils.py)
---

# Utilitaires RAG (`src/rag/utils.py`)

Le fichier `src/rag/utils.py` contient des fonctions utilitaires et des classes spécifiques qui supportent le fonctionnement du pipeline RAG, notamment le prétraitement du texte arabe pour l'améliorer avant l'indexation et la recherche.

## Classe `ArabicTextLoader`

Cette classe hérite de `TextLoader` de Langchain et est conçue pour charger le contenu de fichiers texte (`.txt`) tout en appliquant un prétraitement spécifique au texte arabe.

```python
from langchain_community.document_loaders import TextLoader
from typing import List
from langchain.schema import Document

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
```

### Héritage et Initialisation

- **Héritage** : Hérite de `TextLoader` pour s'intégrer avec les mécanismes de chargement de documents de Langchain (comme `DirectoryLoader`)
- **Constructeur** : Utilise le constructeur de `TextLoader` qui prend le chemin du fichier (`file_path`) et l'encodage

### Méthodes principales

**`load()`** :
- Lit le contenu du fichier texte avec l'encodage spécifié (utf-8 par défaut)
- Appelle la fonction `pretraiter_texte_arabe(text)` pour nettoyer et normaliser le texte arabe
- Crée un objet `Document` de Langchain avec le texte prétraité et des métadonnées (la source étant le chemin du fichier)
- Gère les exceptions lors de la lecture du fichier avec un message d'erreur explicite

**Utilisation** : Cette classe est utilisée par `DirectoryLoader` dans `src/rag/loader.py` pour charger les fichiers `.txt`.

## Fonction de Prétraitement du Texte Arabe

Le cœur de ce fichier réside dans sa fonction de nettoyage et de normalisation du texte arabe, conçue pour améliorer la qualité des embeddings et de la recherche sémantique.

### `pretraiter_texte_arabe(text)`

```python
def pretraiter_texte_arabe(text: str) -> str:
    """
    Normalise, reshape et réordonne le texte arabe pour un affichage correct.
    """
    text = normalize_unicode(text)
    text = arabic_reshaper.reshape(text)
    text = get_display(text)
    return text
```

**Objectif** : Normaliser et reformater le texte arabe pour une représentation optimale.

**Étapes de traitement** :

1. **`normalize_unicode(text)`** :
   - Utilise `camel_tools.utils.normalize.normalize_unicode`
   - Normalise les caractères Unicode arabes
   - Unifie les différentes formes de caractères pour une représentation standard

2. **`arabic_reshaper.reshape(text)`** :
   - Utilise la bibliothèque `arabic_reshaper`
   - Connecte les lettres arabes de manière appropriée
   - Gère la forme contextuelle des caractères arabes (initiale, médiane, finale, isolée)

3. **`get_display(text)`** :
   - Utilise `bidi.algorithm.get_display`
   - Applique l'algorithme bidirectionnel pour l'affichage correct
   - Gère l'ordre de lecture de droite à gauche pour l'arabe

### Dépendances requises

Le module utilise plusieurs bibliothèques spécialisées pour le traitement du texte arabe :

```python
import arabic_reshaper
from bidi.algorithm import get_display
from camel_tools.utils.normalize import normalize_unicode
```

- **`arabic_reshaper`** : Pour la connexion correcte des lettres arabes
- **`bidi`** : Pour la gestion de l'affichage bidirectionnel
- **`camel_tools`** : Boîte à outils complète pour le traitement de l'arabe

## Fonctionnement dans le Pipeline

### Intégration avec le Chargement

1. **Appel par DirectoryLoader** : Le `DirectoryLoader` dans `loader.py` utilise `ArabicTextLoader` pour les fichiers `.txt`
2. **Traitement automatique** : Chaque fichier texte arabe est automatiquement prétraité lors du chargement
3. **Préservation des métadonnées** : Les informations sur la source du document sont conservées

### Amélioration de la Recherche

Le prétraitement du texte arabe améliore significativement :
- **Qualité des embeddings** : Un texte normalisé produit de meilleurs vecteurs de représentation
- **Consistance** : Différentes écritures du même texte sont normalisées vers une forme standard
- **Recherche sémantique** : Une meilleure correspondance entre les questions et les documents

### Impact sur l'Affichage

- **Affichage correct** : Le texte arabe s'affiche correctement dans l'interface utilisateur
- **Lisibilité** : La connexion appropriée des lettres améliore la lisibilité
- **Bidirectionnalité** : Gestion correcte du mélange de texte arabe (droite à gauche) et latin (gauche à droite)

## Avantages de l'Approche

### Spécialisation Linguistique
- **Optimisation pour l'arabe** : Traitement spécifique aux particularités de l'écriture arabe
- **Bibliothèques spécialisées** : Utilisation d'outils dédiés au traitement de l'arabe
- **Qualité professionnelle** : Respect des standards d'affichage et de traitement du texte arabe

### Intégration Transparente
- **Compatible Langchain** : S'intègre parfaitement avec l'écosystème Langchain
- **Traitement automatique** : Aucune intervention manuelle nécessaire
- **Préservation des métadonnées** : Maintient toutes les informations sur les documents

### Extensibilité
- **Modularité** : La fonction `pretraiter_texte_arabe()` peut être utilisée indépendamment
- **Personnalisation** : Facile d'ajouter des étapes de prétraitement supplémentaires
- **Réutilisabilité** : Le même prétraitement peut être appliqué à d'autres types de documents

Ce module est donc essentiel pour assurer que les données textuelles en arabe sont dans un format optimal avant d'être utilisées par le modèle d'embedding et le système de recherche sémantique du pipeline RAG.

---

Après avoir vu les utilitaires, nous pouvons maintenant examiner la [Gestion du Vector Store](../rag-components/vectorstore.md) (src/rag/vectorstore.py) pour comprendre comment les documents prétraités sont stockés et indexés.