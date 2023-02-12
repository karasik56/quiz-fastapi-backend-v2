from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.exc import IntegrityError

from app.config.session import get_db
from app.schemas.users import UserCreate, ShowUser
from app.services.users import UserService

logger = getLogger(__name__)

user_router = APIRouter()


@user_router.post("/", response_model=ShowUser)
async def create_user(user_data: UserCreate, db: get_db = Depends()) -> ShowUser:
    try:
        return await UserService(db)._create_user(user_data)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
