"""
This cog contains fun commands that are used to entertain the user.

Commands:
- 8ball: Ask the bot a question.
- lyrics: Get the lyrics to a song.
- slap: Slap a user.
- roll: Roll a die.
- coinflip: Flip a coin.
- f: Press F to pay respect.
- bapbap: Bapbap.
- slot: Spin the slot machine.
- roulette: Play roulette.
- avatar: Get a random avatar quote.
"""

import asyncio
import aiohttp
from typing import Literal, Optional
from discord.ext import commands
from discord.ext.commands import Cog
from discord import app_commands
from discord.ext.commands import Context
from milkman.constants import (
    SUCCESS_COLOR,
    ERROR_COLOR,
    FUN_COG_NAME,
    AVATAR_QUOTES,
    SLAP_IMAGES,
    LYRICS_API_URL,
)
from milkman.util import deduplicate_newlines
import discord
import random


class Fun(Cog, name=FUN_COG_NAME):
    """
    This cog contains fun commands that are used to entertain the user.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def _get_lyrics(self, artist: str, title: str) -> Optional[str]:
        """
        Get the lyrics to a song.
        """
        url = LYRICS_API_URL.format(artist=artist, title=title)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return None

                data = await response.json()
                return data.get("lyrics")

    @commands.hybrid_command(name="lyrics", description="Get the lyrics to a song.")
    @app_commands.describe(
        song="The song to get the lyrics to.", artist="The artist of the song."
    )
    async def lyrics(self, ctx: Context, song: str, artist: str) -> None:
        """
        Get the lyrics to a song.

        Args:
            ctx (Context): The context of the command.
            song (str): The song to get the lyrics to.
            artist (str): The artist of the song.
        """
        embed = discord.Embed(
            description="Searching for lyrics...",
            color=SUCCESS_COLOR,
        )
        msg = await ctx.send(embed=embed)

        lyrics = await self._get_lyrics(artist, song)
        if lyrics is None:
            embed.title = "🔴"
            embed.description = "No lyrics found for the given song and artist."
            embed.color = ERROR_COLOR
            await msg.edit(embed=embed)
            return

        lyrics = deduplicate_newlines(lyrics)
        lyrics = lyrics.replace("\n", "\n\n")
        embed.title = "🎵"
        embed.description = lyrics
        embed.set_footer(text=f"Song: {song.title()} - Artist: {artist.title()}")
        await msg.edit(embed=embed)

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

    @commands.hybrid_command(name="crazy", description="I was crazy once.")
    async def crazy(self, ctx: Context, times: int = 1) -> None:
        """
        I was crazy once.

        Args:
            ctx (Context): The context of the command.
            times (int): The number of times to repeat the message, defaults to 1.
        """
        if times < 1:
            embed = discord.Embed(
                title="🔴",
                description="Invalid number of times, please enter a valid positive integer.",
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)
            return

        if times > 10:
            embed = discord.Embed(
                title="🔴",
                description="Too many times, please enter a number less than 20.",
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)
            return

        prompt = "Crazy?\nI was crazy once.\nThey locked me in a room.\nA rubber room.\nA rubber room with rats.\nAnd rats make me crazy.\n"
        await ctx.send(prompt * times)

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
        embed.set_image(url=random.choice(SLAP_IMAGES))
        embed.set_thumbnail(url=f"{user.avatar.url}")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="roll", description="Roll a die.")
    @app_commands.describe(
        sides="The number of sides on the die.", dice="The number of dice to roll."
    )
    async def roll(self, ctx: Context, sides: int, dice: int = 1) -> None:
        """
        Roll a die.

        Args:
            ctx (Context): The context of the command.
            sides (int): The number of sides on the die.
            dice (int): The number of dice to roll, defaults to 1.
        """
        if sides < 1:
            embed = discord.Embed(
                title="🔴",
                description="Invalid number of sides, please enter a valid positive integer.",
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)
            return

        if dice < 1:
            embed = discord.Embed(
                title="🔴",
                description="Invalid number of dice, please enter a valid positive integer.",
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)
            return
        
        if sides > 100:
            embed = discord.Embed(
                title="🔴",
                description="Too many sides, please enter a number less than 100.",
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)
            return
        
        if dice > 200:
            embed = discord.Embed(
                title="🔴",
                description="Too many dice, please enter a number less than 200.",
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)
            return
        

        dice_word = "die" if dice == 1 else "dice"

        embed = discord.Embed(
            description=f"{ctx.author.mention} is rolling {dice:,} {dice_word} on a {sides:,}-sided die...",
            color=SUCCESS_COLOR,
        )
        msg = await ctx.send(embed=embed)

        results = [random.randint(1, sides) for _ in range(dice)]
        total = sum(results)
        results_str = ", ".join([f"{result:,}" for result in results])

        embed.title = "🎲"
        embed.description = f"{ctx.author.mention} rolled {dice:,} {dice_word} on a {sides:,}-sided die."

        if 1 < len(results) <= 12:
            embed.add_field(name="Results", value=results_str)
        embed.add_field(name="Total", value=f"**{total:,}**")
        await msg.edit(embed=embed)

    @commands.hybrid_command(name="coinflip", description="Flip a coin.")
    async def coinflip(self, ctx: Context) -> None:
        """
        Flip a coin.

        Args:
            ctx (Context): The context of the command.
        """
        result = random.choice(["Heads", "Tails"])
        await ctx.send(f"The coin landed on {result}.")

    @commands.hybrid_command(name="f", description="Press F to pay respect")
    @app_commands.describe(reason="The reason for the respect.")
    async def f(self, ctx: Context, reason: commands.clean_content = None) -> None:
        """
        Press F to pay respect.

        Args:
            ctx (Context): The context of the command.
            reason (str): The reason for the respect.
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

        Args:
            ctx (Context): The context of the command.
        """
        await ctx.send(
            "It's called bapbap because that's what it says when you start the round."
        )

    @commands.hybrid_command(
        name="slot", description="Spin the slot machine.", aliases=["spin", "gamble"]
    )
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def slot(self, ctx: Context) -> None:
        """
        Spin the slot machine.

        Args:
            ctx (Context): The context of the command.
        """
        items = ["🍎", "🍊", "🍌", "🍇", "🍓", "🍒", "🍑", "🍍", "🥝", "🥑"]
        result = random.choices(items, k=3)

        message = ""
        won = False
        if result[0] == result[1] == result[2] == "🍒":
            message = "Jackpot! 💰💰💰"
            won = True
        elif result[0] == result[1] == result[2]:
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
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def roulette(
        self, ctx: Context, color: Literal["red", "black", "green", "yellow"]
    ) -> None:
        """
        Play roulette.

        Args:
            ctx (Context): The context of the command.
            color (str): The color to bet on.
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

        embed = discord.Embed(
            title="🔵🔴🟢🟡",
            description=f"Spinning the wheel...",
            color=SUCCESS_COLOR,
        )
        msg = await ctx.send(embed=embed)

        await asyncio.sleep(3)

        response = f"The wheel landed on {result}."
        if picked_color == result:
            response += " You won! 🎉"
        else:
            response += " You lost! 😢"

        embed.description = response
        embed.color = SUCCESS_COLOR if picked_color == result else ERROR_COLOR
        await msg.edit(embed=embed)

    @commands.hybrid_command(name="avatar", description="Get a random avatar quote.")
    async def avatar(self, ctx: Context) -> None:
        """
        Get a random avatar quote.

        Args:
            ctx (Context): The context of the command.
        """
        quote = random.choice(AVATAR_QUOTES)
        embed = discord.Embed(
            title="👤",
            description=quote,
            color=SUCCESS_COLOR,
        )
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """
    Setup the Fun cog.

    Args:
        bot (commands.Bot): The bot instance.
    """
    await bot.add_cog(Fun(bot))
