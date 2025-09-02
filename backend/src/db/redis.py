from redis import asyncio as aioredis

from src.config import Config

# Durée d'expiration des tokens en blocklist (en secondes) - 1 heure
JTI_EXPIRY = 3600

# Connexion Redis pour gérer la liste noire des tokens JWT
token_blocklist = aioredis.StrictRedis(
    host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0
)

async def add_jti_to_blocklist(jti: str) -> None:
    """
    Ajoute un JTI (JWT ID) à la liste noire des tokens
    Le token expire automatiquement après JTI_EXPIRY secondes
    """
    await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)


async def token_in_blocklist(jti: str) -> bool:
    """
    Vérifie si un JTI est présent dans la liste noire
    Retourne True si le token est blacklisté, False sinon
    """
    jti = await token_blocklist.get(jti)

    return jti is not None