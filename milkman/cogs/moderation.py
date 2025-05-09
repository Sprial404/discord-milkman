"""
This cog contains moderation commands.

Commands:
    - kick: Kick a user from the server.
    - ban: Ban a user from the server.
    - warn: Warn a user.
    - remove_warning: Remove a warning from a user.
    - list_warnings: List all warnings for a user.
    - purge: Purge messages from the server.
"""

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from milkman.constants import SUCCESS_COLOR, ERROR_COLOR, MODERATION_COG_NAME

import logging

logger = logging.getLogger(__name__)


class Moderation(commands.Cog, name=MODERATION_COG_NAME):
    """
    This cog contains moderation commands.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="kick", description="Kick a user from the server.")
    @app_commands.describe(
        user="The user to kick.",
        reason="The reason for the kick.",
    )
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(
        self, ctx: Context, user: discord.User, reason: str = "No reason provided."
    ) -> None:
        """
        Kick a user from the server.

        Args:
            ctx (Context): The context of the command.
            user (discord.User): The user that is being kicked from the server.
            reason (str): The reason for the kick, defaulting to "No reason provided."
        """

        member = ctx.guild.get_member(user.id) or await ctx.guild.fetch_member(user.id)
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                description="You cannot kick an administrator.",
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)
            return
        else:
            try:
                embed = discord.Embed(
                    description=f"Kicked **{member}** from the server by **{ctx.author}**.",
                    color=SUCCESS_COLOR,
                )
                embed.set_footer(text=f"Reason: {reason}")
                await ctx.send(embed=embed)

                try:
                    await member.send(
                        f"You were kicked from **{ctx.guild}** by **{ctx.author}**!\n\nReason: {reason}"
                    )
                except Exception:
                    # If the user has DMs disabled, we can't send them a message.
                    pass

                await member.kick(reason=reason)
            except Exception as e:
                embed = discord.Embed(
                    description=f"Failed to kick {member.mention} from the server. Please ensure my role is higher than the user's role.",
                    color=ERROR_COLOR,
                )
                await ctx.send(embed=embed)

                logger.error(
                    f"Failed to kick {member.mention} from the server. Please ensure my role is higher than the user's role. Error: {e}"
                )

    @commands.hybrid_command(name="ban", description="Ban a user from the server.")
    @app_commands.describe(
        user="The user to ban.",
        reason="The reason for the ban.",
    )
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(
        self, ctx: Context, user: discord.User, reason: str = "No reason provided."
    ) -> None:
        """
        Ban a user from the server.

        Args:
            ctx (Context): The context of the command.
            user (discord.User): The user that is being banned from the server.
            reason (str): The reason for the ban, defaulting to "No reason provided."
        """

        member = ctx.guild.get_member(user.id) or await ctx.guild.fetch_member(user.id)
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                description="You cannot ban an administrator.",
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)
            return
        else:
            try:
                embed = discord.Embed(
                    description=f"Banned **{member}** from the server by **{ctx.author}**.",
                    color=SUCCESS_COLOR,
                )
                embed.set_footer(text=f"Reason: {reason}")
                await ctx.send(embed=embed)

                try:
                    await member.send(
                        f"You were banned from **{ctx.guild}** by **{ctx.author}**!\n\nReason: {reason}"
                    )
                except Exception:
                    # If the user has DMs disabled, we can't send them a message.
                    pass

                await member.ban(reason=reason)
            except Exception as e:
                embed = discord.Embed(
                    description=f"Failed to ban {member.mention} from the server. Please ensure my role is higher than the user's role.",
                    color=ERROR_COLOR,
                )
                await ctx.send(embed=embed)

                logger.error(
                    f"Failed to ban {member.mention} from the server. Please ensure my role is higher than the user's role. Error: {e}"
                )

    @commands.hybrid_command(name="warn", description="Warn a user.")
    @app_commands.describe(
        user="The user to warn.",
        reason="The reason for the warn.",
    )
    @commands.has_permissions(manage_messages=True)
    async def warn(
        self, ctx: Context, user: discord.User, reason: str = "No reason provided."
    ) -> None:
        """
        Warn a user.

        Args:
            ctx (Context): The context of the command.
            user (discord.User): The user that is being warned.
            reason (str): The reason for the warn, defaulting to "No reason provided."
        """

        member = ctx.guild.get_member(user.id) or await ctx.guild.fetch_member(user.id)
        await self.bot.db.add_warning(
            user.id,
            ctx.guild.id,
            ctx.author.id,
            reason,
        )
        embed = discord.Embed(
            description=f"Warned **{member}** from the server by **{ctx.author}**.",
            color=SUCCESS_COLOR,
        )
        embed.set_footer(text=f"Reason: {reason}")
        await ctx.send(embed=embed)
        try:
            await member.send(
                f"You were warned from **{ctx.guild}** by **{ctx.author}**!\n\nReason: {reason}"
            )
        except Exception:
            # If the user has DMs disabled, we can't send them a message.
            await ctx.send(
                f"{member.mention}, you were warned by **{ctx.author}**!\n\nReason: {reason}"
            )

    @commands.hybrid_command(
        name="remove_warning", description="Remove a warning from a user."
    )
    @app_commands.describe(
        user="The user to remove a warning from.",
        id="The id of the warning to remove.",
    )
    @commands.has_permissions(manage_messages=True)
    async def remove_warning(self, ctx: Context, user: discord.User, id: int) -> None:
        """
        Remove a warning from a user.

        Args:
            ctx (Context): The context of the command.
            user (discord.User): The user to remove a warning from.
            id (int): The id of the warning to remove.
        """
        member = ctx.guild.get_member(user.id) or await ctx.guild.fetch_member(user.id)
        await self.bot.db.remove_warning(id, user.id, ctx.guild.id)
        embed = discord.Embed(
            description=f"Removed warning **{id}** from **{member}**.",
            color=SUCCESS_COLOR,
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="list_warnings", description="List all warnings for a user."
    )
    @app_commands.describe(
        user="The user to list warnings for.",
    )
    @commands.has_permissions(manage_messages=True)
    async def list_warnings(self, ctx: Context, user: discord.User) -> None:
        """
        List all warnings for a user.

        Args:
            ctx (Context): The context of the command.
            user (discord.User): The user to list warnings for.
        """
        warnings = await self.bot.db.get_warnings(user.id, ctx.guild.id)
        if not warnings:
            embed = discord.Embed(
                description="No warnings found for this user.",
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)
        else:
            lines = []
            for warning in warnings:
                lines.append(
                    f"• Warned by <@{warning.moderator_id}>: {warning.reason} (<t:{int(warning.created_at.timestamp())}>) - Warning ID: {warning.id}"
                )
            description = "\n".join(lines)
            embed = discord.Embed(
                title=f"Warnings for {user}",
                description=description,
                color=SUCCESS_COLOR,
            )
            await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="purge", description="Purge messages from the server."
    )
    @app_commands.describe(
        amount="The amount of messages to purge.",
        user="The user to purge messages from.",
    )
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx: Context, amount: int, user: discord.User = None) -> None:
        """
        Purge messages from the server.

        Args:
            ctx (Context): The context of the command.
            amount (int): The amount of messages to purge.
            user (discord.User): The user to purge messages from, defaulting to None.
        """

        await ctx.send("Deleting messages...")

        purged_messages = await ctx.channel.purge(limit=amount + 1)
        embed = discord.Embed(
            description=f"**{ctx.author}** purged {len(purged_messages) - 1} messages from the server.",
            color=SUCCESS_COLOR,
        )
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """
    Setup the moderation cog.

    Args:
        bot (commands.Bot): The bot to add the cog to.
    """
    await bot.add_cog(Moderation(bot))
