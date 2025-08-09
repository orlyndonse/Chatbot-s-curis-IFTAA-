---
sidebar_position: 1
title: Vue d'Ensemble des Tests
---

# Vue d'Ensemble des Tests

Les tests sont un aspect essentiel du développement logiciel pour garantir la qualité, la fiabilité et la maintenabilité de l'application Assistant RAG Fiqh. Le backend du projet inclut une structure de tests unitaires et potentiellement d'intégration utilisant Pytest.

## Objectifs des Tests

* **Vérifier la fonctionnalité** : S'assurer que chaque composant (fonctions, classes, endpoints API) se comporte comme attendu.
* **Prévenir les régressions** : Détecter si des modifications récentes ont introduit des bugs dans des fonctionnalités existantes.
* **Faciliter le refactoring** : Donner confiance lors de la modification ou de l'amélioration du code, en sachant que les tests peuvent signaler des problèmes.
* **Documenter le code** : Les tests servent aussi d'exemples d'utilisation des différents modules.

## Structure des Tests

Les tests pour le backend sont situés dans le dossier `Code_Source/backend/src/tests/`.

* **`conftest.py`**:
    * Ce fichier est utilisé par Pytest pour définir des fixtures, des hooks et des plugins partagés entre plusieurs fichiers de test.
    * Dans ce projet, il est utilisé pour :
        * **Mocker les dépendances** :
            * `get_session`: La dépendance FastAPI pour obtenir une session de base de données est remplacée par un mock (`mock_session`), évitant ainsi de réelles interactions avec la base de données pendant la plupart des tests unitaires.
            * `AccessTokenBearer`, `RefreshTokenBearer`, `RoleChecker`: Les dépendances de sécurité sont également mockées pour isoler la logique des endpoints de la validation réelle des tokens ou des rôles lors des tests.
        * **Fournir des fixtures réutilisables** :
            * `fake_session`: Retourne l'instance `mock_session`.
            * `fake_user_service`: Fournit une instance mockée du `UserService`.
            * `fake_question_service`: Fournit une instance mockée d'un `QuestionService` (ce nom pourrait correspondre à une version antérieure du `ConversationService` ou être un service non encore entièrement migré).
            * `test_client`: Fournit une instance de `TestClient` de FastAPI, permettant de faire des requêtes HTTP aux endpoints de l'application dans un contexte de test.
            * `test_question`: Fournit un exemple d'objet `Question` (potentiellement un ancien modèle de données ou un exemple pour les tests).
    * `app.dependency_overrides`: Permet de remplacer les dépendances réelles par leurs mocks au niveau de l'application FastAPI pour l'environnement de test.

* **`test_auth.py`**:
    * Contient les tests pour le module d'authentification (`src/auth/`).
    * Exemple de test : `test_user_creation` vérifie que lors de l'appel à l'endpoint `/signup` :
        * `fake_user_service.user_exists` est appelé correctement.
        * `fake_user_service.create_user` est appelé avec les bonnes données si l'utilisateur n'existe pas.
    * Les tests utilisent le `test_client` pour simuler des requêtes HTTP et les mocks (`fake_user_service`, `fake_session`) pour vérifier les interactions avec les services et la base de données sans les exécuter réellement.

* **`test_question.py`**:
    * Ce fichier semble contenir des tests pour une entité "Question" qui pourrait être un ancien nom ou un composant lié aux conversations/messages.
    * Les tests (`test_get_all_questions`, `test_create_question`, `test_get_question_by_uid`, `test_update_question_by_uid`) suivent un schéma similaire :
        * Utilisation du `test_client` pour appeler des endpoints (par exemple, `/api/v1/questions`).
        * Assertion que les méthodes du service mocké (`fake_question_service`) sont appelées comme prévu avec les bons arguments.

## Comment Lancer les Tests

Les tests sont généralement exécutés avec Pytest.

1.  Assurez-vous d'être dans l'environnement virtuel du backend où Pytest et les autres dépendances sont installés.
2.  Naviguez à la racine du dossier `Code_Source/backend/`.
3.  Exécutez la commande Pytest :
    ```bash
    pytest
    ```
    Ou, pour plus de détails :
    ```bash
    pytest -v
    ```
    Pytest découvrira et exécutera automatiquement les fichiers de test (nommés `test_*.py` ou `*_test.py`) et les fonctions de test (nommées `test_*`).

## Stratégie de Test Actuelle

D'après les fichiers fournis, la stratégie de test actuelle se concentre sur :
* **Tests d'intégration au niveau des API endpoints** : En utilisant `TestClient` pour s'assurer que les routes sont correctement configurées et appellent les services appropriés.
* **Mocking des dépendances externes** : Les services (comme `UserService`) et les sessions de base de données sont mockés pour isoler les tests de la logique des endpoints eux-mêmes et éviter la dépendance à une base de données réelle ou à des services externes pendant les tests unitaires/d'intégration des routes.
* **Vérification des appels de méthodes (Mock Assertions)** : Les tests vérifient que les méthodes des services mockés sont appelées une fois et avec les bons arguments.

Cette approche est efficace pour tester la couche API et s'assurer que la plomberie entre les routes, les services et les dépendances fonctionne comme prévu. Pour une couverture plus complète, des tests unitaires plus granulaires pour la logique métier au sein des services eux-mêmes (sans mocker la base de données, mais en utilisant une base de données de test par exemple) pourraient être ajoutés.

---

Après avoir exploré les tests, nous aborderons la [Documentation Utilisateur](./../user-documentation/overview.md) et comment elle est structurée.