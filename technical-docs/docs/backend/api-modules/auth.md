---
sidebar_position: 1
title: Module d'Authentification (src/auth/)
---

# Module d'Authentification (`src/auth/`)

Le module d'authentification (`src/auth/`) est responsable de toutes les opérations liées à la gestion des utilisateurs et à la sécurité de l'accès à l'API. Il gère l'inscription, la connexion, la vérification des emails, la réinitialisation des mots de passe, la gestion des tokens JWT, et la protection des routes.

## Structure du Module

Le module `auth` est structuré en plusieurs fichiers pour une meilleure organisation :

* **`routes.py`**: Définit les endpoints API relatifs à l'authentification.
* **`schemas.py`**: Contient les modèles Pydantic pour la validation des données des requêtes et la sérialisation des réponses.
* **`service.py`**: Implémente la logique métier pour les opérations sur les utilisateurs (création, recherche, mise à jour).
* **`utils.py`**: Fournit des fonctions utilitaires pour l'authentification, comme la génération et le décodage des tokens JWT, le hachage et la vérification des mots de passe, et la création de tokens URL-safe pour la vérification d'email et la réinitialisation de mot de passe.
* **`dependencies.py`**: Définit les dépendances FastAPI utilisées pour la sécurité des endpoints, comme la vérification des tokens d'accès/rafraîchissement et la vérification des rôles utilisateurs.

## Fonctionnalités Principales et Flux

### 1. `routes.py` - Endpoints de l'API d'Authentification

Ce fichier est au cœur des interactions client-serveur pour l'authentification. Il utilise `FastAPI.APIRouter` pour regrouper les routes.

