"""
This module contains the Database class, which is used to manage the database.
"""

import aiosqlite
import os

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Warning:
    """
    A class for storing warnings.
    """

    id: int
    user_id: str
    guild_id: str
    moderator_id: str
    reason: str
    created_at: datetime

@dataclass
class TemporaryChannel:
    """
    A class for storing temporary channel information.
    """

    id: int
    channel_id: str
    guild_id: str
    creator_id: str
    is_deleted: bool
    created_at: datetime
    deleted_at: Optional[datetime]


class Database:
    """
    A class for managing the database. Handles creating tables and closing the connection and retrieving and accessing data.
    """

    def __init__(self, connection_path: str) -> None:
        """
        Initialize the database.

        Args:
            connection_path (str): The path to the database file.
        """
        self.connection_path = connection_path
        self.connection = None

    async def connect(self) -> None:
        """
        Connect to the database.
        """
        self.connection = await aiosqlite.connect(self.connection_path)

    async def create_tables(self) -> None:
        """
        Create the tables in the database from the schema.sql file.
        Raises:
            RuntimeError: If the database connection is not established.
        """
        if self.connection is None:
            raise RuntimeError("Database connection is not established. Call connect() first.")

        database_schema_path = os.path.join(
            os.path.realpath(os.path.dirname(__file__)), "schema.sql"
        )
        with open(database_schema_path, "r", encoding="utf-8") as f:
            await self.connection.executescript(f.read())
        await self.connection.commit()

    async def close(self) -> None:
        """
        Close the connection to the database.
        Raises:
            RuntimeError: If the database connection is not established.
        """
        if self.connection is None:
            raise RuntimeError("Database connection is not established. Call connect() first.")

        await self.connection.close()

    async def add_temporary_channel(
        self,
        channel_id: str,
        guild_id: str,
        user_id: str,
    ) -> TemporaryChannel:
        """
        Add a temporary channel to the database.

        Args:
            channel_id (str): The id of the temporary channel.
            guild_id (str): The id of the guild the channel belongs to.
            user_id (str): The id of the user who created the channel.

        Returns:
            TemporaryChannel: An instance of TemporaryChannel containing the details of the added channel.

        Raises:
            RuntimeError: If the database connection is not established or if the insert operation fails.
        """
        if self.connection is None:
            raise RuntimeError("Database connection is not established. Call connect() first.")

        cursor = await self.connection.execute(
            "INSERT INTO temporary_channels (channel_id, guild_id, creator_id) VALUES (?, ?, ?)",
            (channel_id, guild_id, user_id),
        )
        await self.connection.commit()

        if cursor.lastrowid is None:
            raise RuntimeError("Failed to insert temporary channel into the database.")
        
        temporary_channel = TemporaryChannel(
            id=cursor.lastrowid,
            channel_id=channel_id,
            guild_id=guild_id,
            creator_id=user_id,
            is_deleted=False,
            created_at=datetime.now(),
            deleted_at=None
        )
        return temporary_channel

    async def remove_temporary_channel(
        self,
        channel_id: str,
        guild_id: str,
    ) -> None:
        """
        Remove a temporary channel from the database.
        Args:
            channel_id (str): The id of the temporary channel to remove.
            guild_id (str): The id of the guild the channel belongs to.

        Raises:
            RuntimeError: If the database connection is not established or if the update operation fails.
        """
    
        if self.connection is None:
            raise RuntimeError("Database connection is not established. Call connect() first.")

        await self.connection.execute(
            "UPDATE temporary_channels SET is_deleted = 1, deleted_at = ? WHERE channel_id = ? AND guild_id = ?",
            (datetime.now().isoformat(), channel_id, guild_id),
        )
        await self.connection.commit()

    async def get_active_temporary_channels(self) -> list[TemporaryChannel]:
        """
        Get all temporary channels that have not been deleted.

        Returns:
            list[TemporaryChannel]: A list of temporary channels.

        Raises:
            RuntimeError: If the database connection is not established.
        """
        if self.connection is None:
            raise RuntimeError("Database connection is not established. Call connect() first.")

        async with self.connection.execute(
            "SELECT * FROM temporary_channels WHERE is_deleted = 0",
        ) as cursor:
            rows = await cursor.fetchall()
            return [
                TemporaryChannel(
                    id=row[0],
                    channel_id=row[1],
                    guild_id=row[2],
                    creator_id=row[3],
                    is_deleted=bool(row[4]),
                    created_at=datetime.fromisoformat(row[5]),
                    deleted_at=datetime.fromisoformat(row[6]) if row[6] else None,
                )
                for row in rows
            ]

    async def add_warning(
        self,
        user_id: str,
        guild_id: str,
        moderator_id: str,
        reason: str,
    ) -> None:
        """
        Add a warning to the database.

        Args:
            user_id (str): The id of the user to warn.
            guild_id (str): The id of the guild to warn the user in.
            moderator_id (str): The id of the moderator who warned the user.
            reason (str): The reason for the warning.

        Raises:
            RuntimeError: If the database connection is not established or if the insert operation fails.
        """
        if self.connection is None:
            raise RuntimeError("Database connection is not established. Call connect() first.")

        await self.connection.execute(
            "INSERT INTO warns (user_id, guild_id, moderator_id, reason) VALUES (?, ?, ?, ?)",
            (user_id, guild_id, moderator_id, reason),
        )
        await self.connection.commit()

    async def remove_warning(
        self,
        id: int,
        user_id: str,
        guild_id: str,
    ) -> None:
        """
        Remove a warning from the database.

        Args:
            id (int): The id of the warning to remove.
            user_id (str): The id of the user to remove the warning for.
            guild_id (str): The id of the guild to remove the warning for.

        Raises:
            RuntimeError: If the database connection is not established or if the delete operation fails.
        """
        if self.connection is None:
            raise RuntimeError("Database connection is not established. Call connect() first.")

        await self.connection.execute(
            "DELETE FROM warns WHERE id = ? AND user_id = ? AND guild_id = ?",
            (id, user_id, guild_id),
        )

    async def get_warnings(
        self,
        user_id: str,
        guild_id: str,
    ) -> list[Warning]:
        """
        Get all warnings for a user in a guild in descending order of creation.

        Args:
            user_id (str): The id of the user to get warnings for.
            guild_id (str): The id of the guild to get warnings for.

        Returns:
            list[Warning]: A list of warnings.

        Raises:
            RuntimeError: If the database connection is not established.
        """
        if self.connection is None:
            raise RuntimeError("Database connection is not established. Call connect() first.")

        async with self.connection.execute(
            "SELECT * FROM warns WHERE user_id = ? AND guild_id = ? ORDER BY created_at DESC",
            (user_id, guild_id),
        ) as cursor:
            rows = await cursor.fetchall()
            return [
                Warning(
                    id=row[0],
                    user_id=row[1],
                    guild_id=row[2],
                    moderator_id=row[3],
                    reason=row[4],
                    created_at=datetime.fromisoformat(row[5]),
                )
                for row in rows
            ]
