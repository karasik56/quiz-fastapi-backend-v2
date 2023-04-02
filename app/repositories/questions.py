from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Category, Topic
from app.schemas.questions import ShowCategory


class QuestionRepository:
    """ Репозиторий для взаимодействия бизнес логики вопросов для квиза с базой данных """
    def __init__(self, async_session: AsyncSession) -> None:
        self.async_session = async_session

    async def add_category(self, name: str) -> Category:
        category = Category(
            category_name=name
        )
        self.async_session.add(category)
        await self.async_session.flush()
        return category

    async def add_topic(self, name: str, category_id: int) -> Topic:
        topic = Topic(
            topic_name=name,
            category_id=category_id
        )
        self.async_session.add(topic)
        await self.async_session.flush()
        await self.async_session.refresh(topic)
        return topic
