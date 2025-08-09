---
sidebar_position: 5
title: Gestion des Erreurs (src/errors.py)
---

# Gestion des Erreurs (`src/errors.py`)

Le fichier `src/errors.py` joue un rôle crucial dans la manière dont l'application backend gère et répond aux erreurs. Il définit une série d'exceptions personnalisées et une factory pour créer des gestionnaires d'exceptions FastAPI, garantissant ainsi des réponses d'erreur cohérentes et informatives pour le client.

## Objectifs

* **Centralisation des Exceptions Métier** : Définir des classes d'exception spécifiques pour les erreurs courantes de l'application (par exemple, utilisateur non trouvé, token invalide, etc.).
* **Réponses d'Erreur Structurées** : Assurer que les erreurs API renvoient des réponses JSON standardisées avec des codes de statut HTTP appropriés et des messages clairs.
* **Extensibilité** : Faciliter l'ajout de nouvelles exceptions personnalisées et de leurs gestionnaires.

## Structure du Fichier

### 1. Classe de Base `ChatAppException`

```python
# Extrait de src/errors.py
class ChatAppException(Exception):
    """Classe de base pour les exceptions personnalisées de l'application."""
    def __init__(self, detail: str = "Une erreur est survenue."):
        self.detail = detail
        super().__init__(self.detail)
```

Toutes les exceptions personnalisées de l'application héritent de cette classe de base. Elle prend un argument `detail` qui contient le message d'erreur spécifique.

### 2. Exceptions Personnalisées Spécifiques

Une série d'exceptions sont définies, héritant de `ChatAppException`, pour couvrir divers scénarios d'erreur. En voici quelques exemples :

#### Exceptions d'Authentification (Auth Exceptions)

- **InvalidToken** : Token invalide ou expiré.
- **RevokedToken** : Token révoqué (par exemple, après une déconnexion).
- **AccessTokenRequired** : Un token d'accès est attendu, mais un token de rafraîchissement a été fourni.
- **RefreshTokenRequired** : Inversement, un token de rafraîchissement est attendu.
- **UserAlreadyExists** : Tentative de création d'un utilisateur avec un email déjà existant.
- **InvalidCredentials** : Email ou mot de passe incorrect lors de la connexion.
- **InsufficientPermission** : L'utilisateur n'a pas les droits nécessaires pour une action.
- **UserNotFound** : L'utilisateur spécifié n'a pas été trouvé.
- **AccountNotVerified** : Le compte utilisateur n'a pas encore été vérifié par email.
- **TokenExpired** : Un token (généralement pour la vérification d'email ou la réinitialisation de mot de passe) a expiré.

#### Exceptions de Ressources/Application (Resource/App Exceptions)

- **ConversationNotFound** : La conversation spécifiée n'a pas été trouvée.
- **MessageNotFound** : Le message spécifié n'a pas été trouvé.
- **DocumentNotFound** : Le document spécifié n'a pas été trouvé.
- **ForbiddenAccess** : L'utilisateur tente d'accéder à une ressource qui ne lui appartient pas ou pour laquelle il n'a pas les droits.

### 3. Factory de Gestionnaires d'Exceptions (`create_exception_handler`)

```python
# Extrait de src/errors.py
def create_exception_handler(
    status_code: int, initial_detail: Any, error_code: str
) -> Callable[[Request, ChatAppException], JSONResponse]:
    """Crée une fonction handler pour une exception spécifique."""

    async def exception_handler(request: Request, exc: ChatAppException):
        logging.warning(
            f"Handled Exception: {exc.__class__.__name__} - Path: {request.url.path} - Detail: {exc.detail}"
        )
        content = {}
        if isinstance(initial_detail, dict):
            content = initial_detail.copy()
            content["error_code"] = error_code
            content["message"] = exc.detail
        elif isinstance(initial_detail, str):
             content = {"message": exc.detail, "error_code": error_code}

        return JSONResponse(content=content, status_code=status_code)

    return exception_handler
```

Cette fonction est une factory qui génère des fonctions `exception_handler` spécifiques pour FastAPI. Chaque handler :

- Loggue l'exception gérée.
- Construit une réponse JSON structurée contenant un message (provenant du `detail` de l'exception levée) et un `error_code` spécifique.
- Renvoie la `JSONResponse` avec le `status_code` HTTP approprié.

### 4. Enregistrement des Gestionnaires d'Erreurs (`register_all_errors`)

```python
# Extrait de src/errors.py
def register_all_errors(app: FastAPI):
    """Enregistre tous les handlers d'exceptions personnalisées pour l'application FastAPI."""

    # Auth Errors
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_detail={"message": "Un utilisateur avec cet email existe déjà."},
            error_code="USER_ALREADY_EXISTS",
        ),
    )
    # ... (autres handlers pour les exceptions d'authentification) ...

    # Resource/App Errors
    app.add_exception_handler(
        ConversationNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={"message": "Conversation non trouvée."},
            error_code="CONVERSATION_NOT_FOUND",
        ),
    )
    # ... (autres handlers pour les exceptions de ressources) ...

    # Generic Handlers
    @app.exception_handler(SQLAlchemyError)
    async def database_error_handler(request: Request, exc: SQLAlchemyError):
        # ...
        return JSONResponse(...)

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        # ...
        return JSONResponse(...)
```

La fonction `register_all_errors(app: FastAPI)` est appelée dans `src/__init__.py` pour associer chaque classe d'exception personnalisée à un handler généré par `create_exception_handler`. Elle enregistre également des handlers génériques pour les erreurs `SQLAlchemyError` et les exceptions `Exception` non interceptées, assurant ainsi que toutes les erreurs potentielles sont gérées de manière contrôlée.

## Avantages de cette Approche

Cette approche centralisée et structurée de la gestion des erreurs améliore :

- **Robustesse** : Toutes les erreurs sont capturées et gérées de manière cohérente
- **Maintenabilité** : Les exceptions et leurs handlers sont centralisés et facilement modifiables
- **Expérience utilisateur** : Des retours d'erreur clairs et standardisés pour les clients de l'API
- **Débogage** : Logging automatique de toutes les exceptions avec contexte
- **Extensibilité** : Facilité d'ajout de nouvelles exceptions personnalisées

Cette gestion des erreurs robuste garantit que l'application backend fournit des réponses cohérentes et informatives, améliorant ainsi l'expérience des développeurs frontend et la fiabilité générale du système.

---

Après avoir examiné la gestion des erreurs, nous allons nous pencher sur les Modules API Principaux, en commençant par [le module d'authentification](../backend/api-modules/auth.md).