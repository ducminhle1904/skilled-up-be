from typing import Optional
import strawberry
from app.Scalars.common_scalar import MutationResponse

from app.Scalars.user_scalar import User


@strawberry.input
class RegisterInput:
    username: str
    email: str
    password: str

@strawberry.input
class LoginInput:
    email: str
    password: str

@strawberry.type
class LoginResult(MutationResponse):
    token: Optional[str]
    user: Optional[User]

@strawberry.type
class RegisterResult(MutationResponse):
    message: str = "User created successfully!"
