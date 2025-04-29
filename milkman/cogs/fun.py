"""
This cog contains fun commands that are used to entertain the user.

Commands:
- 8ball: Ask the bot a question.
- slap: Slap a user.
- roll: Roll a die.
- coinflip: Flip a coin.
"""

import asyncio
from typing import Literal
from discord.ext import commands
from discord.ext.commands import Cog
from discord import app_commands
from discord.ext.commands import Context
from milkman.constants import SUCCESS_COLOR, ERROR_COLOR, FUN_COG_NAME
import discord
import random


class Fun(Cog, name=FUN_COG_NAME):
    """
    This cog contains fun commands that are used to entertain the user.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

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
            description=f"{ctx.author.mention} slapped {user.mention} for {reason}",
            color=SUCCESS_COLOR,
        )
        embed.set_image(
            url=f"https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExamNjdDN6cDh1anlhd3Y3YTM5Njc3djlhNzQ0ZXUwOHZ3aXFqODhveiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/lX03hULhgCYQ8/giphy.gif"
        )
        embed.set_thumbnail(url=f"{user.avatar.url}")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="roll", description="Roll a die.")
    @app_commands.describe(sides="The number of sides on the die.")
    async def roll(self, ctx: Context, sides: int) -> None:
        """
        Roll a die.

        Args:
            ctx (Context): The context of the command.
            sides (int): The number of sides on the die.
        """
        result = random.randint(1, sides)
        embed = discord.Embed(
            title="🎲",
            description=f"{ctx.author.mention} rolled a {result} on a {sides}-sided die.",
            color=SUCCESS_COLOR,
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="coinflip", description="Flip a coin.")
    async def coinflip(self, ctx: Context) -> None:
        """
        Flip a coin.
        """
        result = random.choice(["Heads", "Tails"])
        await ctx.send(f"The coin landed on {result}.")

    @commands.hybrid_command(name="f", description="Press F to pay respect")
    @app_commands.describe(reason="The reason for the respect.")
    async def f(self, ctx: Context, reason: commands.clean_content = None) -> None:
        """
        Press F to pay respect.
        """
        hearts = ["💖", "💙", "💚", "💛", "💜", "💝", "💞", "💟", "❤"]
        reason = f"for **{reason}**" if reason else ""

        await ctx.send(
            f"**{ctx.author.mention}** has paid their respects {reason} {random.choice(hearts)}"
        )

    @commands.hybrid_command(name="bapbap", description="Bapbap.")
    async def bapbap(self, ctx: Context) -> None:
        """
        Bapbap.
        """
        await ctx.send(
            "It's called bapbap because that's what it says when you start the round."
        )

    @commands.hybrid_command(
        name="slot", description="Spin the slot machine.", aliases=["spin", "gamble"]
    )
    async def slot(self, ctx: Context) -> None:
        """
        Spin the slot machine.
        """
        items = ["🍎", "🍊", "🍌", "🍇", "🍓", "🍒", "🍑", "🍍", "🥝", "🥑"]
        result = random.choices(items, k=3)

        message = ""
        if result[0] == result[1] == result[2]:
            message = "All matching, you won! 🎉"
            won = True
        elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
            message = "Two matching, you won! 🎉"
            won = True
        else:
            message = "No matching, you lost! 😢"
            won = False

        embed = discord.Embed(
            title="🎰",
            description=f"[ {result[0]} {result[1]} {result[2]} ]\n\n{ctx.author.mention}, {message}",
            color=SUCCESS_COLOR if won else ERROR_COLOR,
        )
        embed.set_footer(text=f"Spin the slot machine to win!")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="roulette", description="Play roulette.")
    @app_commands.describe(color="The color to bet on.")
    async def roulette(
        self, ctx: Context, color: Literal["red", "black", "green", "yellow"]
    ) -> None:
        """
        Play roulette.
        """
        colors = ["red", "black", "green", "yellow"]

        picked_color = color.lower()
        if picked_color not in colors:
            embed = discord.Embed(
                title="🔴",
                description=f"Invalid color, please enter a valid color.\n\nValid colors: {', '.join(colors)}",
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)
            return

        result = random.choice(colors)
        msg = await ctx.send(f"Spinning the wheel 🔵🔴🟢🟡...")

        await asyncio.sleep(3)

        response = f"The wheel landed on {result}."
        if picked_color == result:
            response += " You won! 🎉"
        else:
            response += " You lost! 😢"

        await msg.edit(content=response)


async def setup(bot: commands.Bot) -> None:
    """
    Setup the Fun cog.

    Args:
        bot (commands.Bot): The bot instance.
    """
    await bot.add_cog(Fun(bot))
