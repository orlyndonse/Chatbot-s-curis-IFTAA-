# source code/backend/src/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
import os # Import os

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_HOST:str="localhost"
    REDIS_PORT:int=6379
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
    DOMAIN: str
    FRONTEND_URL: str = "http://localhost:3000"
    GEMINI_API_KEY: str

    # --- ADD THIS ---
    # Define a base directory for uploads. Ensure this directory exists or is created by your app.
    # Example: 'uploaded_files' in your backend's root directory
    UPLOAD_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploaded_files")
    # --- END ADDITION ---


    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

Config = Settings()

# --- ADD THIS: Ensure UPLOAD_DIR exists ---
if not os.path.exists(Config.UPLOAD_DIR):
    os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
# --- END ADDITION ---