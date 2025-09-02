import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Base de données
    DATABASE_URL: str
    
    # Authentification JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    # Configuration email
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    
    # URLs et domaine
    DOMAIN: str
    FRONTEND_URL: str = "http://localhost:3000"
    
    # API externes
    GEMINI_API_KEY: str

    # Répertoire de stockage des fichiers
    UPLOAD_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploaded_files")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Instance globale de configuration
Config = Settings()

# Création du répertoire d'upload s'il n'existe pas
if not os.path.exists(Config.UPLOAD_DIR):
    os.makedirs(Config.UPLOAD_DIR, exist_ok=True)