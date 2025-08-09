from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError
import logging # Import logging

# --- Base Exception ---
class ChatAppException(Exception):
    """Classe de base pour les exceptions personnalisées de l'application."""
    def __init__(self, detail: str = "Une erreur est survenue."):
        self.detail = detail
        super().__init__(self.detail)

# --- Auth Exceptions ---
class InvalidToken(ChatAppException):
    """Le token fourni est invalide ou a expiré."""
    def __init__(self, detail: str = "Token invalide ou expiré"):
        super().__init__(detail)

class RevokedToken(ChatAppException):
    """Le token fourni a été révoqué."""
    def __init__(self, detail: str = "Token révoqué"):
        super().__init__(detail)

class AccessTokenRequired(ChatAppException):
    """Un access token est requis, mais un refresh token a été fourni."""
    def __init__(self, detail: str = "Access token requis"):
        super().__init__(detail)

class RefreshTokenRequired(ChatAppException):
    """Un refresh token est requis, mais un access token a été fourni."""
    def __init__(self, detail: str = "Refresh token requis"):
        super().__init__(detail)

class UserAlreadyExists(ChatAppException):
    """L'email fourni existe déjà lors de l'inscription."""
    def __init__(self, detail: str = "Un utilisateur avec cet email existe déjà"):
        super().__init__(detail)

class InvalidCredentials(ChatAppException):
    """Email ou mot de passe incorrect lors de la connexion."""
    def __init__(self, detail: str = "Email ou mot de passe incorrect"):
        super().__init__(detail)

class InsufficientPermission(ChatAppException):
    """L'utilisateur n'a pas les permissions nécessaires."""
    def __init__(self, detail: str = "Permissions insuffisantes"):
        super().__init__(detail)

class UserNotFound(ChatAppException):
    """Utilisateur non trouvé dans la base de données."""
    def __init__(self, detail: str = "Utilisateur non trouvé"):
        super().__init__(detail)

class AccountNotVerified(ChatAppException): # Hérite de ChatAppException pour la cohérence
    """Le compte utilisateur n'a pas encore été vérifié."""
    def __init__(self, detail: str = "Compte non vérifié"):
        super().__init__(detail)

class TokenExpired(ChatAppException): # Hérite de ChatAppException
    """Le token (généralement pour la réinitialisation) a expiré."""
    def __init__(self, detail: str = "Token expiré"):
        super().__init__(detail)

# --- Resource/App Exceptions ---
class ConversationNotFound(ChatAppException): # Renamed from Table3NotFound
    """La conversation spécifiée n'a pas été trouvée."""
    def __init__(self, detail: str = "Conversation non trouvée"):
        super().__init__(detail)

# Remove Table3AlreadyExists if not applicable, or rename:
# class ConversationAlreadyExists(ChatAppException):
#     """Une conversation similaire existe déjà (si besoin)."""
#     def __init__(self, detail: str = "Conversation existe déjà"):
#         super().__init__(detail)

class MessageNotFound(ChatAppException): # Nouvelle exception pour les messages
    """Le message spécifié n'a pas été trouvé."""
    def __init__(self, detail: str = "Message non trouvé"):
        super().__init__(detail)

class MessageNotFound(ChatAppException): # Nouvelle exception pour les messages
    """Le message spécifié n'a pas été trouvé."""
    def __init__(self, detail: str = "Message non trouvé"):
        super().__init__(detail)

# N'oublie pas de l'enregistrer dans register_all_errors
# app.add_exception_handler(
#     MessageNotFound,
#     create_exception_handler(
#         status_code=status.HTTP_404_NOT_FOUND,
#         initial_detail={"message": "Message non trouvé."},
#         error_code="MESSAGE_NOT_FOUND",
#     ),
# )

class DocumentNotFound(ChatAppException): # Renamed from Table3NotFound
    """Le document spécifiée n'a pas été trouvée."""
    def __init__(self, detail: str = "Document non trouvée"):
        super().__init__(detail)

class ForbiddenAccess(ChatAppException): # Pour les problèmes de droits d'accès
    """L'utilisateur tente d'accéder à une ressource qui ne lui appartient pas."""
    def __init__(self, detail: str = "Accès non autorisé"):
        super().__init__(detail)

