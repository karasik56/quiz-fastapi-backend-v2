from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import AuthUser


class UserRepository:

    def __init__(self, async_session: AsyncSession) -> None:
        self.async_session = async_session

    async def add(self, name: str, surname: str, email: str) -> AuthUser:
        async with self.async_session as session:
            new_user = AuthUser(
                name=name,
                surname=surname,
                email=email,
            )
            session.add(new_user)
            await session.commit()
            return new_user
