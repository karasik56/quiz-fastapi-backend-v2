from fastapi import APIRouter

from app.routers.login_handlers import login_router
from app.routers.question_handlers import question_router
from app.routers.user_handlers import user_router

main_api_router = APIRouter()
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(login_router, prefix="/login", tags=["login"])
main_api_router.include_router(question_router, prefix="/question", tags=["question"])
