"""
Repository classes for database operations using SQLAlchemy.
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .models import TemporaryChannel, GuildWarning


class WarningRepository:
    """Repository for warning-related database operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add_warning(
        self,
        user_id: str,
        guild_id: str,
        moderator_id: str,
        reason: str,
    ) -> GuildWarning:
        """Add a warning to the database."""
        warning = GuildWarning(
            user_id=user_id,
            guild_id=guild_id,
            moderator_id=moderator_id,
            reason=reason
        )
        self.session.add(warning)
        await self.session.flush()  # Ensure ID is available
        return warning
    
    async def remove_warning(
        self,
        warning_id: int,
        user_id: str,
        guild_id: str,
    ) -> bool:
        """Remove a warning from the database."""
        stmt = delete(GuildWarning).where(
            GuildWarning.id == warning_id,
            GuildWarning.user_id == user_id,
            GuildWarning.guild_id == guild_id
        )
        result = await self.session.execute(stmt)
        return result.rowcount > 0
    
    async def get_warnings(
        self,
        user_id: str,
        guild_id: str,
    ) -> List[GuildWarning]:
        """Get all warnings for a user in a guild, ordered by creation date (newest first)."""
        stmt = (
            select(GuildWarning)
            .where(GuildWarning.user_id == user_id, GuildWarning.guild_id == guild_id)
            .order_by(GuildWarning.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class TemporaryChannelRepository:
    """Repository for temporary channel-related database operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add_temporary_channel(
        self,
        channel_id: str,
        guild_id: str,
        creator_id: str,
    ) -> TemporaryChannel:
        """Add a temporary channel to the database."""
        temp_channel = TemporaryChannel(
            channel_id=channel_id,
            guild_id=guild_id,
            creator_id=creator_id
        )
        self.session.add(temp_channel)
        await self.session.flush()  # Ensure ID is available
        return temp_channel
    
    async def remove_temporary_channel(
        self,
        channel_id: str,
        guild_id: str,
    ) -> bool:
        """Mark a temporary channel as deleted."""
        stmt = (
            update(TemporaryChannel)
            .where(
                TemporaryChannel.channel_id == channel_id,
                TemporaryChannel.guild_id == guild_id,
                TemporaryChannel.is_deleted == False
            )
            .values(is_deleted=True, deleted_at=datetime.now())
        )
        result = await self.session.execute(stmt)
        return result.rowcount > 0
    
    async def get_active_temporary_channels(self) -> List[TemporaryChannel]:
        """Get all temporary channels that have not been deleted."""
        stmt = select(TemporaryChannel).where(TemporaryChannel.is_deleted == False)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def get_temporary_channel(
        self,
        channel_id: str,
        guild_id: str,
    ) -> Optional[TemporaryChannel]:
        """Get a specific temporary channel."""
        stmt = select(TemporaryChannel).where(
            TemporaryChannel.channel_id == channel_id,
            TemporaryChannel.guild_id == guild_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class DatabaseService:
    """Service class that provides access to all repositories."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.warnings = WarningRepository(session)
        self.temporary_channels = TemporaryChannelRepository(session)
    
    async def commit(self) -> None:
        """Commit the current transaction."""
        await self.session.commit()
    
    async def rollback(self) -> None:
        """Rollback the current transaction."""
        await self.session.rollback()