* **`/signup` (POST)**:
    * Permet à un nouvel utilisateur de créer un compte.
    * Prend en entrée les données utilisateur (prénom, nom, nom d'utilisateur, email, mot de passe) via le modèle `UserCreateModel`.
    * Vérifie si l'utilisateur existe déjà via `UserService.user_exists`.
    * Si non, crée l'utilisateur via `UserService.create_user`.
    * Génère un token de vérification URL-safe (`create_url_safe_token`) et envoie un email de vérification contenant un lien vers le frontend.
    * Retourne les informations de l'utilisateur créé (modèle `UserModel`).
* **`/resend-verification-email` (POST)**:
    * Permet à un utilisateur de demander un nouvel email de vérification si son compte n'est pas encore vérifié.
    * Prend l'email de l'utilisateur (`EmailModel`).
    * Vérifie l'existence de l'utilisateur et son statut de vérification.
    * Renvoie un nouvel email de vérification.
* **`/verify-email` (POST)**:
    * Valide le compte d'un utilisateur via un token fourni dans le corps de la requête (`VerifyTokenModel`).
    * Décode le token URL-safe (`decode_url_safe_token`).
    * Si le token est valide et de type "verification", met à jour le statut `is_verified` de l'utilisateur.
* **`/login` (POST)**:
    * Permet à un utilisateur de se connecter.
    * Prend en entrée email et mot de passe (`UserLoginModel`).
    * Vérifie les identifiants (`verify_password`) et si le compte est vérifié.
    * Si la connexion réussit, génère un `access_token` et un `refresh_token` JWT (`create_access_token`).
    * Retourne les tokens et des informations utilisateur de base.
* **`/refresh-token` (POST)**:
    * Permet d'obtenir un nouveau `access_token` en utilisant un `refresh_token` valide.
    * Le `refresh_token` est validé par `RefreshTokenBearer`.
    * Vérifie que le compte de l'utilisateur est toujours vérifié.
    * Génère un nouvel `access_token`.
* **`/me` (GET)**:
    * Retourne les informations détaillées de l'utilisateur actuellement connecté et vérifié (`UserDetailModel`).
    * Protégé par `AccessTokenBearer` et `RoleChecker`.
* **`/logout` (POST)**:
    * Déconnecte l'utilisateur en ajoutant le JTI (JWT ID) de l'`access_token` à une blocklist Redis (`add_jti_to_blocklist`).
    * Protégé par `AccessTokenBearer`.
* **`/password-reset-request` (POST)**:
    * Permet à un utilisateur de demander une réinitialisation de son mot de passe.
    * Prend l'email de l'utilisateur (`PasswordResetRequestModel`).
    * Si l'utilisateur existe, génère un token URL-safe de type "password\_reset" et envoie un email contenant un lien vers le frontend.
* **`/password-reset-confirm` (POST)**:
    * Permet à un utilisateur de définir un nouveau mot de passe en utilisant un token valide et en fournissant le nouveau mot de passe (`PasswordResetConfirmModel`).
    * Décode le token URL-safe, vérifie sa validité et son type.
    * Met à jour le hash du mot de passe de l'utilisateur.
* **`/validate-reset-token/{token}` (GET)**:
    * Valide un token de réinitialisation de mot de passe (utilisé par le frontend avant d'afficher le formulaire de saisie du nouveau mot de passe).
    * Retourne un statut de validité et l'email associé si le token est correct.

### 2. `schemas.py` - Modèles de Données Pydantic

Ce fichier définit les structures de données attendues en entrée et en sortie des endpoints API, en utilisant Pydantic pour la validation.

* `UserCreateModel`: Utilisé pour l'inscription, avec des contraintes de longueur pour les champs.
* `UserModel`: Représentation standard d'un utilisateur, excluant le hash du mot de passe.
* `UserDetailModel`: Modèle `UserModel` étendu pour inclure des informations liées (par exemple, les conversations).
* `UserLoginModel`: Pour les requêtes de connexion.
* `EmailModel`, `SingleEmailModel`: Pour les requêtes nécessitant un ou plusieurs emails.
* `PasswordResetRequestModel`: Pour la demande de réinitialisation de mot de passe.
* `PasswordResetConfirmModel`: Pour la confirmation de réinitialisation de mot de passe, incluant le token et les nouveaux mots de passe.
* `VerifyTokenModel`: Pour recevoir le token de vérification d'email dans le corps d'une requête POST.
* `TokenValidationResponse`: Pour la réponse de l'endpoint de validation de token.

La configuration `model_config = ConfigDict(from_attributes=True)` est utilisée pour permettre la création de modèles Pydantic à partir d'objets ORM (SQLModel).

### 3. `service.py` - Logique Métier des Utilisateurs

La classe `UserService` encapsule la logique d'interaction avec la base de données pour les opérations liées aux utilisateurs.

* `get_user_by_email(email, session)`: Récupère un utilisateur par son adresse email.
* `user_exists(email, session)`: Vérifie si un utilisateur avec l'email donné existe.
* `create_user(user_data, session)`: Crée un nouvel utilisateur. Hache le mot de passe en utilisant `generate_passwd_hash` et assigne un rôle par défaut.
* `update_user(user, user_data, session)`: Met à jour les attributs d'un utilisateur existant.

### 4. `utils.py` - Utilitaires d'Authentification

Ce fichier contient des fonctions d'aide cruciales pour la sécurité et la gestion des tokens.

* `passwd_context`: Instance de `CryptContext` de `passlib` configurée avec l'algorithme `bcrypt` pour le hachage des mots de passe.
* `generate_passwd_hash(password)`: Génère un hash sécurisé pour un mot de passe.
* `verify_password(password, hash)`: Vérifie un mot de passe en clair par rapport à un hash stocké.
* `create_access_token(user_data, expiry, refresh)`: Crée un token JWT (accès ou rafraîchissement).
    * Le payload inclut les données utilisateur, une date d'expiration (`exp`), un identifiant unique de token (`jti`), et un booléen `refresh`.
    * Utilise `Config.JWT_SECRET` et `Config.JWT_ALGORITHM` pour l'encodage.
* `decode_token(token)`: Décode et valide un token JWT.
    * Gère les erreurs `PyJWTError` (par exemple, token expiré, signature invalide).
* `serializer`: Instance de `URLSafeTimedSerializer` de `itsdangerous` pour créer des tokens sécurisés pour les URLs (vérification email, reset mot de passe). Utilise `Config.JWT_SECRET` comme clé secrète.
* `create_url_safe_token(data)`: Génère un token sérialisé et signé pour les URLs.
* `decode_url_safe_token(token)`: Décode et valide un token URL-safe.

### 5. `dependencies.py` - Dépendances de Sécurité FastAPI

Ce fichier définit des classes de dépendances réutilisables pour sécuriser les endpoints FastAPI.

* `TokenBearer(HTTPBearer)`: Classe de base pour la validation des tokens JWT.
    * Vérifie la validité du token (`decode_token`).
    * Vérifie si le JTI du token est dans la blocklist Redis (`token_in_blocklist`).
    * Définit une méthode `verify_token_data` à surcharger par les classes filles.
* `AccessTokenBearer(TokenBearer)`: Vérifie que le token fourni est un token d'accès (et non de rafraîchissement).
* `RefreshTokenBearer(TokenBearer)`: Vérifie que le token fourni est un token de rafraîchissement.
* `get_current_user(token_details, session)`: Dépendance pour obtenir l'objet `User` complet à partir des informations du token d'accès validé.
* `RoleChecker(allowed_roles)`: Dépendance pour vérifier si l'utilisateur actuel a un rôle autorisé et si son compte est vérifié.

L'ensemble de ces composants forme un système d'authentification robuste et complet pour l'application.

---

Le prochain module API que nous allons examiner est celui des [Conversations (`src/conversations/`)](./conversations.md).