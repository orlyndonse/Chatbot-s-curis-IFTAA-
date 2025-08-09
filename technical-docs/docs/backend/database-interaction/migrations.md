---
sidebar_position: 3
title: Migrations de Base de Données (Alembic)
---

# Migrations de Base de Données avec Alembic

La gestion des évolutions du schéma de la base de données relationnelle (PostgreSQL) est cruciale pour maintenir la cohérence des données à mesure que l'application se développe. Ce projet utilise [Alembic](https://alembic.sqlalchemy.org/) en conjonction avec SQLModel (et donc SQLAlchemy) pour gérer ces migrations.

## Rôle d'Alembic

Alembic permet de :
* **Générer des scripts de migration** : Lorsque les modèles de données SQLModel (définis dans `src/db/models.py`) sont modifiés (ajout/suppression de tables, ajout/modification/suppression de colonnes, etc.), Alembic peut comparer l'état actuel des modèles avec l'état de la base de données et générer un script Python qui applique ces changements.
* **Appliquer les migrations** : Exécuter les scripts de migration pour mettre à jour le schéma de la base de données de manière incrémentale et versionnée.
* **Revenir en arrière (Downgrade)** : Permettre de défaire des migrations si nécessaire.
* **Versionner le schéma de la base de données** : Chaque migration est identifiée par un ID de révision, permettant de suivre l'historique des modifications du schéma.

## Configuration

La configuration d'Alembic se trouve principalement dans deux fichiers à la racine du projet backend :

* **`alembic.ini`**:
    * Fichier de configuration principal pour Alembic.
    * Contient des informations telles que :
        * `script_location`: Le chemin vers le répertoire des scripts de migration (par défaut `migrations`).
        * `sqlalchemy.url`: L'URL de connexion à la base de données. **Important** : Pour qu'Alembic fonctionne correctement, cette URL doit pointer vers votre base de données de développement ou de production. Elle est souvent commentée par défaut et doit être configurée pour pointer vers la même base de données que celle définie dans `src/config.py` (mais en utilisant un driver synchrone pour Alembic, par exemple `postgresql://user:password@host/dbname`).
    * D'autres options de configuration pour le logging, les templates de nom de fichier de migration, etc.

* **Dossier `migrations/`** (généré par Alembic) :
    * `env.py`: Script Python exécuté par Alembic. Il est configuré pour :
        * Se connecter à la base de données en utilisant l'URL de `alembic.ini` ou une variable d'environnement.
        * Accéder aux métadonnées des tables SQLModel (`SQLModel.metadata` depuis `src.db.models`) pour la génération automatique des migrations ("autogenerate").
    * `script.py.mako`: Template utilisé pour générer les nouveaux fichiers de migration.
    * `versions/`: Dossier contenant les scripts de migration individuels, chacun représentant une étape de l'évolution du schéma.

## Utilisation Courante

Les commandes Alembic sont généralement exécutées depuis la racine du dossier `Code_Source/backend/`.

1.  **Initialisation (une seule fois par projet)**:
    ```bash
    alembic init migrations
    ```
    (Cette étape a déjà été faite pour ce projet, créant `alembic.ini` et le dossier `migrations/`).

2.  **Génération d'une nouvelle migration (après modification des modèles dans `src/db/models.py`)**:
    ```bash
    alembic revision -m "description_de_la_modification" --autogenerate
    ```
    * `-m "..."`: Fournit un message descriptif pour la migration.
    * `--autogenerate`: Demande à Alembic de comparer les modèles avec la base de données et de tenter de générer automatiquement les opérations de migration (création de table, ajout de colonne, etc.).
    * Un nouveau fichier de migration sera créé dans `migrations/versions/`. Il est **essentiel de vérifier** ce fichier généré avant de l'appliquer, car l'autogénération n'est pas toujours parfaite.

3.  **Application des migrations à la base de données**:
    ```bash
    alembic upgrade head
    ```
    * `head`: Applique toutes les migrations jusqu'à la dernière version (la "tête").
    * On peut aussi cibler une révision spécifique : `alembic upgrade <revision_id>`.

4.  **Revenir à une version précédente (downgrade)**:
    ```bash
    alembic downgrade -1 # Revenir d'une révision
    alembic downgrade base # Revenir à un schéma vide
    alembic downgrade <revision_id> # Revenir à une révision spécifique
    ```

5.  **Afficher l'historique des migrations**:
    ```bash
    alembic history
    ```

6.  **Afficher la révision actuelle de la base de données**:
    ```bash
    alembic current
    ```

L'utilisation d'Alembic est une bonne pratique pour gérer les changements de schéma de base de données de manière contrôlée et reproductible, surtout dans un environnement d'équipe ou lors de déploiements multiples.

---

Maintenant que la gestion du schéma est couverte, nous allons nous intéresser au module [`src/db/redis.py`](../database-interaction/redis.md) et à son rôle dans la gestion de la blocklist des tokens.