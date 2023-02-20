from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide
from sqlalchemy.exc import IntegrityError
from starlette import status

from app.containers.containers import Container
from app.schemas.users import UserCreate, ShowUser
from app.services.users import UserService

logger = getLogger(__name__)

user_router = APIRouter()


@user_router.post("/", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
@inject
async def create_user(
        user_data: UserCreate,
        user_service: UserService = Depends(Provide[Container.user_service])
) -> ShowUser:
    try:
        return await user_service.create_user(user_data)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
