---
sidebar_position: 1
title: Glossaire des Termes Techniques
---

# Glossaire des Termes Techniques

Cette section définit les termes techniques et les acronymes fréquemment utilisés dans cette documentation et dans le contexte du projet Assistant RAG Fiqh.

* **API (Application Programming Interface)** : Interface de programmation applicative. Un ensemble de règles et de protocoles permettant à différents composants logiciels de communiquer entre eux. Dans ce projet, le backend FastAPI expose une API REST pour le frontend.

* **ASGI (Asynchronous Server Gateway Interface)** : Interface standard entre les serveurs web Python asynchrones et les frameworks (comme FastAPI). Uvicorn est un serveur ASGI.

* **Alembic** : Outil de migration de schémas de base de données pour SQLAlchemy. Utilisé pour gérer les évolutions de la structure de la base de données PostgreSQL.

* **Authentification** : Processus de vérification de l'identité d'un utilisateur, généralement via un nom d'utilisateur/email et un mot de passe.

* **Autorisation** : Processus de vérification des droits d'accès d'un utilisateur authentifié à des ressources ou fonctionnalités spécifiques.

* **Backend** : Partie du système qui s'exécute sur le serveur et gère la logique métier, les interactions avec la base de données, et l'API. Dans ce projet, il est développé en Python avec FastAPI.

* **BCrypt** : Algorithme de hachage de mot de passe robuste et adaptatif, utilisé par `passlib` pour sécuriser les mots de passe des utilisateurs.

* **ChromaDB** : Base de données vectorielle open-source conçue pour stocker et rechercher des embeddings. Utilisée dans ce projet pour le composant RAG.

* **Chunk / Chunking** : Segment de texte. Le "chunking" est le processus de découpage de longs documents en morceaux plus petits avant de générer leurs embeddings.

* **CORS (Cross-Origin Resource Sharing)** : Mécanisme de sécurité des navigateurs web qui permet (ou restreint) les requêtes HTTP effectuées depuis un domaine différent de celui du serveur. Géré par `CORSMiddleware` dans FastAPI.

* **CRUD (Create, Read, Update, Delete)** : Opérations de base pour la persistance des données dans une base de données.

* **CSS (Cascading Style Sheets)** : Langage utilisé pour décrire la présentation et le style d'un document HTML.

* **DaisyUI** : Plugin pour Tailwind CSS qui fournit des composants d'interface utilisateur pré-stylisés. (Mentionné dans la configuration Tailwind du frontend).

