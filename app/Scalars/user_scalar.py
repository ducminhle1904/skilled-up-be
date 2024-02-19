import strawberry


@strawberry.type
class User:
    username: str
    email: str
    id: int
