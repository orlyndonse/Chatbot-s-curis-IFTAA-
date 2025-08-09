---
sidebar_position: 1
title: Structure du Projet Backend
---

# Structure du Projet Backend

Le backend de l'Assistant RAG Fiqh est développé en Python en utilisant le framework FastAPI. Il est organisé en modules pour une meilleure maintenabilité et séparation des préoccupations. Le code source principal du backend se trouve dans le dossier `Code_Source/backend/src/`.

## Organisation Générale des Dossiers

Voici un aperçu de la structure des dossiers clés au sein de `Code_Source/backend/src/` :

## Description des Dossiers Clés

* **`auth/`** : Contient toute la logique relative à l'authentification des utilisateurs, y compris la création de compte, la connexion, la vérification par email, la réinitialisation de mot de passe, et la gestion des tokens JWT.
* **`conversations/`** : Gère les fonctionnalités de base de l'application de chat, telles que la création et la récupération de conversations, l'ajout de messages, le téléversement et la gestion des documents associés à une conversation, et l'obtention des réponses du système RAG.
* **`db/`** : Centralise la configuration et l'interaction avec la base de données relationnelle (PostgreSQL via SQLModel) pour le stockage des données persistantes et avec Redis pour le caching ou la gestion de listes de blocage.
* **`rag/`** : Regroupe tous les composants spécifiques à la logique RAG (Retrieval Augmented Generation). Cela inclut le chargement et le traitement des documents, la création et la gestion de la base de données vectorielle (ChromaDB), et l'orchestration de la chaîne de questions-réponses avec le LLM (Google Gemini).
* **`tests/`** : Contient les scripts de test pour assurer la fiabilité et le bon fonctionnement des différents modules du backend.
* **Fichiers à la racine de `src/`** :
    * `__init__.py` : Initialise l'application FastAPI, enregistre les routeurs et les middlewares.
    * `config.py` : Charge et rend disponible la configuration de l'application à partir de variables d'environnement ou d'un fichier `.env`.
    * `errors.py` : Définit les exceptions personnalisées pour une gestion d'erreurs plus claire et les handlers FastAPI correspondants.
    * `mail.py` : Configure le service d'envoi d'emails utilisé pour la vérification des comptes et la réinitialisation des mots de passe.
    * `middleware.py` : Enregistre les middlewares FastAPI, comme celui pour la gestion des requêtes CORS ou le logging.

## Fichiers Importants Hors `src/`

* **`alembic.ini`** : Fichier de configuration pour Alembic, l'outil de migration de base de données utilisé avec SQLAlchemy/SQLModel.
* **`indexer_rag.py`** : Script autonome pour l'indexation initiale des documents dans la base de données vectorielle.
* **`requirements.txt`** : Liste toutes les dépendances Python du projet backend.
* **`monstockage_backup_2025-04-20.sql`** : Un exemple de sauvegarde de la base de données PostgreSQL, utile pour comprendre le schéma attendu ou pour restaurer un état.

Cette structure modulaire vise à faciliter le développement, les tests et la maintenance de l'application backend.

---

Ensuite, on va voir [le point d'entrée principal pour l'application backend FastAPI](../backend/entry-point.md) src/__init__.py.