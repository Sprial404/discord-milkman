"""
This cog is used to manage the bot and adds a bunch of commands that are only available to the owner of the bot.

Commands:
    - sync: Syncronises the slash commands.
    - unsync: Unsyncronises the slash commands.
    - load: Loads a cog.
    - unload: Unloads a cog.
    - reload: Reloads a cog.
    - shutdown: Shuts down the bot.
    - say: Says something.
    - embed: Sends an embed.
    - listcogs: Lists all cogs.
"""

from typing import Literal
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import logging

from milkman.constants import SUCCESS_COLOR, ERROR_COLOR, OWNER_COG_NAME

logger = logging.getLogger(__name__)


class Owner(commands.Cog, name=OWNER_COG_NAME):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="sync", description="Syncronises the slash commands.")
    @app_commands.describe(
        scope="The scope of the syncronisation, which can be global or guild.",
    )
    @commands.is_owner()
    async def sync(self, ctx: Context, scope: Literal["global", "guild"]) -> None:
        """
        Syncronises the slash commands.

        Args:
            ctx (Context): The context of the command.
            scope (str): The scope of the syncronisation.
        """

        if scope == "global":
            await self.bot.tree.sync()
            embed = discord.Embed(
                description="Syncronised the slash commands globally.",
                color=SUCCESS_COLOR,
            )
            await ctx.send(embed=embed)
        elif scope == "guild":
            self.bot.tree.copy_global_to(guild=ctx.guild)
            await self.bot.tree.sync(guild=ctx.guild)
            embed = discord.Embed(
                description="Syncronised the slash commands for this guild.",
                color=SUCCESS_COLOR,
            )
            await ctx.send(embed=embed)

    @commands.command(name="unsync", description="Unsyncronises the slash commands.")
    @app_commands.describe(
        scope="The scope of the unsyncronisation, which can be global or guild.",
    )
    @commands.is_owner()
    async def unsync(self, ctx: Context, scope: str) -> None:
        """
        Unsyncronises the slash commands.

        Args:
            ctx (Context): The context of the command.
            scope (str): The scope of the unsyncronisation.
        """

        if scope == "global":
            self.bot.tree.clear_commands(guild=None)
            await self.bot.tree.sync()
            embed = discord.Embed(
                description="Unsyncronised the slash commands globally.",
                color=SUCCESS_COLOR,
            )
            await ctx.send(embed=embed)
        elif scope == "guild":
            self.bot.tree.clear_commands(guild=ctx.guild)
            await self.bot.tree.sync(guild=ctx.guild)
            embed = discord.Embed(
                description="Unsyncronised the slash commands for this guild.",
                color=SUCCESS_COLOR,
            )
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="load", description="Loads a cog.")
    @app_commands.describe(cog="The name of the cog to load.")
    @commands.is_owner()
    async def load(self, ctx: Context, cog: str) -> None:
        """
        Loads a cog.

        Args:
            ctx (Context): The context of the command.
            cog (str): The name of the cog to load.
        """

        try:
            await self.bot.load_extension(f"cogs.{cog}")
        except Exception as e:
            embed = discord.Embed(
                description=f"Failed to load the cog `{cog}`",
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            description=f"Successfully loaded the cog `{cog}`",
            color=SUCCESS_COLOR,
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="unload", description="Unloads a cog.")
    @app_commands.describe(cog="The name of the cog to unload.")
    @commands.is_owner()
    async def unload(self, ctx: Context, cog: str) -> None:
        """
        Unloads a cog.

        Args:
            ctx (Context): The context of the command.
            cog (str): The name of the cog to unload.
        """

        try:
            await self.bot.unload_extension(f"cogs.{cog}")
        except Exception as e:
            embed = discord.Embed(
                description=f"Failed to unload the cog `{cog}`",
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            description=f"Successfully unloaded the cog `{cog}`",
            color=SUCCESS_COLOR,
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="reload", description="Reloads a cog.")
    @app_commands.describe(cog="The name of the cog to reload.")
    @commands.is_owner()
    async def reload(self, ctx: Context, cog: str) -> None:
        """
        Reloads a cog.

        Args:
            ctx (Context): The context of the command.
            cog (str): The name of the cog to reload.
        """

        try:
            await self.bot.reload_extension(f"cogs.{cog}")
        except Exception as e:
            embed = discord.Embed(
                description=f"Could not reload the cog `{cog}`",
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            description=f"Successfully reloaded the cog `{cog}`",
            color=SUCCESS_COLOR,
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="shutdown", description="Shuts down the bot.")
    @commands.is_owner()
    async def shutdown(self, ctx: Context) -> None:
        """
        Shuts down the bot.

        Args:
            ctx (Context): The context of the command.
        """

        embed = discord.Embed(
            description="Shutting down :wave:",
            color=SUCCESS_COLOR,
        )
        await ctx.send(embed=embed)
        await self.bot.close()

    @commands.hybrid_command(name="say", description="Says something.")
    @app_commands.describe(message="The message to say that the bot will repeat")
    @commands.is_owner()
    async def say(self, ctx: Context, message: str) -> None:
        """
        Says something.

        Args:
            ctx (Context): The context of the command.
            message (str): The message to say that the bot will repeat.
        """

        await ctx.send(message)

    @commands.hybrid_command(name="embed", description="Sends an embed.")
    @app_commands.describe(
        title="The title of the embed.",
        description="The description of the embed.",
        color="The color of the embed.",
    )
    @commands.is_owner()
    async def embed(
        self, ctx: Context, title: str, description: str, color: str
    ) -> None:
        """
        Sends an embed.
        """

        await ctx.send(
            embed=discord.Embed(title=title, description=description, color=color)
        )

    @commands.hybrid_command(name="listcogs", description="Lists all cogs.")
    @commands.is_owner()
    async def listcogs(self, ctx: Context) -> None:
        """
        Lists all cogs.
        """

        cogs = [f"`{cog}`" for cog in self.bot.cogs]
        embed = discord.Embed(
            description="\n".join(cogs),
            color=SUCCESS_COLOR,
        )
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """
    Setup the Owner cog.

    Args:
        bot (commands.Bot): The bot instance.
    """
    await bot.add_cog(Owner(bot))
