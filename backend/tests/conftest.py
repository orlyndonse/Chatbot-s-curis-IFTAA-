from unittest.mock import Mock, AsyncMock
import pytest
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
import time
import os

# Importe l'application FastAPI principale
from src import app as original_app
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer, RefreshTokenBearer, RoleChecker

# Création des mocks pour les services et la session
mock_session = AsyncMock()  # Utiliser AsyncMock pour les opérations asynchrones
mock_user_service = Mock()

def get_mock_session():
    """Remplace la dépendance de session par un mock."""
    yield mock_session

# Mocks pour les dépendances de sécurité et de rôles
mock_access_token_bearer = AsyncMock()  # Utiliser AsyncMock pour AccessTokenBearer
mock_access_token_bearer.side_effect = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authenticated"
)
mock_refresh_token_bearer = Mock()
mock_role_checker = lambda: True  # Simplifier pour éviter les interférences

# Remplacement des dépendances dans l'application pour les tests
app = FastAPI()
app.include_router(original_app.router)
app.dependency_overrides = original_app.dependency_overrides.copy()
app.dependency_overrides[get_session] = get_mock_session
app.dependency_overrides[AccessTokenBearer] = lambda: mock_access_token_bearer
app.dependency_overrides[RefreshTokenBearer] = lambda: mock_refresh_token_bearer
app.dependency_overrides[RoleChecker] = lambda: mock_role_checker

# Configuration des middlewares pour les tests (sans TrustedHostMiddleware)
origins = [
    "http://localhost:3000",
    os.getenv("FRONTEND_URL")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.middleware("http")
async def custom_logging(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    processing_time = time.time() - start_time
    message = f"{request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {response.status_code} completed after {processing_time}s"
    print(message)
    return response

@pytest.fixture
def fake_session():
    """Fixture pour le mock de la session de base de données."""
    return mock_session

@pytest.fixture
def fake_user_service():
    """Fixture pour le mock du service utilisateur."""
    mock_user_service.reset_mock()
    return mock_user_service

@pytest.fixture
def test_client():
    """Fixture pour le client de test FastAPI."""
    return TestClient(app)