import strawberry

from typing import Optional

@strawberry.type
class User:
    username: str
    email: str
    id: int

@strawberry.type
class NoteType:
    id: int
    name: str
    description: str

@strawberry.input
class NoteInput:
    name: str
    description: str

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
class LoginResult:
    success: bool
    message: str
    token: Optional[str]
    user: Optional[User]