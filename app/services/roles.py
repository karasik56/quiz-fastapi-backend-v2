from fastapi import Depends, HTTPException

from app.models.models import AuthUser
from app.utils.auth import oauth2_scheme


class RoleChecker:
    def __init__(self, user_service):
        self.user_service = user_service

    async def __call__(self,
                       token=Depends(oauth2_scheme),
                       ):
        current_user: AuthUser = await self.user_service.get_current_user_from_token(token)
        if current_user.is_admin is not True:
            return False
        return True
