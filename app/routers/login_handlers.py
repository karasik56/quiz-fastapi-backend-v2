from datetime import timedelta

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import status

from app.config import settings
from app.schemas.users import Token
from app.services.users import UserService
from app.utils.auth import oauth2_scheme
from app.utils.security import create_access_token
from app.containers.containers import Container

login_router = APIRouter()


@login_router.post("/token", response_model=Token)
@inject
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        user_service: UserService = Depends(Provide[Container.user_service])
):
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email, "other_custom_data": [1, 2, 3, 4]},
                                       expires_delta=access_token_expire)
    return {"access_token": access_token, "token_type": "bearer"}


@login_router.get("/test_auth_endpoint")
@inject
async def sample_endpoint_under_jwt(
        user_service: UserService = Depends(Provide[Container.user_service]),
        token: str = Depends(oauth2_scheme)
):
    return {"Success": True, "current_user": await user_service.get_current_user_from_token(token)}
