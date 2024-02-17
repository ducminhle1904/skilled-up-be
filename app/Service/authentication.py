import re

from fastapi import HTTPException, Request
from passlib.context import CryptContext
from app.Model.user import User
from app.Repository.user import UserRepository
from schema import LoginResult, RegisterInput, LoginInput
from app.Middleware.JWTManager import JWTManager

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

class AuthenticationService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(plain_password, hashed_password):
        return AuthenticationService.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(password):
        return AuthenticationService.pwd_context.hash(password)

    @staticmethod
    async def login(payload: LoginInput) -> LoginResult:
        user = await UserRepository.get_by_email(payload.email)
        if not user:
            return LoginResult(success=False, message="User not found", token=None, user=None)
        if not AuthenticationService.verify_password(payload.password, user.password):
            return LoginResult(success=False, message="Invalid password", token=None, user=None)
        token = JWTManager.generate_token({"sub": user.email})
        return LoginResult(
            success=True,
            message="Login successful",
            token=token,
            user=user
        )
    
    @staticmethod
    async def register(payload: RegisterInput) -> str:
        user = await UserRepository.get_by_email(payload.email)
        if user:
            raise ValueError("User already exists")
        
        # Validate email
        if not EMAIL_REGEX.match(payload.email):
            raise ValueError("Invalid email")
        
        hashed_password = AuthenticationService.get_password_hash(payload.password)
        user = User(username=payload.username, email=payload.email, password=hashed_password)
        
        try:
            await UserRepository.create(user)
            return f"User {payload.username} created successfully!"
        except Exception as e:
            return f"Failed to create user: {str(e)}"
        
    @staticmethod
    async def me(request: Request) -> User:
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
        