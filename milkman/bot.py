import asyncio
import logging
import os
import random

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context
from dotenv import load_dotenv

from .constants import ERROR_COLOR
from .util.database import Database


class CustomFormatter(logging.Formatter):
    """
    Custom formatter for the logging module that adds color to the log messages.
    """

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    RESET = "\033[0m"
    BOLD = "\033[1m"

    COLORS = {
        logging.DEBUG: WHITE + BOLD,
        logging.INFO: GREEN + BOLD,
        logging.WARNING: YELLOW + BOLD,
        logging.ERROR: RED,
        logging.CRITICAL: RED + BOLD,
    }

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log message.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message.
        """
        log_color = self.COLORS.get(record.levelno, self.RESET)
        format_str = (
            "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (white){name}(reset) - {message}".replace(
                "(black)", self.BLACK
            )
            .replace("(reset)", self.RESET)
            .replace("(levelcolor)", log_color)
            .replace("(white)", self.WHITE + self.BOLD)
        )
        formatter = logging.Formatter(format_str, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


class Supervisor(commands.Bot):
    def __init__(
        self,
        *args,
        bot_prefix: str,
        data_path: str,
        logger: logging.Logger,
        db: Database,
        **kwargs,
    ):
        super().__init__(
            *args,
            command_prefix=commands.when_mentioned_or(bot_prefix),
            help_command=None,
            **kwargs,
        )

        self.logger = logger
        self.data_path = data_path
        self.bot_prefix = bot_prefix
        self.db = db

    async def load_cogs(self) -> None:
        """
        Load the cogs by loading each file in the 'cogs/' directory.
        """
        logs_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), "cogs")
        for file in os.listdir(logs_path):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.load_extension(f"milkman.cogs.{extension}")
                    self.logger.info(f"Loaded extension: {extension}")
                except commands.NoEntryPointError:
                    self.logger.info(f"No entry point found for extension: {extension}")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    self.logger.error(
                        f"Failed to load extension: {extension}: Error: {exception}", exc_info=True
                    )

    @tasks.loop(minutes=1.0)
    async def update_status(self) -> None:
        """
        Update the bot's status.
        """
        statuses = [
            "always watching",
            "always counting",
            "always listening",
            "always thinking",
            "always feeling",
            "always breathing",
            "always existing",
            "always behind you",
            "always in your head",
            "always in your bed",
            "always living without you",
        ]

        status = random.choice(statuses)
        await self.change_presence(activity=discord.Game(name=status))

    @update_status.before_loop
    async def before_update_status(self) -> None:
        """
        Wait for the bot to be ready before updating the status.
        """
        await self.wait_until_ready()

    async def setup_hook(self) -> None:
        """
        Set up the bot.
        """
        if self.user is None:
            raise RuntimeError("The bot has not been logged in yet.")

        self.logger.info(f"Logged in as {self.user.name}")
        await self.db.connect()
        await self.db.create_tables()
        await self.load_cogs()
        self.update_status.start()

    async def on_command_completion(self, context: Context) -> None:
        """
        The code in this event is executed every time a normal command has been *successfully* executed.

        Args:
            context (Context): The context of the command that has been executed.
        """
        if context.command is None:
            return

        full_command_name = context.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])
        kwargs = context.kwargs
        args = context.args
        if context.guild is not None:
            self.logger.info(
                (
                    f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by"
                    f"{context.author} (ID: {context.author.id}) with args: {args if args else '(empty)'} and"
                    f"kwargs: {kwargs if kwargs else '(empty)'}"
                )
            )
        else:
            self.logger.info(
                f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs with args:"
                f" {args if args else '(empty)'} and kwargs: {kwargs if kwargs else '(empty)'}"
            )

    async def on_command_error(
        self, ctx: Context, exception: commands.CommandError
    ) -> None:
        """
        The code in this event is executed every time a command has *failed*.

        Args:
            ctx (Context): The context of the command that failed.
            exception (Exception): The exception that was raised.
        """
        if isinstance(exception, commands.CommandOnCooldown):
            minutes, seconds = divmod(exception.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = discord.Embed(
                title="Slow down!",
                description=(
                    f"You are being rate limited. Please wait "
                    f"{f'{hours} hours, ' if round(hours) > 0 else ''}"
                    f"{f'{minutes} minutes, ' if round(minutes) > 0 else ''}"
                    f"{f'{seconds} seconds' if round(seconds) > 0 else ''}."
                ),
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)
        elif isinstance(exception, commands.NotOwner):
            embed = discord.Embed(
                title="Not Owner",
                description="You are not the owner of the bot.",
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)
        elif isinstance(exception, commands.MissingPermissions):
            embed = discord.Embed(
                title="Missing Permissions",
                description=(
                    f"You do not have permission to use this command. "
                    f"Required permission(s): `{', '.join(exception.missing_permissions)}`."
                ),
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)
        elif isinstance(exception, commands.BotMissingPermissions):
            embed = discord.Embed(
                title="Bot Missing Permissions",
                description=(
                    f"I am missing the following permissions to use this command: "
                    f"`{', '.join(exception.missing_permissions)}`."
                ),
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)
        elif isinstance(exception, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Missing Required Argument",
                description=f"You are missing a required argument. Error: `{str(exception).capitalize()}`",
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)
        elif isinstance(exception, commands.BadLiteralArgument):
            embed = discord.Embed(
                title="Bad Literal Argument",
                description=f"You provided an invalid literal argument. Error: `{str(exception).capitalize()}`",
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)
        elif isinstance(exception, commands.BadArgument):
            embed = discord.Embed(
                title="Bad Argument",
                description=f"You provided an invalid argument. Error: `{str(exception).capitalize()}`",
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)
        elif isinstance(exception, commands.CommandNotFound):
            embed = discord.Embed(
                title="Command Not Found",
                description="The command you provided was not found.",
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)
        else:
            raise exception


async def main() -> None:
    """
    The main function of the bot that is responsible for configuring the parameters of the bot
    and setting up the logging system.
    """
    load_dotenv()

    data_dir = os.getenv("DATA_DIR", "data")

    intents = discord.Intents.default()
    intents.message_content = True
    intents.reactions = True

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(CustomFormatter())
    console_handler.setLevel(logging.INFO)

    # Create a file handler

    # Make logs directory if not exists
    logs_dir = os.path.join(data_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    file_path = os.path.join(logs_dir, "supervisor.log")
    file_handler = logging.FileHandler(file_path, encoding="utf-8", mode="w")
    file_handler_formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
    )
    file_handler.setFormatter(file_handler_formatter)
    file_handler.setLevel(logging.DEBUG)

    # Add the handlers to the logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Create a logger for the bot
    logger = logging.getLogger(__name__)

    # Get the environment variables
    discord_token = os.getenv("DISCORD_TOKEN")
    bot_prefix = os.getenv("BOT_PREFIX")

    if not discord_token:
        discord_token_file = os.getenv("DISCORD_TOKEN_FILE")
        if not discord_token_file:
            logger.error("The environment variable DISCORD_TOKEN is not set")
            exit(1)
        with open(discord_token_file, "r") as f:
            discord_token = f.read().strip()

    if not bot_prefix:
        logger.error("The environment variable BOT_PREFIX is not set")
        exit(1)

    db = Database(os.path.join(data_dir, "milkman.db"))

    async with Supervisor(
        data_path=data_dir,
        db=db,
        bot_prefix=bot_prefix,
        logger=logger,
        intents=intents,
    ) as bot:
        await bot.start(discord_token)


if __name__ == "__main__":
    asyncio.run(main())
