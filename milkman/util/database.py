"""
This module contains the Database class, which is used to manage the database.
"""

import aiosqlite
import os

from dataclasses import dataclass
from datetime import datetime


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
        """
        database_schema_path = os.path.join(
            os.path.realpath(os.path.dirname(__file__)), "schema.sql"
        )
        with open(database_schema_path, "r", encoding="utf-8") as f:
            await self.connection.executescript(f.read())
        await self.connection.commit()

    async def close(self) -> None:
        """
        Close the connection to the database.
        """
        await self.connection.close()

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
        """
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
        """
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
        """
        async with self.connection.execute(
            "SELECT * FROM warns WHERE user_id = ? AND guild_id = ? ORDER BY created_at DESC",
            (user_id, guild_id),
        ) as cursor:
            rows = await cursor.fetchall()
            return [
                Warning(
                    id=row["id"],
                    user_id=row["user_id"],
                    guild_id=row["guild_id"],
                    moderator_id=row["moderator_id"],
                    reason=row["reason"],
                    created_at=row["created_at"],
                )
                for row in rows
            ]
