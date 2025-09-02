from typing import Any, List

from fastapi import Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.db.models import User
from src.db.redis import token_in_blocklist

from .service import UserService
from .utils import decode_token
from src.errors import (
    InvalidToken,
    RefreshTokenRequired,
    AccessTokenRequired,
    InsufficientPermission,
    AccountNotVerified,
)
from typing import Optional

# Instance du service utilisateur pour les opérations liées aux utilisateurs
user_service = UserService()


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        # Récupère les credentials d'authentification depuis l'en-tête Authorization
        creds = await super().__call__(request)

        # Extrait le token JWT des credentials
        token = creds.credentials

        # Décode le token pour obtenir les données
        token_data = decode_token(token)

        # Vérifie si le token est valide
        if not self.token_valid(token):
            raise InvalidToken()

        # Vérifie si le token est dans la liste noire (révoqué)
        if await token_in_blocklist(token_data["jti"]):
            raise InvalidToken()

        # Vérifie le type de token (access/refresh) selon l'implémentation enfant
        self.verify_token_data(token_data)

        return token_data

    # Vérifie la validité basique du token
    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)

        return token_data is not None

    # Méthode à implémenter dans les classes enfants pour vérifier le type de token
    def verify_token_data(self, token_data):
        raise NotImplementedError("Please Override this method in child classes")


# Bearer spécifique pour les tokens d'accès
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        # Vérifie que ce n'est pas un token de rafraîchissement
        if token_data and token_data["refresh"]:
            raise AccessTokenRequired()


# Bearer spécifique pour les tokens de rafraîchissement
class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        # Vérifie que c'est bien un token de rafraîchissement
        if token_data and not token_data["refresh"]:
            raise RefreshTokenRequired()


# Dépendance pour récupérer l'utilisateur courant à partir du token
async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    # Extrait l'email de l'utilisateur depuis le token décodé
    user_email = token_details["user"]["email"]

    # Récupère l'utilisateur depuis la base de données
    user = await user_service.get_user_by_email(user_email, session)

    return user


# Vérificateur de rôles pour la gestion des permissions
class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
        # Vérifie que le compte est vérifié
        if not current_user.is_verified:
            raise AccountNotVerified()
        
        # Vérifie que l'utilisateur a un des rôles autorisés
        if current_user.role in self.allowed_roles:
            return True

        raise InsufficientPermission()