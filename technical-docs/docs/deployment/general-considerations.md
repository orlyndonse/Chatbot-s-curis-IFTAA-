---
sidebar_position: 1
title: Considérations Générales pour le Déploiement
---

# Considérations Générales pour le Déploiement

Le déploiement de l'Assistant RAG Fiqh en production nécessite de prendre en compte plusieurs aspects pour assurer sa stabilité, sa sécurité et ses performances. Cette section aborde des considérations générales. Des solutions d'hébergement gratuites ou avec des niveaux gratuits généreux peuvent être utilisées pour démarrer.

## 1. Backend (FastAPI)

* **Serveur d'Application ASGI**:
    * FastAPI étant un framework ASGI, il nécessite un serveur ASGI comme Uvicorn pour fonctionner en production.
    * Pour la robustesse, il est courant d'utiliser Gunicorn comme gestionnaire de processus pour Uvicorn, permettant de gérer plusieurs workers, les redémarrages, etc.
    * Exemple de commande Gunicorn :
        ```bash
        gunicorn -w 4 -k uvicorn.workers.UvicornWorker src:app
        ```
        (où `-w 4` spécifie 4 processus workers).
* **Hébergement Backend**:
    * **Plateformes PaaS (Platform as a Service)** : Des services comme Render, Fly.io, ou Heroku (avec son plan gratuit pour les petits projets) peuvent simplifier le déploiement d'applications Python/FastAPI. Ils gèrent souvent l'infrastructure sous-jacente. Render, par exemple, propose un niveau gratuit pour les services web qui pourrait convenir pour un démarrage.
    * **VPS (Virtual Private Server)** : Des fournisseurs comme DigitalOcean, Linode, Vultr (certains peuvent avoir des crédits d'essai ou des options très abordables). Cela vous donne plus de contrôle mais nécessite plus de configuration manuelle (sécurité, mises à jour, etc.).
    * **Conteneurisation (Docker)** : Empaqueter le backend dans une image Docker est fortement recommandé. Cela facilite le déploiement sur de nombreuses plateformes (y compris celles mentionnées ci-dessus) et assure la cohérence de l'environnement.
* **Variables d'Environnement**:
    * Toutes les configurations sensibles (clés API, URL de base de données, secrets JWT) définies dans `src/config.py` et chargées via le fichier `.env` en développement doivent être définies comme des variables d'environnement sécurisées sur la plateforme d'hébergement de production. Ne committez jamais de fichiers `.env` contenant des secrets de production dans votre dépôt Git.
* **Stockage des Fichiers (`UPLOAD_DIR`)**:
    * Le chemin `Config.UPLOAD_DIR` doit pointer vers un emplacement de stockage persistant sur le serveur de production.
    * Pour les plateformes PaaS, vérifiez leurs options de stockage de fichiers persistants (disques persistants, services de stockage d'objets comme AWS S3, Google Cloud Storage, ou des équivalents gratuits/abordables). Un stockage éphémère du système de fichiers du conteneur ne suffira pas si les fichiers doivent persister entre les redéploiements.

## 2. Frontend (React + Vite)

* **Build de Production**:
    * Avant le déploiement, générez les fichiers statiques optimisés du frontend :
        ```bash
        cd Code_Source/frontend
        npm run build
        ```
        (ou `yarn build`)
    * Cela créera un dossier `dist/` (ou similaire) contenant les fichiers HTML, CSS et JavaScript prêts pour la production.
* **Hébergement Frontend (Statique)**:
    * **Services d'hébergement statique gratuits/abordables** :
        * Netlify
        * Vercel (très populaire pour les projets React/Vite)
        * GitHub Pages (gratuit pour les projets publics et privés)
        * Cloudflare Pages
        * Render (supporte aussi les sites statiques)
    * Ces services se chargent de servir vos fichiers statiques de manière optimisée via un CDN.
* **Configuration de l'API Base URL**:
    * Le frontend doit savoir où se trouve l'API backend. Si l'API est déployée sur un domaine différent de celui du frontend, la configuration CORS du backend doit l'autoriser.
    * La variable `API_BASE_URL` dans le code frontend (par exemple, dans `src/utils/fetchWithAuth.js` ou `src/contexts/UserContext.jsx`) doit être configurée pour pointer vers l'URL publique de votre backend en production. Cela peut être géré via des variables d'environnement au moment du build du frontend.

## 3. Base de Données (PostgreSQL)

* **Services de Base de Données Managés**:
    * De nombreux fournisseurs cloud proposent des services PostgreSQL managés (AWS RDS, Google Cloud SQL, Azure Database for PostgreSQL).
    * **Options gratuites/abordables** :
        * Supabase (offre un niveau gratuit généreux pour PostgreSQL)
        * ElephantSQL (propose un petit plan gratuit)
        * Railway.app (peut provisionner PostgreSQL avec un niveau gratuit)
        * Render (propose PostgreSQL en tant que service, avec un plan gratuit)
* **Configuration**: L'URL `DATABASE_URL` du backend doit pointer vers cette base de données de production.
* **Migrations**: Exécutez les migrations Alembic (`alembic upgrade head`) sur la base de données de production pour créer le schéma initial.

## 4. Base Vectorielle (ChromaDB)

* **Persistance**: Le dossier `CHROMA_DB_PATH` (par exemple, `chroma_db_fiqh`) doit être stocké sur un volume persistant si le backend est conteneurisé ou déployé sur une plateforme où le système de fichiers est éphémère.
    * Si vous utilisez Docker, montez un volume Docker pour ce chemin.
    * Sur des PaaS, cela peut nécessiter un disque persistant attaché au service backend.
* **Indexation Initiale**: Exécutez le script `indexer_rag.py` sur l'environnement de production si vous avez un corpus de documents de base à indexer.

## 5. Redis

* **Services Redis Managés ou Hébergés**:
    * De nombreux fournisseurs cloud (AWS ElastiCache, Google Memorystore, Azure Cache for Redis).
    * **Options gratuites/abordables** :
        * Upstash (offre un niveau gratuit pour Redis serverless)
        * Redis Labs (maintenant Redis Ltd., propose un plan gratuit)
        * Railway.app (peut provisionner Redis)
* **Configuration**: Les variables `REDIS_HOST` et `REDIS_PORT` du backend doivent pointer vers l'instance Redis de production.

## 6. Sécurité

* **HTTPS**: Utilisez impérativement HTTPS pour le frontend et le backend. La plupart des plateformes d'hébergement modernes facilitent cela avec des certificats SSL/TLS gratuits (par exemple, via Let's Encrypt).
* **Secrets Management**: Gérez correctement toutes les clés API, mots de passe, et `JWT_SECRET` en utilisant les mécanismes de secrets de votre plateforme d'hébergement. Ne les hardcodez jamais et ne les committez pas dans le code source.
* **CORS**: Configurez `allow_origins` dans le `CORSMiddleware` du backend pour n'autoriser que l'URL de votre frontend de production.
* **En-têtes de Sécurité HTTP**: Ajoutez des en-têtes de sécurité (X-Content-Type-Options, X-Frame-Options, Strict-Transport-Security, etc.) via votre serveur d'application ou un reverse proxy.
* **Limitations de Taux (Rate Limiting)**: Implémentez une limitation de taux sur les endpoints sensibles (login, reset de mot de passe, etc.) pour prévenir les abus.

## 7. Logging et Monitoring

* Configurez un système de logging centralisé pour le backend afin de capturer les erreurs et les informations de diagnostic en production.
* Mettez en place un monitoring basique pour surveiller la disponibilité et les performances de l'application.

Le choix des outils et plateformes spécifiques dépendra de vos contraintes budgétaires, de vos compétences techniques et des besoins de l'application à mesure qu'elle évolue. Commencer avec des niveaux gratuits est une excellente stratégie pour les projets personnels ou les POCs.

---

Maintenant que nous avons abordé le déploiement, la section suivante concerne les [Tests (`src/tests/`)](./../tests/overview.md).