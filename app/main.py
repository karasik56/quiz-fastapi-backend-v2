import uvicorn
from fastapi import FastAPI, APIRouter

from app.containers.containers import Container
from app.routers.handlers import user_router
from app.routers.login_handlers import login_router


def create_app() -> FastAPI:
    container = Container()
    application = FastAPI()

    main_api_router = APIRouter()
    main_api_router.include_router(user_router, prefix="/user", tags=["user"])
    main_api_router.include_router(login_router, prefix="/login", tags=["login"])
    application.include_router(main_api_router)

    application.container = container

    return application


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
