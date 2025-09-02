import logging
import uuid
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer

import jwt
from passlib.context import CryptContext

from src.config import Config

# Contexte de hachage de mot de passe utilisant bcrypt
passwd_context = CryptContext(schemes=["bcrypt"])

# Durée d'expiration par défaut des tokens d'accès (1 heure)
ACCESS_TOKEN_EXPIRY = 3600


# Génère un hash sécurisé pour un mot de passe
def generate_passwd_hash(password: str) -> str:
    hash = passwd_context.hash(password)

    return hash


# Vérifie si un mot de passe correspond à un hash
def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)


# Crée un token JWT avec les données utilisateur
def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):
    payload = {}

    payload["user"] = user_data
    # Définit la date d'expiration du token
    payload["exp"] = datetime.now() + (
        expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    )
    # Identifiant unique du token (pour la révocation)
    payload["jti"] = str(uuid.uuid4())
    # Indique si c'est un token de rafraîchissement
    payload["refresh"] = refresh

    # Encode le token avec la clé secrète et l'algorithme configurés
    token = jwt.encode(
        payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM
    )

    return token


# Décode et valide un token JWT
def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM]
        )

        return token_data

    except jwt.PyJWTError as e:
        logging.exception(e)
        return None

# Serializer pour créer des tokens sécurisés pour les URLs (verification email, etc.)
serializer = URLSafeTimedSerializer(
    secret_key=Config.JWT_SECRET, salt="email-configuration"
)

# Crée un token sécurisé pour les URLs
def create_url_safe_token(data: dict):
    token = serializer.dumps(data)

    return token

# Décode et valide un token sécurisé pour les URLs
def decode_url_safe_token(token:str):
    try:
        token_data = serializer.loads(token)

        return token_data
    
    except Exception as e:
        logging.error(str(e))