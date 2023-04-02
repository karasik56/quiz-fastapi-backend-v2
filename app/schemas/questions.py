from app.schemas.base import TunedModel


class CreateCategory(TunedModel):
    category_name: str


class ShowCategory(TunedModel):
    category_id: int
    category_name: str


class CreateTopic(TunedModel):
    topic_name: str
    category_id: int


class ShowTopic(TunedModel):
    topic_id: int
    topic_name: str
    category: ShowCategory
