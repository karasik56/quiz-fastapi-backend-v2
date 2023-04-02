from app.repositories.questions import QuestionRepository
from app.schemas.questions import CreateCategory, ShowCategory, CreateTopic, ShowTopic


class QuestionService:

    def __init__(self, question_repository: QuestionRepository) -> None:
        self._repository = question_repository

    async def create_category(self, category_data: CreateCategory) -> ShowCategory:
        category = await self._repository.add_category(name=category_data.category_name, )
        return ShowCategory(
            category_id=category.category_id,
            category_name=category.category_name,
        )

    async def create_topic(self, topic_data: CreateTopic) -> ShowTopic:
        topic = await self._repository.add_topic(name=topic_data.topic_name, category_id=topic_data.category_id)
        return ShowTopic(
            topic_id=topic.topic_id,
            topic_name=topic.topic_name,
            category=topic.category
        )
