from dependency_injector import containers, providers, resources
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.repositories.user import UserRepository
from app.services.users import UserService


class AsyncSessionProvider(resources.AsyncResource):
    async def init(self, sessionmaker) -> AsyncSession:
        return sessionmaker()

    async def shutdown(self, session: AsyncSession) -> None:
        await session.close()


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    db_engine = providers.Singleton(
        create_async_engine,
        settings.REAL_DATABASE_URL,
        future=True,
        echo=True,
    )

    async_session = providers.Singleton(
        sessionmaker,
        bind=db_engine,
        expire_on_commit=False,
        class_=AsyncSession
    )

    async_session = providers.Resource(AsyncSessionProvider, async_session)

    user_repository = providers.Factory(
        UserRepository,
        async_session=async_session
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository
    )
