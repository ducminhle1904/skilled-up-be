import strawberry

from typing import List
from app.Middleware.JWTBearer import IsAuthenticated
from app.Scalars.user_scalar import User
from app.Service.authentication import AuthenticationService

@strawberry.type
class Query:
    
    @strawberry.field
    async def get_current_user(self, info) -> User:
        return await AuthenticationService.me(info.context["request"])