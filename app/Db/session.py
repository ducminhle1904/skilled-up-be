from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from app.Core.config import settings


class DatabaseSession:
    def __init__(self, url: str = settings.DB_CONFIG):
        self.engine = create_async_engine(url, echo=True)
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    # Generating models into database
    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def drop_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)

    # Close connection
    async def close(self):
        await self.engine.dispose()

    # Prepare the context for the asynchronous operation
    async def __aenter__(self) -> AsyncSession:
        self.session = self.SessionLocal()
        return self.session

    # This for clean up resources
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def commit_rollback(self):
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise


db = DatabaseSession()
