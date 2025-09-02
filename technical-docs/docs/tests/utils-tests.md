---
sidebar_position: 3
title: Focus - Tester les Utilitaires
---

# Focus : Guide sur les Tests Unitaires Purs

En plus des tests d'intégration qui vérifient les endpoints API, le projet contient des **tests unitaires purs**. Ces tests sont plus simples, plus rapides et se concentrent sur une seule pièce de logique à la fois. Les fichiers `test_auth_utils.py` et `test_rag_utils.py` en sont de parfaits exemples.

## Qu'est-ce qu'un Test Unitaire Pur ?

Un test unitaire pur vérifie le comportement d'une fonction unique en isolation totale. Il ne dépend :
* Ni de l'application FastAPI.
* Ni d'une base de données.
* Ni de services externes.
* Souvent, il n'a même pas besoin de mocks.

Son but est de répondre à la question : "Si je donne *telle entrée* à cette fonction, est-ce que j'obtiens bien *telle sortie* ?"

## Exemple : `test_password_verification_logic`

Ce test se trouve dans `test_auth_utils.py` et valide les fonctions de hachage de mot de passe.

```python
# Fichier: tests/test_auth_utils.py

from src.auth.utils import generate_passwd_hash, verify_password

def test_password_verification_logic():
    password = "my_secure_password_123"
    hashed_password = generate_passwd_hash(password)

    # Scénario 1: Le mot de passe correct fonctionne
    assert verify_password(password, hashed_password) is True

    # Scénario 2: Un mot de passe incorrect échoue
    assert verify_password("wrong_password", hashed_password) is False
```

### Analyse de ce test :

* **Simple** : Il n'a besoin d'aucune fixture comme `test_client` ou `fake_service`. Il importe juste les fonctions qu'il veut tester.

* **Rapide** : Il s'exécute en quelques millisecondes car il n'y a pas de réseau, pas de base de données, juste du calcul pur.

* **Fiable** : Il teste la logique de base du hachage. Si ce test passe, nous sommes sûrs que cette brique fondamentale de notre système de sécurité fonctionne.

## Exemple : Tests RAG - `test_pretraiter_texte_arabe`

Ce test se trouve dans `test_rag_utils.py` et valide le prétraitement du texte arabe.

```python
# Fichier: tests/test_rag_utils.py

from src.rag.utils import pretraiter_texte_arabe

def test_pretraiter_texte_arabe():
    # Test avec du texte arabe contenant des diacritiques
    texte_avec_diacritiques = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
    texte_nettoye = pretraiter_texte_arabe(texte_avec_diacritiques)
    
    # Vérifier que les diacritiques ont été supprimés
    assert "ِ" not in texte_nettoye  # Kasra
    assert "ْ" not in texte_nettoye  # Sukun
    assert "َ" not in texte_nettoye  # Fatha
    assert "ٰ" not in texte_nettoye  # Alif khanjariya
    
    # Vérifier que le texte de base est préservé
    assert "بسم" in texte_nettoye
    assert "الله" in texte_nettoye
```

Ce test garantit que notre fonction de prétraitement :
* Supprime correctement les diacritiques arabes
* Préserve le texte principal
* Fonctionne de manière consistante

## Importance de ces Tests

Tester les fonctions utilitaires de cette manière est une bonne pratique car :

### 1. Isolation des Bugs
Si un test d'intégration complexe échoue, le problème peut venir de la route, du service, ou de la base de données. Si un test unitaire comme celui-ci échoue, nous savons exactement où se trouve le bug : dans la fonction testée.

### 2. Robustesse
En garantissant que toutes nos petites fonctions utilitaires sont fiables, nous construisons une application plus robuste et plus facile à déboguer.

### 3. Rapidité de Développement
Ces tests s'exécutent très rapidement, permettant un feedback immédiat lors du développement.

### 4. Documentation Vivante
Ces tests servent de documentation sur le comportement attendu de chaque fonction utilitaire.

## Bonnes Pratiques pour les Tests Unitaires Purs

### 1. Tester les Cas Limites
```python
def test_hash_password_edge_cases():
    # Test avec mot de passe vide
    empty_hash = generate_passwd_hash("")
    assert verify_password("", empty_hash) is True
    assert verify_password("not_empty", empty_hash) is False
    
    # Test avec mot de passe très long
    long_password = "a" * 1000
    long_hash = generate_passwd_hash(long_password)
    assert verify_password(long_password, long_hash) is True
```

### 2. Tester Plusieurs Scénarios
```python
def test_pretraiter_texte_arabe_scenarios():
    # Scénario 1: Texte sans diacritiques
    texte_simple = "السلام عليكم"
    assert pretraiter_texte_arabe(texte_simple) == "السلام عليكم"
    
    # Scénario 2: Texte vide
    assert pretraiter_texte_arabe("") == ""
    
    # Scénario 3: Texte avec espaces supplémentaires
    texte_espaces = "  النص   مع   مسافات  "
    resultat = pretraiter_texte_arabe(texte_espaces)
    assert resultat.strip() == "النص مع مسافات"
```

### 3. Noms de Tests Descriptifs
Utilisez des noms qui décrivent clairement ce qui est testé :
- `test_password_verification_with_correct_password`
- `test_arabic_text_preprocessing_removes_diacritics`
- `test_empty_input_handling`

## Conclusion

La même logique s'applique à `test_rag_utils.py`, qui garantit que notre traitement de texte arabe est correct avant même qu'il ne soit utilisé dans le flux RAG plus complexe.

Ces tests unitaires purs forment la fondation de notre suite de tests. Ils nous donnent confiance que nos briques de base fonctionnent correctement, ce qui facilite grandement le débogage quand des tests plus complexes échouent.

---

Après avoir exploré les tests, nous aborderons la [Documentation Utilisateur](../user-documentation/overview) et comment elle est structurée.