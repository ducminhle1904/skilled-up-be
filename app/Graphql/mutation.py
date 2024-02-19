import strawberry
from app.Fragments.auth_fragments import LoginResponse, RegisterResponse
from app.Scalars.auth_scalar import RegisterInput, LoginInput, LoginResult
from app.Service.authentication import AuthenticationService

from app.Middleware.JWTBearer import IsAuthenticated

@strawberry.type
class Mutation:
    
    @strawberry.mutation
    async def register(self, register_data: RegisterInput) -> RegisterResponse:
        return await AuthenticationService.register(register_data)
    
    @strawberry.mutation
    async def login(self, login_data: LoginInput) -> LoginResponse:
        return await AuthenticationService.login(login_data)