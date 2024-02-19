import strawberry
from typing import Optional


@strawberry.type
class MutationResponse:
    code: int
    success: bool
    message: str