import re

from fastapi import HTTPException, Request
from passlib.context import CryptContext
from app.Fragments.auth_fragments import LoginResponse, RegisterResponse
from app.Model.user_model import User as user_model
from app.Repository.user import UserRepository
from app.Scalars.auth_scalar import LoginResult, RegisterInput, LoginInput, RegisterResult
from app.Middleware.JWTManager import JWTManager
from app.Scalars.common_scalar import MutationResponse

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

class AuthenticationService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(plain_password, hashed_password):
        return AuthenticationService.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(password):
        return AuthenticationService.pwd_context.hash(password)

    @staticmethod
    async def login(payload: LoginInput) -> LoginResponse:
        user = await UserRepository.get_by_email(payload.email)
        if not user:
            return MutationResponse(code=404, success=False, message="User not found")
        if not AuthenticationService.verify_password(payload.password, user.password):
            return MutationResponse(code=401, success=False, message="Invalid password")
        token = JWTManager.generate_token({"sub": user.email})
        return LoginResult(
            code=200,
            success=True,
            message="Login successful",
            token=token,
            user=user
        )
    
    @staticmethod
    async def register(payload: RegisterInput) -> RegisterResponse:
        user = await UserRepository.get_by_email(payload.email)
        if user:
            return MutationResponse(code=400, success=False, message="User already exists")
        
        # Validate email
        if not EMAIL_REGEX.match(payload.email):
            return MutationResponse(code=400, success=False, message="Invalid email")
        
        hashed_password = AuthenticationService.get_password_hash(payload.password)
        user = user_model(username=payload.username, email=payload.email, password=hashed_password)
        
        try:
            await UserRepository.create(user)
            return RegisterResult(code=201, success=True)
        except Exception as e:
            return MutationResponse(code=500, success=False, message="Failed to create user")
        
    @staticmethod
    async def me(request: Request) -> user_model:
        try:
            authorization = request.headers.get("Authorization")

            if not authorization or not authorization.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")

            token = authorization.split("Bearer ")[1]
            payload = JWTManager.verify_token(token)
            email = payload.get("sub")
            
            user = await UserRepository.get_by_email(email)

            return user
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid token or user not found") from e
        