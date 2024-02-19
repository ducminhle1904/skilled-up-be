import strawberry

from typing import Annotated, Union
from app.Scalars.auth_scalar import LoginResult, RegisterResult
from app.Scalars.common_scalar import MutationResponse

RegisterResponse = Annotated[Union[RegisterResult, MutationResponse], strawberry.union("RegisterResponse")]

LoginResponse = Annotated[Union[MutationResponse, LoginResult], strawberry.union("LoginResponse")]