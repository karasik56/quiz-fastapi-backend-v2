from dependency_injector.wiring import Provide
from fastapi import Depends, HTTPException

from app.models.models import AuthUser
from app.services.users import UserService
from app.utils.auth import oauth2_scheme
from app.containers.containers import Container


class RoleChecker:
    def __init__(self, only_admin: bool):
        self._admin = only_admin

    async def __call__(self,
                       token=Depends(oauth2_scheme),
                       user_service: UserService = Depends(Provide[Container.user_service])
                       ):
        current_user: AuthUser = await user_service.get_current_user_from_token(token)
        if current_user.is_admin is not True:
            raise HTTPException(status_code=403, detail="Operation not permitted")
