from app.repositories.user import UserRepository
from app.schemas.users import ShowUser, UserCreate


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._repository = user_repository

    async def create_user(self, user_data: UserCreate) -> ShowUser:
        user = await self._repository.add(name=user_data.name, surname=user_data.surname,
                                          email=user_data.email)
        return ShowUser(
            user_id=user.user_id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            is_active=user.is_active,
        )
