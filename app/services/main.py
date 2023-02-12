from sqlalchemy.ext.asyncio import AsyncSession


class DBSessionMixin:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session


class AppService(DBSessionMixin):
    pass


class AppDAL(DBSessionMixin):
    pass
