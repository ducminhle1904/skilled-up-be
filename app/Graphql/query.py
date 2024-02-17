import strawberry

from typing import List
from app.Middleware.JWTBearer import IsAuthenticated
from app.Service.authentication import AuthenticationService
from app.Service.note import NoteService
from schema import NoteType, User

@strawberry.type
class Query:

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def get_all(self) -> List[NoteType]:
        return await NoteService.get_all_notes()
    
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def get_by_id(self, id: int) -> NoteType:
        return await NoteService.get_note_by_id(id)
    
    @strawberry.field
    async def get_current_user(self, info) -> User:
        return await AuthenticationService.me(info.context["request"])