"""
SQLAlchemy models for the Discord bot database.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


class GuildWarning(Base):
    """Model for storing user warnings."""
    
    __tablename__ = "warns"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String, nullable=False)
    guild_id: Mapped[str] = mapped_column(String, nullable=False)
    moderator_id: Mapped[str] = mapped_column(String, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.current_timestamp())


class TemporaryChannel(Base):
    """Model for storing temporary channel information."""
    
    __tablename__ = "temporary_channels"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    channel_id: Mapped[str] = mapped_column(String, nullable=False)
    guild_id: Mapped[str] = mapped_column(String, nullable=False)
    creator_id: Mapped[str] = mapped_column(String, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.current_timestamp())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)