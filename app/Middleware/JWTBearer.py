import typing

from strawberry.permission import BasePermission
from strawberry.types import Info
from app.Middleware.JWTManager import JWTManager


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    def has_permission(self, source: typing.Any, info: Info, **kwargs: typing.Any) -> bool | typing.Awaitable[bool]:
        request = info.context["request"]
        # Access headers authentication
        authorization = request.headers.get("Authorization")
        if authorization:
            token = authorization.split("Bearer ")[1]
            return JWTManager.verify_token(token)
        return False
