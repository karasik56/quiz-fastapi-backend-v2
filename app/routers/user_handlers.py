import uuid
from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide
from sqlalchemy.exc import IntegrityError
from fastapi import status

from app.containers.containers import Container
from app.schemas.users import UserCreate, ShowUser, DeleteUser
from app.services.roles import RoleChecker
from app.services.users import UserService
from app.utils.auth import oauth2_scheme

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


@user_router.delete("/{user_id}",
                    status_code=status.HTTP_204_NO_CONTENT,
                    dependencies=[Depends(Provide[Container.role_check])],
                    )
@inject
async def delete_user(user_id,
                      user_service: UserService = Depends(Provide[Container.user_service]),
                      token: str = Depends(oauth2_scheme)
                      ):
    deleted_user_id = await user_service.delete_user(user_id)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return DeleteUser(user_id=deleted_user_id)


@user_router.get("/{user_id}", status_code=status.HTTP_200_OK,
                 response_model=ShowUser,
                 )
@inject
async def get_user_by_id(user_id: uuid.UUID,
                         check_role: RoleChecker = Depends(Provide[Container.role_check]),
                         user_service: UserService = Depends(Provide[Container.user_service]),
                         token: str = Depends(oauth2_scheme),
                         ):
    is_admin = await check_role(token)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Operation not permitted")

    user = await user_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return user
