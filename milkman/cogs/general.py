"""
This cog contains general commands that are used to help the user.

Commands:
    - ping: Pings the bot.
    - help: Shows all commands that the bot has loaded.
    - 8ball: Ask the bot a question.
    - slap: Slap a user.
"""

import random
import discord
from discord import app_commands
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
            for command in cog_commands:
                description = command.description.partition("\n")[0]
                data.append(f"`{command.name}` - {description}")
            help_text = "\n".join(data)
            embed.add_field(
                name=cog_name.capitalize(), value=f"```{help_text}```", inline=False
            )

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="8ball", description="Ask the bot a question.")
    @app_commands.describe(question="The question to ask the bot.")
    async def eightball(self, ctx: Context, question: str) -> None:
        """
        Ask the bot a question.

        Args:
            ctx (Context): The context of the command.
            question (str): The question to ask the bot.
        """
        answers = [
            "It is certain.",
            "It is decidedly so.",
            "You may rely on it.",
            "Without a doubt.",
            "Yes - definitely.",
            "As I see, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again later.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
        ]
        response = random.choice(answers)
        embed = discord.Embed(
            title="🎱",
            description=f"{response}",
            color=SUCCESS_COLOR,
        )
        embed.set_footer(text=f"The question was: {question}")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="slap", description="Slap a user.")
    @app_commands.describe(user="The user to slap.", reason="The reason for the slap.")
    async def slap(
        self, ctx: Context, user: discord.Member, reason: str = "Because I can."
    ) -> None:
        """
        Slap a user.

        Args:
            ctx (Context): The context of the command.
            user (discord.Member): The user to slap.
            reason (str): The reason for the slap.
        """
        embed = discord.Embed(
            title="👋",
            description=f"{ctx.author} slapped {user.mention} for {reason}",
            color=SUCCESS_COLOR,
        )
        embed.set_image(
            url=f"https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExamNjdDN6cDh1anlhd3Y3YTM5Njc3djlhNzQ0ZXUwOHZ3aXFqODhveiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/lX03hULhgCYQ8/giphy.gif"
        )
        embed.set_thumbnail(url=f"{ctx.author.avatar.url}")
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """
    Setup the General cog.

    Args:
        bot (commands.Bot): The bot instance.
    """
    await bot.add_cog(General(bot))
