from app.Model.user_model import User as user_model
from app.Db.session import db
from sqlalchemy.sql import select
from sqlalchemy import update as update_query, delete as delete_query


class UserRepository:

    @staticmethod
    async def create(user: user_model):
        async with db as session:
            async with session.begin():
                session.add(user)
            await db.commit_rollback()

    @staticmethod
    async def get_by_id(id: int):
        async with db as session:
            result = await session.execute(select(user_model).where(user_model.id == id))
            return result.scalars().first()

    @staticmethod
    async def get_all():
        async with db as session:
            result = await session.execute(select(user_model))
            return result.scalars().all()

    @staticmethod
    async def update(id: int, user_data: user_model):
        async with db as session:
            result = await session.execute(select(user_model).where(user_model.id == id))
            user = result.scalars().first()
            user.name = user_data.name
            user.password = user_data.password
            user.email = user_data.email

            query = update_query(user_model).where(user_model.id == id).values(**user.dict()).execution_options(
                synchronize_session="fetch")
            await session.execute(query)
            await db.commit_rollback()

    @staticmethod
    async def delete(id: int):
        async with db as session:
            query = delete_query(user_model).where(user_model.id == id)
            await session.execute(query)
            await db.commit_rollback()

    @staticmethod
    async def get_by_email(email: str):
        async with db as session:
            result = await session.execute(select(user_model).where(user_model.email == email))
            return result.scalars().first()
