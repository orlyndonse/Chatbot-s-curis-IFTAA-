import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status, BackgroundTasks, Body
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import (
    AccessTokenBearer,
    RefreshTokenBearer,
    RoleChecker,
    get_current_user,
)
from src.auth.schemas import (
    EmailModel, # Utilisé pour resend
    PasswordResetConfirmModel,
    PasswordResetRequestModel,
    TokenValidationResponse,
    UserCreateModel,
    UserDetailModel, # Utilisé pour /me
    UserLoginModel,
    UserModel,
    VerifyTokenModel, # Essentiel pour POST /verify-email
)
from src.auth.service import UserService
from src.auth.utils import (
    create_access_token,
    create_url_safe_token,
    decode_token, # Peut-être non utilisé directement ici, mais ok
    decode_url_safe_token,
    generate_passwd_hash,
    verify_password,
)
from src.auth.schemas import PasswordResetConfirmModel

from src.config import Config # Essentiel pour FRONTEND_URL
from src.db.main import get_session
from src.db.models import User
from src.db.redis import add_jti_to_blocklist, token_in_blocklist
from src.errors import (
    AccountNotVerified, # Important pour login/refresh
    InvalidCredentials,
    InvalidToken,
    TokenExpired, # Important pour decode_url_safe_token
    UserAlreadyExists,
    UserNotFound,
    InsufficientPermission, # Géré par RoleChecker
)
from src.mail import create_message, mail

# Initialisation du routeur et des services
auth_router = APIRouter()
user_service = UserService()
REFRESH_TOKEN_EXPIRY_DAYS = 7

# --- Routes d'authentification ---

