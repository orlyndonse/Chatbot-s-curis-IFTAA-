---
sidebar_position: 1
title: Vue d'Ensemble
---

# Vue d'Ensemble de l'Architecture

L'application Assistant RAG Fiqh est structurée autour d'une architecture client-serveur moderne, conçue pour la modularité et l'extensibilité. Elle se compose des principaux éléments suivants :

## Composants Majeurs

1.  **Frontend (React + Vite) :**
    * Responsable de l'interface utilisateur (UI) avec laquelle l'utilisateur final interagit.
    * Construit avec [React](https://react.dev/) et [Vite](https://vitejs.dev/) pour un développement et un build rapides.
    * Gère l'affichage des conversations, la saisie des prompts, le téléversement des documents, et la présentation des réponses de l'IA.
    * Communique avec le backend via des requêtes HTTP (API REST).

2.  **Backend (Python - FastAPI) :**
    * Sert d'API RESTful pour le frontend et orchestre la logique métier.
    * Développé avec [FastAPI](https://fastapi.tiangolo.com/), un framework Python moderne pour construire des APIs.
    * Gère l'authentification des utilisateurs, les opérations CRUD (Create, Read, Update, Delete) pour les conversations et les messages, le traitement des documents téléversés, et l'interaction avec le pipeline RAG.

3.  **Base de Données Relationnelle (PostgreSQL) :**
    * Utilisée pour stocker les données structurées persistantes.
    * Gérée via [SQLModel](https://sqlmodel.tiangolo.com/) (qui combine Pydantic et SQLAlchemy) pour la définition des modèles et les interactions.
    * Stocke les informations des utilisateurs (profils, identifiants hachés), les métadonnées des conversations, les messages échangés, et les métadonnées des documents téléversés.
    * Les migrations de schéma sont gérées par [Alembic](https://alembic.sqlalchemy.org/).

4.  **Base de Données Vectorielle (ChromaDB) :**
    * Essentielle pour le composant RAG.
    * Stocke les embeddings (représentations vectorielles) des documents téléversés, permettant une recherche sémantique rapide et efficace.
    * Utilise [ChromaDB](https://www.trychroma.com/) en mode persistant.

5.  **Modèle de Langage (LLM - Google Gemini) :**
    * Le cœur de la génération de réponses intelligentes.
    * Utilise l'API [Google Generative AI (Gemini Pro/Flash)](https://ai.google.dev/) pour comprendre les prompts et générer des réponses en se basant sur le contexte récupéré.

6.  **Serveur de Cache/Blocklist (Redis) :**
    * Utilisé pour la gestion de la blocklist des tokens JWT (pour la déconnexion et la sécurité des tokens).
    * Peut potentiellement être étendu pour d'autres besoins de caching.

## Diagramme d'Architecture Simplifié

![Flowchart](/img/screenshot-diagram.png)