from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    username: str
    email: str = Field(index=True, unique=True)
    password: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