# Route d'inscription - Crée un compte utilisateur et envoie un email de vérification
@auth_router.post(
    "/signup",
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED,
    summary="Create User Account",
    description="Registers a new user and sends a verification email."
)
async def create_user_account(
    user_data: UserCreateModel,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    """Crée un compte utilisateur et envoie un email de vérification."""
    # Vérifie si l'utilisateur existe déjà
    user_exists = await user_service.user_exists(user_data.email, session)
    if user_exists:
        raise UserAlreadyExists()

    try:
        # Crée le nouvel utilisateur
        new_user = await user_service.create_user(user_data, session)
        # Génère un token de vérification sécurisé
        token = create_url_safe_token({"email": new_user.email, "type": "verification"})
        # Construit le lien de vérification pointant vers le frontend
        verification_link = f"{Config.FRONTEND_URL}/verify-email?token={token}" #

        # Contenu HTML de l'email de vérification
        html_content = f"""
        <h1>Vérifiez votre Email</h1>
        <p>Bienvenue ! Veuillez cliquer sur ce <a href="{verification_link}">lien</a> pour vérifier votre adresse email et activer votre compte.</p>
        <p>Si vous n'avez pas créé de compte, veuillez ignorer cet email.</p>
        """ # [cite: 1]
        # Crée et envoie le message email en tâche de fond
        message = create_message(
            recipients=[new_user.email],
            subject="Vérification de votre compte", # Sujet descriptif
            body=html_content
        )
        background_tasks.add_task(mail.send_message, message)
        logging.info(f"Verification email sent to {new_user.email}")
        # Retourne les informations de l'utilisateur créé
        return UserModel.model_validate(new_user)
    except Exception as e:
        logging.exception("Error during signup or email sending.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur lors de la création du compte.")


# Route pour renvoyer l'email de vérification
@auth_router.post(
    "/resend-verification-email",
    status_code=status.HTTP_200_OK,
    summary="Resend Verification Email",
)
async def resend_verification_email(
    email_data: EmailModel,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    """Renvoie l'email de vérification si le compte n'est pas encore vérifié."""
    # Extrait l'email de la requête
    email = email_data.addresses[0] if email_data.addresses else None
    if not email:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Adresse email requise.")

    # Vérifie si l'utilisateur existe et n'est pas déjà vérifié
    user = await user_service.get_user_by_email(email, session)
    if not user: raise UserNotFound()
    if user.is_verified: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ce compte est déjà vérifié.")

    # Génère un nouveau token et lien de vérification
    token = create_url_safe_token({"email": user.email, "type": "verification"})
    verification_link = f"{Config.FRONTEND_URL}/verify-email?token={token}" #

    # Contenu HTML pour le nouvel email de vérification
    html_content = f"""
    <h1>Nouvelle tentative de vérification</h1>
    <p>Veuillez cliquer <a href="{verification_link}">ici</a> pour finaliser la vérification de votre compte.</p>
    <p>Si vous n'avez pas demandé ce renvoi, veuillez ignorer cet email.</p>
    """ # [cite: 1]
    # Crée et envoie le message
    message = create_message(
        recipients=[user.email],
        subject="Vérification de compte",
        body=html_content
    )
    background_tasks.add_task(mail.send_message, message)
    logging.info(f"Resent verification email to {user.email}")
    return {"message": "Email de vérification renvoyé avec succès."}


# Route POST pour vérifier l'email avec token dans le corps de la requête
@auth_router.post( # Endpoint POST pour la vérification
    "/verify-email",
    status_code=status.HTTP_200_OK,
    summary="Verify User Email Account",
)
async def verify_user_email(
    token_data_in: VerifyTokenModel, # Utilise VerifyTokenModel pour recevoir le token dans le corps
    session: AsyncSession = Depends(get_session)
):
    """Vérifie le compte email de l'utilisateur à partir du token fourni dans le corps POST."""
    token = token_data_in.token
    try:
        # Décode et valide le token
        token_data = decode_url_safe_token(token)
        if not token_data or token_data.get("type") != "verification":
             raise InvalidToken("Token de vérification invalide ou expiré.")
        user_email = token_data.get("email")
        if not user_email:
             raise InvalidToken("Données de token invalides (email manquant).")

        # Récupère l'utilisateur et vérifie son statut
        user = await user_service.get_user_by_email(user_email, session)
        if not user: raise UserNotFound()
        if user.is_verified: return {"message": "Compte déjà vérifié."}

        # Met à jour le statut de vérification de l'utilisateur
        await user_service.update_user(user, {"is_verified": True, "verified_at": datetime.utcnow()}, session)
        logging.info(f"User account {user_email} verified successfully via POST request.")
        return {"message": "Compte vérifié avec succès ! Vous pouvez maintenant vous connecter."}
    except (InvalidToken, TokenExpired) as e:
         logging.warning(f"Email verification POST failed for token {token[:10]}...: {str(e)}")
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except UserNotFound as e:
         logging.warning(f"Email verification POST failed: User not found for token {token[:10]}...")
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logging.exception(f"Error during email verification POST process for token {token[:10]}...")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur interne lors de la vérification.")


# Route GET de redirection pour la vérification d'email (compatibilité avec anciens liens)
@auth_router.get("/verify/{token}", include_in_schema=False)
async def redirect_verify_user_account(token: str):
    """
    Redirige les requêtes GET de vérification vers la page frontend qui gère le POST.
    Utile si d'anciens liens existent ou par mesure de précaution.
    """
    logging.info(f"Redirecting verification GET request for token {token[:10]}... to frontend handler.")
    frontend_verify_url = f"{Config.FRONTEND_URL}/verify-email?token={token}" #
    return RedirectResponse(url=frontend_verify_url)


# Route de connexion utilisateur
@auth_router.post("/login", response_model=dict, summary="User Login")
async def login_users(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    # Vérifie les credentials de l'utilisateur
    user = await user_service.get_user_by_email(login_data.email, session)
    if user is None or not verify_password(login_data.password, user.password_hash):
        raise InvalidCredentials()

    # Vérification du statut 'is_verified' - empêche la connexion si non vérifié
    if not user.is_verified:
        logging.warning(f"Login attempt failed for unverified user: {user.email}")
        raise AccountNotVerified(
            detail="Votre compte n'est pas vérifié. Veuillez vérifier votre email."
        )

    # Crée les tokens d'accès et de rafraîchissement
    user_payload_data = {"email": user.email, "user_uid": str(user.uid), "role": user.role}
    refresh_payload_data = {"email": user.email, "user_uid": str(user.uid)}
    access_token = create_access_token(user_data=user_payload_data, refresh=False)
    refresh_token = create_access_token(
        user_data=refresh_payload_data,
        expiry=timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS),
        refresh=True
    )
    logging.info(f"User {user.email} logged in successfully.")
    return {
        "message": "Connexion réussie",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {"email": user.email, "uid": str(user.uid), "first_name": user.first_name},
    }


# Route pour rafraîchir le token d'accès
@auth_router.post("/refresh-token", response_model=dict, summary="Refresh Access Token")
async def refresh_access_token(
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(RefreshTokenBearer())
):
    # Extrait les données utilisateur du token de rafraîchissement
    user_data_from_refresh = token_details.get("user")
    if not user_data_from_refresh or not user_data_from_refresh.get('email'):
         raise InvalidToken("Invalid refresh token payload structure.")

    # Vérifie que l'utilisateur existe toujours
    user = await user_service.get_user_by_email(user_data_from_refresh['email'], session)
    if not user: raise InvalidToken("User associated with refresh token not found.")

    # Vérification si l'utilisateur est toujours vérifié (peut avoir été désactivé)
    if not user.is_verified:
        logging.warning(f"Refresh token attempt for now unverified user: {user.email}")
        raise AccountNotVerified(
            detail="Votre compte n'est plus vérifié. Veuillez contacter le support."
        )

    # Génère un nouveau token d'accès
    access_token_payload_data = {"email": user.email, "user_uid": str(user.uid), "role": user.role}
    new_access_token = create_access_token(user_data=access_token_payload_data, refresh=False)
    logging.info(f"Access token refreshed for user {user.email}")
    return {"access_token": new_access_token}


# Route pour obtenir les informations de l'utilisateur connecté
@auth_router.get("/me", response_model=UserDetailModel, dependencies=[Depends(RoleChecker(["admin", "user"]))], summary="Get Current User Info")
async def get_logged_in_user_info(current_user: User = Depends(get_current_user)):
    """Retourne les informations détaillées de l'utilisateur connecté et vérifié."""
    return current_user


# Route de déconnexion - ajoute le token à la blocklist
@auth_router.post("/logout", status_code=status.HTTP_200_OK, summary="User Logout")
async def logout_user(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details.get("jti")
    if jti:
        # Ajoute le JTI (JWT ID) à la blocklist pour invalider le token
        await add_jti_to_blocklist(jti)
        user_email = token_details.get("user", {}).get("email", "unknown user")
        logging.info(f"Token {jti} added to blocklist for user {user_email} upon logout.")
        return {"message": "Déconnexion réussie"}
    else:
         logging.error("Logout attempt without JTI in token details.")
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Impossible d'invalider le token.")


# Route pour demander une réinitialisation de mot de passe
@auth_router.post("/password-reset-request", status_code=status.HTTP_200_OK, summary="Request Password Reset")
async def request_password_reset(
    email_data: PasswordResetRequestModel,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    """Demande une réinitialisation de mot de passe pour l'email donné."""
    user = await user_service.get_user_by_email(email_data.email, session)
    if user:
        # Génère un token de réinitialisation sécurisé
        token = create_url_safe_token({"email": user.email, "type": "password_reset"})
        # Construit le lien de réinitialisation pointant vers le frontend
        reset_link = f"{Config.FRONTEND_URL}/reset-password?token={token}" #

        # Contenu HTML de l'email de réinitialisation
        html_content = f"""
        <h1>Réinitialisez votre mot de passe</h1>
        <p>Veuillez cliquer sur ce <a href="{reset_link}">lien</a> pour réinitialiser votre mot de passe.</p>
        <p>Ce lien expirera bientôt. Si vous n'avez pas demandé cette réinitialisation, veuillez ignorer cet email.</p>
        """ # [cite: 1]
        # Crée et envoie le message email en tâche de fond
        message = create_message(
            recipients=[user.email],
            subject="Réinitialisation de votre mot de passe",
            body=html_content
        )
        background_tasks.add_task(mail.send_message, message)
        logging.info(f"Password reset email sent to {user.email}")
    else:
        # Log mais ne révèle pas que l'email n'existe pas (pour la sécurité)
        logging.info(f"Password reset requested for non-existent email: {email_data.email}")

    return JSONResponse(content={"message": "Si un compte est associé à cet email, un lien de réinitialisation a été envoyé."}, status_code=status.HTTP_200_OK)


# Route POST pour confirmer la réinitialisation du mot de passe
@auth_router.post( # Endpoint POST pour la confirmation
    "/password-reset-confirm",
    status_code=status.HTTP_200_OK,
    summary="Confirm Password Reset",
)
async def confirm_password_reset(
    reset_data: PasswordResetConfirmModel, # Prend token + passwords du corps
    session: AsyncSession = Depends(get_session),
):
    """Réinitialise le mot de passe de l'utilisateur à partir du token et des nouveaux mots de passe."""
    token = reset_data.token
    new_password = reset_data.new_password
    confirm_new_password = reset_data.confirm_new_password

    # Validation des mots de passe
    if new_password != confirm_new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Les mots de passe ne correspondent pas.")
    if len(new_password) < 8:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Le mot de passe doit contenir au moins 8 caractères.")

    try:
        # Décode et valide le token de réinitialisation
        token_data = decode_url_safe_token(token)
        if not token_data or token_data.get("type") != "password_reset":
             raise InvalidToken("Token de réinitialisation invalide ou expiré.")
        user_email = token_data.get("email")
        if not user_email: raise InvalidToken("Données de token invalides.")

        # Récupère l'utilisateur et met à jour son mot de passe
        user = await user_service.get_user_by_email(user_email, session)
        if not user: raise UserNotFound()

        new_password_hash = generate_passwd_hash(new_password)
        await user_service.update_user(user, {"password_hash": new_password_hash}, session)

        logging.info(f"Password reset successfully for user {user_email}")
        return JSONResponse(content={"message": "Mot de passe réinitialisé avec succès."}, status_code=status.HTTP_200_OK)

    except (InvalidToken, TokenExpired) as e:
         logging.warning(f"Password reset confirmation POST failed for token {token[:10]}...: {str(e)}")
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except UserNotFound:
         logging.warning(f"Password reset confirmation POST failed: User not found for token {token[:10]}...")
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé associé à ce token.")
    except Exception as e:
        logging.exception(f"Error during password reset confirmation POST for token {token[:10]}...")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur interne lors de la réinitialisation.")


# Route GET de redirection pour la réinitialisation de mot de passe (compatibilité)
@auth_router.get("/password-reset-confirm/{token}", include_in_schema=False)
async def redirect_to_password_reset_page(token: str):
    """
    Redirige les requêtes GET de reset vers la page frontend qui gère le POST.
    """
    logging.info(f"Redirecting password reset GET request for token {token[:10]}... to frontend handler.")
    try:
        # Validation très basique pour la redirection
        decode_url_safe_token(token)
        frontend_reset_url = f"{Config.FRONTEND_URL}/reset-password?token={token}" #
        return RedirectResponse(url=frontend_reset_url)
    except Exception as e:
        logging.warning(f"Password reset GET redirection failed for token {token[:10]}...: {str(e)}")
        frontend_error_url = f"{Config.FRONTEND_URL}/link-error?reason=invalid_or_expired" #
        return RedirectResponse(url=frontend_error_url)


# Route pour valider un token de réinitialisation de mot de passe
@auth_router.get("/validate-reset-token/{token}", response_model=TokenValidationResponse, summary="Validate Password Reset Token")
async def validate_password_reset_token(token: str):
    """
    Valide un token (utilisé par le frontend avant d'afficher le formulaire de reset).
    """
    try:
        # Décode et valide le token
        token_data = decode_url_safe_token(token)
        if not token_data or token_data.get("type") != "password_reset":
            raise InvalidToken("Token invalide ou type incorrect.")
        user_email = token_data.get("email")
        if not user_email: raise InvalidToken("Données de token invalides.")

        logging.info(f"Reset token validation successful for {user_email} (token {token[:10]}...)")
        return TokenValidationResponse(valid=True, email=user_email)
    except (InvalidToken, TokenExpired) as e:
        logging.warning(f"Reset token validation failed for token {token[:10]}...: {str(e)}")
        return TokenValidationResponse(valid=False, detail=str(e))
    except Exception as e:
        logging.exception(f"Unexpected error validating reset token {token[:10]}...: {e}")
        return TokenValidationResponse(valid=False, detail="Erreur de validation du token.")


# Route de santé du service d'authentification
@auth_router.get("/ping")
async def ping():
    return {"message": "Auth service is running!"}