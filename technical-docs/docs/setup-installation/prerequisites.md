---
sidebar_position: 1
title: Prérequis d'Installation
---

# Prérequis d'Installation

Avant de pouvoir configurer et lancer l'environnement de développement pour l'Assistant RAG Fiqh, assurez-vous que les logiciels et outils suivants sont installés sur votre système :

## 1. Python

* **Version** : Le backend est développé en Python. Une version récente de Python 3 (idéalement 3.9 ou supérieure, comme indiqué dans `requirements.txt` qui mentionne des dépendances compatibles avec Python 3.9+) est requise.
* **Installation** :
    * **Windows** : Téléchargez l'installeur depuis [python.org](https://www.python.org/downloads/windows/) et assurez-vous d'ajouter Python à votre PATH pendant l'installation.
    * **macOS** : Python est souvent préinstallé. Vous pouvez vérifier avec `python3 --version`. Pour une version plus récente ou une gestion via [Homebrew](https://brew.sh/), utilisez `brew install python3`.
    * **Linux** : Python est généralement préinstallé. Utilisez le gestionnaire de paquets de votre distribution (par exemple, `sudo apt update && sudo apt install python3 python3-pip python3-venv` sur Debian/Ubuntu).
* **Pip** : Le gestionnaire de paquets Python. Il est généralement inclus avec les installations Python récentes. Vérifiez avec `pip3 --version`.
* **Venv** : Module pour créer des environnements virtuels (fortement recommandé). Souvent inclus ou installable via `python3-venv`.

## 2. Node.js et npm (ou Yarn)

* **Version** : Le frontend est construit avec React et Vite, qui nécessitent Node.js. Une version LTS (Long Term Support) de Node.js est recommandée (par exemple, Node.js 18.x ou supérieure, comme indiqué dans `Code_Source/frontend/package.json` qui spécifie `"node": ">=18.0.0"` pour Docusaurus et potentiellement pour le projet frontend lui-même).
* **npm** (Node Package Manager) : Installé automatiquement avec Node.js.
* **Yarn** (Optionnel, mais si utilisé dans le projet frontend) : Un autre gestionnaire de paquets JavaScript. Si `yarn.lock` est présent dans le projet frontend, Yarn est probablement utilisé. Installez-le via `npm install --global yarn` après avoir installé Node.js.
* **Installation** :
    * Téléchargez depuis [nodejs.org](https://nodejs.org/) ou utilisez un gestionnaire de versions comme [nvm](https://github.com/nvm-sh/nvm).

## 3. Git

* **Objectif** : Nécessaire pour cloner le dépôt du projet depuis le gestionnaire de code source (par exemple, GitHub, GitLab).
* **Installation** :
    * Téléchargez depuis [git-scm.com](https://git-scm.com/downloads).

## 4. Base de Données PostgreSQL

* **Version** : Une instance de PostgreSQL est requise pour stocker les données de l'application (utilisateurs, conversations, etc.). La version supportée dépendra des fonctionnalités utilisées, mais une version récente (par exemple, 13 ou supérieure) est généralement un bon choix.
* **Installation** :
    * Visitez [postgresql.org/download/](https://www.postgresql.org/download/) pour les instructions d'installation spécifiques à votre système d'exploitation.
    * Des outils comme pgAdmin (interface graphique) peuvent être utiles pour gérer la base de données.
* **Alternative Docker** : Pour simplifier la configuration locale, vous pouvez utiliser Docker pour lancer une instance PostgreSQL. Un fichier `docker-compose.yml` pourrait faciliter cela.

## 5. Serveur Redis

* **Version** : Une instance Redis est utilisée pour la blocklist des tokens JWT. Une version récente est recommandée.
* **Installation** :
    * Visitez [redis.io/download/](https://redis.io/download/) pour les instructions.
    * **Windows** : Redis n'est pas officiellement supporté sur Windows, mais des ports communautaires existent (par exemple, via WSL ou des builds non officiels). L'utilisation de Docker est une option plus simple pour Windows.
    * **macOS** : `brew install redis`
    * **Linux** : `sudo apt install redis-server` ou équivalent.
* **Alternative Docker** : Docker peut également être utilisé pour lancer facilement une instance Redis.

## 6. Docker (Optionnel, mais Recommandé pour les Services)

* **Objectif** : Simplifie grandement la mise en place et la gestion des services externes comme PostgreSQL et Redis, surtout en environnement de développement.
* **Installation** :
    * Téléchargez [Docker Desktop](https://www.docker.com/products/docker-desktop/) pour Windows ou macOS.
    * Sur Linux, suivez les instructions d'installation pour votre distribution.

## 7. IDE ou Éditeur de Code

* Un environnement de développement intégré (IDE) ou un éditeur de code de votre choix, par exemple :
    * Visual Studio Code (VS Code)
    * PyCharm (pour le backend Python)
    * WebStorm (pour le frontend React)

Une fois ces prérequis installés, vous serez prêt à configurer l'environnement de développement du backend et du frontend.

---

Après avoir vérifié les prérequis, la prochaine étape est la [Configuration de l'Environnement Backend](./backend-setup.md).