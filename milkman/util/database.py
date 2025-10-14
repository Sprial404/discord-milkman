"""
SQLAlchemy-based database management for the Discord bot.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .models import Base


class DatabaseConfig:
    """Configuration class for database settings."""
    
    def __init__(self, database_path: str):
        self.database_url = f"sqlite+aiosqlite:///{database_path}"
        self.engine = create_async_engine(self.database_url, echo=False)
        self.async_session = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
    
    async def create_tables(self) -> None:
        """Create all tables defined in the models."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get an async database session."""
        async with self.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    async def close(self) -> None:
        """Close the database engine."""
        await self.engine.dispose()