from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import User

from .schemas import UserCreateModel
from .utils import generate_passwd_hash


class UserService:
    # Récupère un utilisateur par son adresse email
    async def get_user_by_email(self, email: str, session: AsyncSession):
        # Crée une requête SQL pour sélectionner l'utilisateur avec l'email donné
        statement = select(User).where(User.email == email)

        # Exécute la requête de manière asynchrone
        result = await session.exec(statement)

        # Récupère le premier résultat (ou None si aucun utilisateur trouvé)
        user = result.first()

        return user

    # Vérifie si un utilisateur existe déjà avec l'email donné
    async def user_exists(self, email, session: AsyncSession):
        # Utilise get_user_by_email pour vérifier l'existence
        user = await self.get_user_by_email(email, session)

        # Retourne True si l'utilisateur existe, False sinon
        return True if user is not None else False

    # Crée un nouvel utilisateur dans la base de données
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        # Convertit le modèle Pydantic en dictionnaire
        user_data_dict = user_data.model_dump()

        # Crée une instance User à partir des données
        new_user = User(**user_data_dict)

        # Génère le hash du mot de passe (ne stocke jamais les mots de passe en clair)
        new_user.password_hash = generate_passwd_hash(user_data_dict["password"])
        # Définit le rôle par défaut
        new_user.role = "user"

        # Ajoute le nouvel utilisateur à la session
        session.add(new_user)

        # Valide la transaction en base de données
        await session.commit()

        return new_user

    # Met à jour les informations d'un utilisateur existant
    async def update_user(self, user: User, user_data: dict, session: AsyncSession):
        # Parcourt tous les champs à mettre à jour
        for k, v in user_data.items():
            # Modifie dynamiquement chaque attribut de l'utilisateur
            setattr(user, k, v)

        # Valide les modifications en base de données
        await session.commit()

        return user