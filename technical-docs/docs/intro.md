---
sidebar_position: 1
title: Introduction à la Documentation Technique
slug: /guide/introduction-technique # MODIFIÉ: Nouveau chemin dédié
---

# Bienvenue dans la Documentation Technique de l'Assistant RAG Fiqh

Cette documentation sert à expliquer clairement comment fonctionne l'application **Assistant RAG Fiqh**, avec ses parties principales, la façon dont les données circulent et les choix techniques faits.

Elle est principalement destinée :
* Aux **développeurs** impliqués dans la maintenance ou l'évolution du projet.
* Aux **administrateurs système** chargés du déploiement.
* À toute personne souhaitant avoir une vue détaillée du fonctionnement interne de l'application.

## Objectifs du Système

L'Assistant RAG Fiqh est une solution web conçue pour :
* Permettre aux utilisateurs (étudiants en Fiqh, éducateurs communautaires, chercheurs) de **téléverser leurs propres documents** relatifs au Fiqh Maliki.
* Offrir une interface de **chat intuitive** pour poser des questions en langue arabe sur le contenu de ces documents.
* Fournir des **réponses contextuelles et précises**, générées par une intelligence artificielle (IA) s'appuyant sur la technique de Génération Augmentée par Récupération (RAG) et les documents fournis.

## Comment Naviguer dans cette Documentation ?

Utilisez la **barre latérale** sur la gauche pour explorer les différentes sections :
* **Architecture Générale** : Vue d'ensemble des composants et des flux de données.
* **Composant Backend** : Détails sur l'API FastAPI, la gestion des données, l'authentification, etc.
* **Composant Frontend** : Informations sur l'interface React, la gestion de l'état et les interactions utilisateur.
* **Base de Données Approfondie** : Schémas et rôles des bases de données PostgreSQL et ChromaDB.
* **Pipeline RAG Détaillé** : Explication des processus d'ingestion des documents et de génération des réponses.
* **Installation, Déploiement, Tests** : Guides pratiques pour mettre en place et maintenir l'application.

Nous vous encourageons à commencer par la section [Vue d'Ensemble de l'Architecture](./architecture/overview.md) pour avoir une première compréhension globale du système.