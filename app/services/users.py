from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import AuthUser
from app.schemas.users import ShowUser, UserCreate
from app.services.main import AppDAL, AppService


class UserService(AppService):
    async def _create_user(self, user_data: UserCreate) -> ShowUser:
        user = await UserDAL(self.db_session).create_user(name=user_data.name, surname=user_data.surname,
                                                          email=user_data.email)
        return ShowUser(
            user_id=user.user_id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            is_active=user.is_active,
        )


class UserDAL(AppDAL):

    async def create_user(self, name: str, surname: str, email: str) -> AuthUser:
        new_user = AuthUser(
            name=name,
            surname=surname,
            email=email,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        await self.db_session.commit()
        return new_user
