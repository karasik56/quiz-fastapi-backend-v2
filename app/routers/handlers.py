from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException, Response
from dependency_injector.wiring import inject, Provide
from sqlalchemy.exc import IntegrityError
from starlette import status

from app.containers.containers import Container
from app.schemas.users import UserCreate, ShowUser, DeleteUser
from app.services.users import UserService

logger = getLogger(__name__)

user_router = APIRouter()


@user_router.post("/", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
@inject
async def create_user(
        user_data: UserCreate,
        user_service: UserService = Depends(Provide[Container.user_service])) -> ShowUser:
    try:
        return await user_service.create_user(user_data)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_user(user_id, user_service: UserService = Depends(Provide[Container.user_service])):
    deleted_user_id = await user_service.delete_user(user_id)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return DeleteUser(user_id=deleted_user_id)


@user_router.get("/{user_id}", status_code=status.HTTP_200_OK)
@inject
async def get_user_by_id(user_id, user_service: UserService = Depends(Provide[Container.user_service])):
    return await user_service.get_user_by_id(user_id)
