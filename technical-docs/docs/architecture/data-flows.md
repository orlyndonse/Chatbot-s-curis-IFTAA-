---
sidebar_position: 2
title: Flux de Données Principaux
---

# Flux de Données Principaux

Cette section décrit les principaux flux de données au sein de l'application Assistant RAG Fiqh, illustrant comment les informations et les actions des utilisateurs transitent entre les différents composants du système.

## 1. Flux d'Authentification Utilisateur

Ce flux couvre l'inscription, la vérification par email, la connexion, la réinitialisation du mot de passe et la déconnexion.

![data-flows](/img/screenshot-data-flows-1.png)

![data-flows-2](/img/screenshot-data-flows-2.png)

## 2. Flux de Création de Conversation

Ce flux illustre la création d'une nouvelle conversation et l'ajout de messages avec génération de réponses IA.

![data-flows-messages](/img/screenshot-data-flows-messages.png)

## 3. Flux d'Upload de Documents

Ce flux décrit le processus de téléchargement et de traitement des documents, incluant leur indexation dans la base de données vectorielle ChromaDB.

![data-flows-documents](/img/screenshot-data-flows-documents.png)

## 4. Flux de Génération de Réponses RAG

Ce flux détaille le processus complet de génération de réponses utilisant la recherche vectorielle (RAG) avec l'historique des conversations et les documents indexés.

![data-flows-rag](/img/screenshot-data-flows-rag.png)

 Maintenant, nous pourrons passer à la section  [Composant Backend](../backend/structure).