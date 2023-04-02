from dependency_injector import containers, providers, resources

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.repositories.questions import QuestionRepository
from app.repositories.users import UserRepository
from app.services.questions import QuestionService
from app.services.roles import RoleChecker
from app.services.users import UserService


class AsyncSessionProvider(resources.AsyncResource):
    """ Контекстный менеджер для Dependency-injector """

    async def init(self, sessionmaker) -> AsyncSession:
        return sessionmaker()

    async def shutdown(self, session: AsyncSession) -> None:
        await session.close()


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(modules=[
        'app.routers.handlers',
        'app.routers.login_handlers',
        'app.routers.user_handlers',
        'app.routers.question_handlers',
    ])

    db_engine = providers.Singleton(
        create_async_engine,
        settings.REAL_DATABASE_URL,
        future=True,
        echo=True,
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )

    async_session = providers.Singleton(
        sessionmaker,
        bind=db_engine,
        expire_on_commit=False,
        class_=AsyncSession,
        autoflush=True,
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

    role_check = providers.Factory(
        RoleChecker,
        user_service=user_service,
    )

    question_repository = providers.Factory(
        QuestionRepository,
        async_session=async_session
    )

    question_service = providers.Factory(
        QuestionService,
        question_repository=question_repository
    )
