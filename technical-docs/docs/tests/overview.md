---
sidebar_position: 1
title: Vue d'Ensemble des Tests
---

# Vue d'Ensemble des Tests

Les tests sont un aspect essentiel du développement logiciel pour garantir la qualité, la fiabilité et la maintenabilité de l'application Assistant RAG Fiqh. Le backend du projet inclut une suite de tests robuste utilisant **Pytest** pour les tests unitaires et d'intégration.

---

## Objectifs des Tests

* **Vérifier la fonctionnalité** : S'assurer que chaque composant (fonctions, classes, endpoints API) se comporte comme attendu.
* **Prévenir les régressions** : Détecter si des modifications récentes ont introduit des bugs dans des fonctionnalités existantes.
* **Faciliter le refactoring** : Donner confiance lors de la modification ou de l'amélioration du code, en sachant que les tests peuvent signaler des problèmes.
* **Documenter le code** : Les tests servent aussi d'exemples concrets d'utilisation des différents modules.

---

## Structure des Tests

Les tests pour le backend sont situés dans le dossier `Code_Source/backend/tests/`.

### `conftest.py`

Ce fichier est le centre de configuration pour Pytest. Il permet de définir des "fixtures" (des morceaux de code réutilisables pour les tests).

* **Mocker les dépendances** : Le rôle principal de ce fichier est de remplacer les dépendances réelles par des "mocks" (des doublures) pour isoler nos tests.
    * `get_session`: La connexion à la base de données est remplacée par un mock asynchrone (`AsyncMock`).
    * `get_user_service`: La dépendance qui fournit le `UserService` est remplacée pour nous permettre d'injecter un faux service (`fake_user_service`). C'est la clé pour tester la logique des routes sans dépendre du vrai service.
    * `get_current_user`: La dépendance de sécurité est remplacée par une fonction qui retourne un faux utilisateur, nous évitant de devoir gérer de vrais tokens JWT dans les tests.

* **Fournir des fixtures réutilisables** :
    * `fake_session`: Fournit le mock de session pour les tests.
    * `fake_user_service`: Fournit le mock du service utilisateur.
    * `test_client`: Fournit une instance de `TestClient`, un outil essentiel pour simuler des requêtes HTTP vers notre application FastAPI.

### `test_auth.py`

Ce fichier contient les tests pour le module d'authentification (`src/auth/`). Il se concentre sur les tests d'intégration des endpoints.
* Il utilise le `test_client` pour simuler des appels API (ex: `POST /api/v1/auth/signup`).
* Il suit le pattern **Arrange, Act, Assert** :
    1.  **Arrange** : On prépare les mocks (ex: `fake_user_service.user_exists.return_value = False`).
    2.  **Act** : On exécute la requête HTTP.
    3.  **Assert** : On vérifie que le code de statut est correct et que les méthodes de nos mocks ont été appelées comme prévu.

### `test_auth_utils.py`

Ce fichier est un exemple de **tests unitaires purs**.
* Il teste les fonctions utilitaires du module d'authentification (`src/auth/utils.py`) de manière totalement isolée.
* Par exemple, il vérifie que la fonction `generate_passwd_hash` et `verify_password` fonctionnent correctement sans avoir besoin de mocks, de l'application FastAPI ou d'une base de données.

### `test_rag_utils.py`

Similaire à `test_auth_utils.py`, ce fichier contient des tests unitaires pour les fonctions utilitaires du module RAG (`src/rag/utils.py`).
* Il vérifie le bon fonctionnement de fonctions comme `pretraiter_texte_arabe`, s'assurant que la logique de bas niveau est fiable.

---

## Comment Lancer les Tests

1.  Activez votre environnement virtuel : `source env/bin/activate` (ou `env\Scripts\activate` sur Windows).
2.  Naviguez à la racine du dossier `Code_Source/backend/`.
3.  Exécutez la commande Pytest :
    ```bash
    pytest -v
    ```
    Pytest découvrira et exécutera automatiquement tous les tests.

---

## Stratégie de Test Actuelle

La stratégie de test se concentre sur deux axes principaux pour une couverture efficace :

1.  **Tests d'intégration des Endpoints API** : En utilisant `TestClient`, nous nous assurons que les routes sont bien configurées, que les données sont validées et que les services appropriés sont appelés. C'est le test le plus proche d'une utilisation réelle.

2.  **Tests unitaires des fonctions utilitaires** : En testant les fonctions "pures" (qui ne dépendent pas de FastAPI ou de la base de données) de manière isolée, nous garantissons que les briques fondamentales de notre logique métier sont correctes et fiables.

Cette double approche permet de tester à la fois la "plomberie" de l'application (les routes et les dépendances) et la logique métier de base, offrant une bonne confiance dans la qualité du code.

Pour une couverture encore plus complète, des tests pourraient être ajoutés pour le module `conversations`, en suivant le même modèle que pour `test_auth.py`.

---

Maintenant, explorons en détail comment tester les endpoints d'authentification dans la section [Focus - Tester l'Authentification](./auth-tests).