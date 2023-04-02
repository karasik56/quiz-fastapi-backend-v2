from sqlalchemy import delete, select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import AuthUser


class UserRepository:

    def __init__(self, async_session: AsyncSession) -> None:
        self.async_session = async_session

    async def add(self, name: str, surname: str, email: str, hashed_password: str) -> AuthUser:
        new_user = AuthUser(
            name=name,
            surname=surname,
            email=email,
            hashed_password=hashed_password,
        )
        self.async_session.add(new_user)
        await self.async_session.flush()
        return new_user

    async def delete(self, user_id):
        query = update(AuthUser).where(and_(AuthUser.user_id == user_id, AuthUser.is_active == True)).values(
            is_active=False).returning(AuthUser.user_id)
        res = await self.async_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]

    async def get(self, user_id):
        query = select(AuthUser).where(AuthUser.user_id == user_id)
        res = await self.async_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_user_by_email(self, email):
        query = select(AuthUser).where(AuthUser.email == email)
        res = await self.async_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]
