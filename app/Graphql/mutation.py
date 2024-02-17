import strawberry
from app.Model.user import User
from app.Service.authentication import AuthenticationService

from app.Service.note import NoteService
from schema import LoginInput, LoginResult, NoteInput, NoteType, RegisterInput

from app.Middleware.JWTBearer import IsAuthenticated

@strawberry.type
class Mutation:

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def create_note(self, note_data: NoteInput) -> NoteType:
        return await NoteService.create_note(note_data)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def delete_note(self, note_id: int) -> str:
        return await NoteService.delete_note(note_id)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def update_note(self, note_id: int, note_data: NoteInput) -> NoteType:
        return await NoteService.update_note(note_id,note_data)
    
    @strawberry.mutation
    async def register(self, register_data: RegisterInput) -> str:
        return await AuthenticationService.register(register_data)
    
    @strawberry.mutation
    async def login(self, login_data: LoginInput) -> LoginResult:
        return await AuthenticationService.login(login_data)