* **Dépendance (FastAPI)** : Fonction ou classe utilisée par FastAPI pour fournir des données ou effectuer des actions avant l'exécution d'un endpoint de route (par exemple, pour l'authentification ou la validation).

* **Docusaurus** : Générateur de sites statiques optimisé pour créer des sites de documentation. Utilisé pour la documentation utilisateur et technique de ce projet.

* **DOM (Document Object Model)** : Représentation structurée d'un document HTML ou XML, permettant aux scripts de manipuler dynamiquement le contenu et la structure de la page.

* **Embedding** : Représentation vectorielle (une liste de nombres) d'un texte dans un espace de haute dimension. Les textes sémantiquement similaires auront des embeddings proches. Générés par des modèles comme Sentence Transformers.

* **Endpoint API** : URL spécifique sur le serveur backend qui exécute une action ou retourne des données lorsque sollicitée par une requête HTTP.

* **FastAPI** : Framework web Python moderne et performant pour construire des APIs, basé sur Pydantic et les type hints Python.

* **Frontend** : Partie du système avec laquelle l'utilisateur interagit directement, généralement dans le navigateur web. Dans ce projet, il est développé avec React et Vite.

* **Génération Augmentée par Récupération (RAG - Retrieval Augmented Generation)** : Technique d'IA où un modèle de langage (LLM) voit sa capacité de génération "augmentée" par des informations pertinentes récupérées dynamiquement à partir d'une base de connaissances externe (ici, les documents vectorisés dans ChromaDB).

* **Gemini (Google Generative AI)** : Famille de modèles de langage (LLM) développée par Google, utilisée dans ce projet pour la génération des réponses IA.

* **Git** : Système de contrôle de version distribué utilisé pour suivre les modifications du code source.

* **HMR (Hot Module Replacement)** : Fonctionnalité des serveurs de développement (comme Vite) qui permet de mettre à jour les modules dans le navigateur sans recharger toute la page, accélérant le développement.

* **Hook (React)** : Fonctions spéciales (`useState`, `useEffect`, etc.) qui permettent d'utiliser l'état et d'autres fonctionnalités de React dans les composants fonctionnels.

* **JWT (JSON Web Token)** : Standard ouvert (RFC 7519) pour créer des tokens d'accès qui affirment des "claims" (revendications) sous forme JSON. Utilisé pour l'authentification sans état.

* **JTI (JWT ID)** : Identifiant unique pour un token JWT, utilisé ici pour la blocklist lors de la déconnexion.

* **Langchain** : Framework pour développer des applications basées sur les modèles de langage (LLM), facilitant la création de chaînes (chains), l'intégration de Vector Stores, etc.

* **LLM (Large Language Model)** : Modèle d'intelligence artificielle entraîné sur de grandes quantités de texte, capable de comprendre et de générer du langage humain (par exemple, Gemini).

* **Loader (React Router)** : Fonction exécutée avant le rendu d'une route pour charger des données nécessaires à cette route.

* **Middleware (FastAPI)** : Fonction qui traite une requête avant qu'elle n'atteigne le code spécifique de la route, et/ou la réponse avant qu'elle ne soit renvoyée.

* **Migration (Base de Données)** : Processus de gestion des changements de schéma de la base de données de manière contrôlée et versionnée, utilisant ici Alembic.

* **Mock / Mocking** : En test logiciel, remplacer un objet ou un module par une version simulée (un mock) pour isoler le code testé de ses dépendances.

* **ORM (Object-Relational Mapper)** : Technique de programmation qui convertit les données entre des systèmes de types incompatibles en utilisant une programmation orientée objet. SQLModel (basé sur SQLAlchemy) est l'ORM utilisé.

* **PaaS (Platform as a Service)** : Modèle de cloud computing où un fournisseur tiers livre des outils matériels et logiciels aux utilisateurs via Internet, généralement pour le déploiement d'applications.

* **PostgreSQL** : Système de gestion de base de données relationnelle objet open-source.

* **PostCSS** : Outil pour transformer les styles CSS avec des plugins JavaScript. Utilisé par Tailwind CSS.

* **Prompt** : Instruction ou question donnée à un modèle de langage pour qu'il génère une réponse.

* **Pydantic** : Bibliothèque Python pour la validation de données et la gestion des paramètres, largement utilisée par FastAPI et SQLModel.

* **Pytest** : Framework de test pour Python, utilisé pour les tests du backend.

* **React** : Bibliothèque JavaScript populaire pour construire des interfaces utilisateur, basée sur des composants.

* **React Router DOM** : Bibliothèque de routage pour les applications React, gérant la navigation côté client.

* **Redis** : Système de stockage en mémoire, souvent utilisé comme base de données, cache, et courtier de messages. Utilisé ici pour la blocklist des tokens JWT.

* **Retriever** : Dans le contexte RAG, composant qui recherche et récupère les informations les plus pertinentes à partir d'une base de connaissances (ici, ChromaDB) en réponse à une requête.

* **Schéma (Base de Données)** : Structure logique d'une base de données, décrivant l'organisation des tables, colonnes, types de données et relations.

* **Schéma (API/Pydantic)** : Modèle de données définissant la structure et les types de données attendus pour les requêtes et les réponses d'une API.

* **Sentence Transformers** : Bibliothèque Python qui fournit des modèles pré-entraînés faciles à utiliser pour calculer des embeddings de phrases et de textes.

* **Session (Base de Données)** : Représente une conversation avec la base de données, permettant d'exécuter des requêtes et de gérer les transactions.

* **SQLModel** : Bibliothèque Python pour interagir avec les bases de données SQL à l'aide de code Python, combinant les fonctionnalités de Pydantic et SQLAlchemy.

* **SWC (Speedy Web Compiler)** : Compilateur ultra-rapide pour JavaScript/TypeScript écrit en Rust, utilisé par Vite pour améliorer les performances de build. (Note: le package.json liste `@vitejs/plugin-react` qui peut utiliser SWC par défaut).

* **Tailwind CSS** : Framework CSS "utility-first" pour construire rapidement des interfaces utilisateur personnalisées.

* **Token (JWT)** : Chaîne de caractères encodée utilisée pour l'authentification et l'autorisation. L'application utilise des tokens d'accès et des tokens de rafraîchissement.

* **Uvicorn** : Serveur ASGI (Asynchronous Server Gateway Interface) léger et rapide, utilisé pour exécuter l'application FastAPI.

* **Vector Store (Base de Données Vectorielle)** : Base de données spécialisée dans le stockage et la recherche d'embeddings (vecteurs). ChromaDB est utilisée dans ce projet.

* **Vite** : Outil de build frontend de nouvelle génération qui vise à fournir une expérience de développement plus rapide et plus légère pour les projets web modernes.