import uvicorn
from fastapi import FastAPI

from app.containers.containers import Container
from app.routers.handlers import main_api_router


def create_app() -> FastAPI:
    container = Container()
    application = FastAPI()

    application.include_router(main_api_router)
    application.container = container

    return application


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
