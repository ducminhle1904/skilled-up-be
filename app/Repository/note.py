from app.Model.note import Note
from app.Db.session import db
from sqlalchemy.sql import select
from sqlalchemy import update as update_query, delete as delete_query

class NoteRepository:

    @staticmethod
    async def create(note: Note):
        async with db as session:
            async with session.begin():
                session.add(note)
            await db.commit_rollback()

    @staticmethod
    async def get_by_id(id: int):
        async with db as session:
            result = await session.execute(select(Note).where(Note.id == id))
            return result.scalars().first()
        
    @staticmethod
    async def get_all():
        async with db as session:
            result = await session.execute(select(Note))
            return result.scalars().all()
        
    @staticmethod
    async def update(id: int, note_data: Note):
        async with db as session:
            result = await session.execute(select(Note).where(Note.id == id))
            note = result.scalars().first()
            note.name = note_data.name
            note.description = note_data.description

            query = update_query(Note).where(Note.id == id).values(**note.dict()).execution_options(synchronize_session="fetch")
            await session.execute(query)
            await db.commit_rollback()

    @staticmethod
    async def delete(id: int):
        async with db as session:
            query = delete_query(Note).where(Note.id == id)
            await session.execute(query)
            await db.commit_rollback()