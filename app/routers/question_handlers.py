from logging import getLogger

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi import status

from sqlalchemy.exc import IntegrityError

from app.schemas.questions import ShowCategory, CreateCategory, ShowTopic, CreateTopic
from app.services.questions import QuestionService
from app.containers.containers import Container
from app.utils.auth import oauth2_scheme

logger = getLogger(__name__)

question_router = APIRouter()


@question_router.post("/category", response_model=ShowCategory,
                      status_code=status.HTTP_201_CREATED,
                      )
@inject
async def create_category(
        category_data: CreateCategory,
        question_service: QuestionService = Depends(Provide[Container.question_service]),
        token: str = Depends(oauth2_scheme)
) -> ShowCategory:
    try:
        return await question_service.create_category(category_data)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@question_router.post("/topic", response_model=ShowTopic,
                      status_code=status.HTTP_201_CREATED,
                      )
@inject
async def create_topic(
        topic_data: CreateTopic,
        question_service: QuestionService = Depends(Provide[Container.question_service]),
        token: str = Depends(oauth2_scheme)
        ):
    try:
        return await question_service.create_topic(topic_data)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