# --- Exception Handler Factory ---
def create_exception_handler(
    status_code: int, initial_detail: Any, error_code: str
) -> Callable[[Request, ChatAppException], JSONResponse]:
    """Crée une fonction handler pour une exception spécifique."""

    async def exception_handler(request: Request, exc: ChatAppException):
        # Log l'erreur gérée
        logging.warning(
            f"Handled Exception: {exc.__class__.__name__} - Path: {request.url.path} - Detail: {exc.detail}"
        )
        # Prépare le contenu de la réponse JSON
        content = {}
        if isinstance(initial_detail, dict):
            content = initial_detail.copy() # Copie pour éviter de modifier l'original
            content["error_code"] = error_code
            # Utilise le détail spécifique de l'exception levée
            content["message"] = exc.detail
        elif isinstance(initial_detail, str):
             content = {"message": exc.detail, "error_code": error_code}

        return JSONResponse(content=content, status_code=status_code)

    return exception_handler

# --- Register Error Handlers ---
def register_all_errors(app: FastAPI):
    """Enregistre tous les handlers d'exceptions personnalisées pour l'application FastAPI."""

    # Auth Errors
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT, # 409 Conflit est plus approprié
            initial_detail={"message": "Un utilisateur avec cet email existe déjà."},
            error_code="USER_ALREADY_EXISTS",
        ),
    )
    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={"message": "Utilisateur non trouvé."},
            error_code="USER_NOT_FOUND",
        ),
    )
    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED, # 401 Non autorisé
            initial_detail={"message": "Email ou mot de passe incorrect."},
            error_code="INVALID_CREDENTIALS",
        ),
    )
    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Le token est invalide ou expiré.",
                "resolution": "Veuillez obtenir un nouveau token.",
            },
            error_code="INVALID_TOKEN",
        ),
    )
    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Le token a été révoqué.",
                "resolution": "Veuillez vous reconnecter.",
            },
            error_code="TOKEN_REVOKED",
        ),
    )
    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={"message": "Un access token est requis pour cette opération."},
            error_code="ACCESS_TOKEN_REQUIRED",
        ),
    )
    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED, # Peut aussi être 401
            initial_detail={"message": "Un refresh token valide est requis."},
            error_code="REFRESH_TOKEN_REQUIRED",
        ),
    )
    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN, # 403 Interdit
            initial_detail={"message": "Permissions insuffisantes pour effectuer cette action."},
            error_code="INSUFFICIENT_PERMISSIONS",
        ),
    )
    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Votre compte n'est pas vérifié.",
                "resolution": "Veuillez vérifier votre email pour activer votre compte.",
            },
            error_code="ACCOUNT_NOT_VERIFIED",
        ),
    )
    app.add_exception_handler(
        TokenExpired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED, # Ou 410 Gone
            initial_detail={"message": "Le token ou le lien a expiré."},
            error_code="TOKEN_EXPIRED",
        ),
    )

    # Resource/App Errors
    app.add_exception_handler(
        ConversationNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={"message": "Conversation non trouvée."},
            error_code="CONVERSATION_NOT_FOUND",
        ),
    )
    app.add_exception_handler(
        MessageNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={"message": "Message non trouvé."},
            error_code="MESSAGE_NOT_FOUND",
        ),
    )
    app.add_exception_handler(
        ForbiddenAccess,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={"message": "Accès non autorisé à cette ressource."},
            error_code="FORBIDDEN_ACCESS",
        ),
    )

    app.add_exception_handler(
        MessageNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={"message": "Message non trouvé."},
            error_code="MESSAGE_NOT_FOUND",
        ),
    )

    app.add_exception_handler(
        DocumentNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={"document": "Document non trouvé."},
            error_code="MESSAGE_NOT_FOUND",
        ),
    )
    # Supprimez les handlers pour QuestionNotFound, Table3NotFound, Table3AlreadyExists s'ils ne sont plus pertinents

    # --- Generic Handlers ---
    @app.exception_handler(SQLAlchemyError)
    async def database_error_handler(request: Request, exc: SQLAlchemyError):
        # Log la vraie erreur pour le débogage
        logging.exception("Database Error Occurred") # Utilise logging.exception pour la trace complète
        return JSONResponse(
            content={
                "message": "Une erreur est survenue lors de l'accès à la base de données.",
                "error_code": "DATABASE_ERROR",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(Exception) # Handler générique pour les erreurs non prévues
    async def generic_exception_handler(request: Request, exc: Exception):
        logging.exception("Unhandled Exception Occurred") # Log la trace complète
        return JSONResponse(
            content={
                "message": "Une erreur interne inattendue est survenue.",
                "error_code": "INTERNAL_SERVER_ERROR",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )