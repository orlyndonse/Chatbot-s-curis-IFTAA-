from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError
import logging

# Configuration du logger
logger = logging.getLogger(__name__)

# Classe de base pour toutes les exceptions personnalisées de l'application
class ChatAppException(Exception):
    """Classe de base pour les exceptions personnalisées de l'application."""
    def __init__(self, detail: str = "Une erreur est survenue."):
        self.detail = detail
        super().__init__(self.detail)

# === EXCEPTIONS LIÉES À L'AUTHENTIFICATION ===

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

class AccountNotVerified(ChatAppException):
    """Le compte utilisateur n'a pas encore été vérifié."""
    def __init__(self, detail: str = "Compte non vérifié"):
        super().__init__(detail)

class TokenExpired(ChatAppException):
    """Le token (généralement pour la réinitialisation) a expiré."""
    def __init__(self, detail: str = "Token expiré"):
        super().__init__(detail)

# === EXCEPTIONS LIÉES AUX RESSOURCES DE L'APPLICATION ===

class ConversationNotFound(ChatAppException):
    """La conversation spécifiée n'a pas été trouvée."""
    def __init__(self, detail: str = "Conversation non trouvée"):
        super().__init__(detail)

class MessageNotFound(ChatAppException):
    """Le message spécifié n'a pas été trouvé."""
    def __init__(self, detail: str = "Message non trouvé"):
        super().__init__(detail)

class DocumentNotFound(ChatAppException):
    """Le document spécifié n'a pas été trouvé."""
    def __init__(self, detail: str = "Document non trouvé"):
        super().__init__(detail)

class ForbiddenAccess(ChatAppException):
    """L'utilisateur tente d'accéder à une ressource qui ne lui appartient pas."""
    def __init__(self, detail: str = "Accès non autorisé"):
        super().__init__(detail)

# === EXCEPTIONS LIÉES À LA VALIDATION DES DONNÉES ===

class ValidationError(ChatAppException):
    """Erreur de validation des données d'entrée."""
    def __init__(self, detail: str = "Données invalides"):
        super().__init__(detail)

class FileUploadError(ChatAppException):
    """Erreur lors du téléchargement de fichier."""
    def __init__(self, detail: str = "Erreur lors du téléchargement du fichier"):
        super().__init__(detail)

class FileTooLarge(ChatAppException):
    """Le fichier téléchargé est trop volumineux."""
    def __init__(self, detail: str = "Le fichier est trop volumineux"):
        super().__init__(detail)

class UnsupportedFileType(ChatAppException):
    """Type de fichier non supporté."""
    def __init__(self, detail: str = "Type de fichier non supporté"):
        super().__init__(detail)

# === EXCEPTIONS LIÉES AUX SERVICES EXTERNES ===

class ExternalServiceError(ChatAppException):
    """Erreur lors de l'appel à un service externe."""
    def __init__(self, detail: str = "Erreur du service externe"):
        super().__init__(detail)

class APIRateLimitExceeded(ChatAppException):
    """Limite de taux d'API dépassée."""
    def __init__(self, detail: str = "Limite de taux dépassée"):
        super().__init__(detail)

# === EXCEPTIONS LIÉES AUX OPÉRATIONS ===

class OperationNotAllowed(ChatAppException):
    """L'opération demandée n'est pas autorisée dans le contexte actuel."""
    def __init__(self, detail: str = "Opération non autorisée"):
        super().__init__(detail)

class ResourceLimitExceeded(ChatAppException):
    """Limite de ressource dépassée."""
    def __init__(self, detail: str = "Limite de ressource dépassée"):
        super().__init__(detail)

# === FABRIQUE DE GESTIONNAIRES D'EXCEPTIONS ===

def create_exception_handler(
    status_code: int, initial_detail: Any, error_code: str
) -> Callable[[Request, ChatAppException], JSONResponse]:
    """Crée une fonction handler pour une exception spécifique."""

    async def exception_handler(request: Request, exc: ChatAppException):
        # Log l'erreur pour le débogage
        logger.warning(
            f"Handled Exception: {exc.__class__.__name__} - "
            f"Path: {request.url.path} - "
            f"Method: {request.method} - "
            f"Detail: {exc.detail}"
        )
        
        # Prépare la réponse JSON avec le détail de l'exception
        content = {}
        if isinstance(initial_detail, dict):
            content = initial_detail.copy()
            content["error_code"] = error_code
            content["message"] = exc.detail
        elif isinstance(initial_detail, str):
            content = {"message": exc.detail, "error_code": error_code}
        else:
            content = {"message": exc.detail, "error_code": error_code}

        return JSONResponse(content=content, status_code=status_code)

    return exception_handler

# === ENREGISTREMENT DES GESTIONNAIRES D'EXCEPTIONS ===

def register_all_errors(app: FastAPI):
    """Enregistre tous les handlers d'exceptions personnalisées pour l'application FastAPI."""

    # === ERREURS D'AUTHENTIFICATION ===
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
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
            status_code=status.HTTP_401_UNAUTHORIZED,
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
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={"message": "Un refresh token valide est requis."},
            error_code="REFRESH_TOKEN_REQUIRED",
        ),
    )
    
    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
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
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={"message": "Le token ou le lien a expiré."},
            error_code="TOKEN_EXPIRED",
        ),
    )

    # === ERREURS LIÉES AUX RESSOURCES ===
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
        DocumentNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={"message": "Document non trouvé."},
            error_code="DOCUMENT_NOT_FOUND",
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

    # === ERREURS DE VALIDATION ===
    app.add_exception_handler(
        ValidationError,
        create_exception_handler(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            initial_detail={"message": "Données invalides."},
            error_code="VALIDATION_ERROR",
        ),
    )
    
    app.add_exception_handler(
        FileUploadError,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={"message": "Erreur lors du téléchargement du fichier."},
            error_code="FILE_UPLOAD_ERROR",
        ),
    )
    
    app.add_exception_handler(
        FileTooLarge,
        create_exception_handler(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            initial_detail={"message": "Le fichier est trop volumineux."},
            error_code="FILE_TOO_LARGE",
        ),
    )
    
    app.add_exception_handler(
        UnsupportedFileType,
        create_exception_handler(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            initial_detail={"message": "Type de fichier non supporté."},
            error_code="UNSUPPORTED_FILE_TYPE",
        ),
    )

    # === ERREURS DE SERVICES EXTERNES ===
    app.add_exception_handler(
        ExternalServiceError,
        create_exception_handler(
            status_code=status.HTTP_502_BAD_GATEWAY,
            initial_detail={"message": "Erreur du service externe."},
            error_code="EXTERNAL_SERVICE_ERROR",
        ),
    )
    
    app.add_exception_handler(
        APIRateLimitExceeded,
        create_exception_handler(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            initial_detail={
                "message": "Limite de taux dépassée.",
                "resolution": "Veuillez réessayer plus tard.",
            },
            error_code="API_RATE_LIMIT_EXCEEDED",
        ),
    )

    # === ERREURS D'OPÉRATIONS ===
    app.add_exception_handler(
        OperationNotAllowed,
        create_exception_handler(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            initial_detail={"message": "Opération non autorisée."},
            error_code="OPERATION_NOT_ALLOWED",
        ),
    )
    
    app.add_exception_handler(
        ResourceLimitExceeded,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_detail={"message": "Limite de ressource dépassée."},
            error_code="RESOURCE_LIMIT_EXCEEDED",
        ),
    )

    # === GESTIONNAIRES D'ERREURS GÉNÉRIQUES ===
    @app.exception_handler(SQLAlchemyError)
    async def database_error_handler(request: Request, exc: SQLAlchemyError):
        """Gère les erreurs de base de données SQLAlchemy."""
        # Log l'erreur complète pour le débogage sans exposer les détails à l'utilisateur
        logger.exception(
            f"Database Error - Path: {request.url.path} - "
            f"Method: {request.method} - Error: {str(exc)}"
        )
        return JSONResponse(
            content={
                "message": "Une erreur est survenue lors de l'accès à la base de données.",
                "error_code": "DATABASE_ERROR",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        """Capture toutes les erreurs non prévues pour éviter les crashes."""
        logger.exception(
            f"Unhandled Exception - Path: {request.url.path} - "
            f"Method: {request.method} - Type: {type(exc).__name__} - "
            f"Error: {str(exc)}"
        )
        return JSONResponse(
            content={
                "message": "Une erreur interne inattendue est survenue.",
                "error_code": "INTERNAL_SERVER_ERROR",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

# === UTILITAIRES POUR LA GESTION D'ERREURS ===

def get_error_details(exc: ChatAppException) -> dict:
    """Extrait les détails d'une exception pour le logging."""
    return {
        "exception_type": exc.__class__.__name__,
        "detail": exc.detail,
    }

def log_exception(exc: ChatAppException, request: Request = None):
    """Log une exception avec les détails appropriés."""
    error_details = get_error_details(exc)
    if request:
        error_details.update({
            "path": request.url.path,
            "method": request.method,
        })
    
    logger.warning(f"ChatApp Exception: {error_details}")

# === CONSTANTES D'ERREURS ===

class ErrorCodes:
    """Constantes pour les codes d'erreur."""
    # Authentification
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    INVALID_TOKEN = "INVALID_TOKEN"
    TOKEN_REVOKED = "TOKEN_REVOKED"
    ACCESS_TOKEN_REQUIRED = "ACCESS_TOKEN_REQUIRED"
    REFRESH_TOKEN_REQUIRED = "REFRESH_TOKEN_REQUIRED"
    INSUFFICIENT_PERMISSIONS = "INSUFFICIENT_PERMISSIONS"
    ACCOUNT_NOT_VERIFIED = "ACCOUNT_NOT_VERIFIED"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    
    # Ressources
    CONVERSATION_NOT_FOUND = "CONVERSATION_NOT_FOUND"
    MESSAGE_NOT_FOUND = "MESSAGE_NOT_FOUND"
    DOCUMENT_NOT_FOUND = "DOCUMENT_NOT_FOUND"
    FORBIDDEN_ACCESS = "FORBIDDEN_ACCESS"
    
    # Validation
    VALIDATION_ERROR = "VALIDATION_ERROR"
    FILE_UPLOAD_ERROR = "FILE_UPLOAD_ERROR"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    UNSUPPORTED_FILE_TYPE = "UNSUPPORTED_FILE_TYPE"
    
    # Services externes
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
    API_RATE_LIMIT_EXCEEDED = "API_RATE_LIMIT_EXCEEDED"
    
    # Opérations
    OPERATION_NOT_ALLOWED = "OPERATION_NOT_ALLOWED"
    RESOURCE_LIMIT_EXCEEDED = "RESOURCE_LIMIT_EXCEEDED"
    
    # Système
    DATABASE_ERROR = "DATABASE_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"