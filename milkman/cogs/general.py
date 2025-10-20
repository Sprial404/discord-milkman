"""
This cog contains general commands that are used to help the user.

Commands:
    - ping: Pings the bot.
    - help: Shows all commands that the bot has loaded.
"""

import discord
from discord.ext import commands
from discord.ext.commands import Context

from milkman.constants import SUCCESS_COLOR, OWNER_COG_NAME, GENERAL_COG_NAME


class General(commands.Cog, name=GENERAL_COG_NAME):
    """
    This cog contains general commands that are used to help the user.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="ping", description="Pings the bot.")
    async def ping(self, ctx: Context) -> None:
        """
        Pings the bot.

        Args:
            ctx (Context): The context of the command.
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms",
            color=SUCCESS_COLOR,
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="help", description="Shows all commands that the bot has loaded."
    )
    async def help(self, ctx: Context) -> None:
        """
        Shows all commands that the bot has loaded.

        Args:
            ctx (Context): The context of the command.
        """
        embed = discord.Embed(
            title="Help",
            description="List of available commands:",
            color=SUCCESS_COLOR,
        )
        for cog_name in self.bot.cogs:
            if cog_name == OWNER_COG_NAME and not (await self.bot.is_owner(ctx.author)):
                continue

            cog = self.bot.get_cog(cog_name)
            cog_commands = cog.get_commands()
            data = []
            if cog_commands:
                for command in cog_commands:
                    description = command.description.partition("\n")[0]
                    data.append(f"`{command.name}` - {description}")
            else:
                data.append("No commands found.")

            help_text = "\n".join(data)
            embed.add_field(
                name=cog_name.capitalize(), value=f"```{help_text}```", inline=False
            )

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """
    Setup the General cog.

    Args:
        bot (commands.Bot): The bot instance.
    """
    await bot.add_cog(General(bot))
