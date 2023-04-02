import uuid

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class AuthUser(Base):
    """ Модель пользователей """
    __tablename__ = "auth_users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)


class Category(Base):
    """ Модель для категорий вопросов """
    __tablename__ = "category"

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String, nullable=False, unique=True)


class Topic(Base):
    """ Модель для тем вопросов """
    __tablename__ = "topic"

    topic_id = Column(Integer, primary_key=True)
    topic_name = Column(String, nullable=False, unique=True)
    category_id = Column(ForeignKey("category.category_id"))

    category = relationship("Category", backref="topic", innerjoin=True, lazy="joined")


