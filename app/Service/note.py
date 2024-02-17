from app.Model.note import Note
from app.Repository.note import NoteRepository
from schema import NoteInput, NoteType

class NoteService:

    @staticmethod
    async def create_note(note_data: Note):
        note = Note(
            name=note_data.name,
            description=note_data.description
        )
        await NoteRepository.create(note)

        return NoteType(
            id=note.id,
            name=note.name,
            description=note.description
        )
    
    @staticmethod
    async def get_all_notes():
        list_notes = await NoteRepository.get_all()
        return [NoteType(
            id=note.id,
            name=note.name,
            description=note.description
        ) for note in list_notes]
    
    @staticmethod
    async def get_note_by_id(id: int):
        note = await NoteRepository.get_by_id(id)
        return NoteType(
            id=note.id,
            name=note.name,
            description=note.description
        )
    
    @staticmethod
    async def update_note(id: int, note_data: NoteInput):
        note = Note(
            name=note_data.name,
            description=note_data.description
        )
        await NoteRepository.update(id, note)
        return await NoteService.get_note_by_id(id)
    
    @staticmethod
    async def delete_note(id: int):
        await NoteRepository.delete(id)
        return f"Note deleted: {id}"