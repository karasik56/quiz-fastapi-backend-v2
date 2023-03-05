from typing import Union

from jose import jwt, JWTError

from app.config import settings
from app.models.models import AuthUser
from app.repositories.user import UserRepository
from app.schemas.users import ShowUser, UserCreate, DeleteUser
from app.utils.exceptions.user_exceptions import credentials_exception
from app.utils.hashing import Hasher


class UserService:

    def __init__(self, user_repository: UserRepository) -> None:
        self._repository = user_repository

    async def create_user(self, user_data: UserCreate) -> ShowUser:
        user = await self._repository.add(name=user_data.name,
                                          surname=user_data.surname,
                                          email=user_data.email,
                                          hashed_password=Hasher.get_password_hash(user_data.password)
                                          )
        return ShowUser(
            user_id=user.user_id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            is_active=user.is_active,
        )

    async def delete_user(self, user_id: DeleteUser):
        user = await self._repository.delete(user_id=user_id)
        return user

    async def get_user_by_id(self, user_id):
        user = await self._repository.get(user_id=user_id)
        if user is not None:
            return ShowUser(
                user_id=user.user_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active,
            )

    async def authenticate_user(self, email: str, password: str) -> Union[AuthUser, None]:
        user: AuthUser = await self._get_user_by_email_for_auth(email=email)
        if user is None:
            return None
        if not Hasher.verify_password(password, user.hashed_password):
            return None
        return user

    async def _get_user_by_email_for_auth(self, email: str):
        return await self._repository.get_user_by_email(email=email)

    async def get_current_user_from_token(self, token: str):
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
            email: str = payload.get("sub")
            print("username/email extracted is ", email)
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = await self._get_user_by_email_for_auth(email=email)
        if user is None:
            raise credentials_exception
        return user
