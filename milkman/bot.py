import logging
import os
import random

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context

from dotenv import load_dotenv

from .util.database import Database
from .constants import ERROR_COLOR

load_dotenv()

data_dir = os.getenv("DATA_DIR", "data")

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True


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
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (white){name}(reset) - {message}"
        format = format.replace("(black)", self.BLACK)
        format = format.replace("(reset)", self.RESET)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(white)", self.WHITE + self.BOLD)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(CustomFormatter())

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

# Add the handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


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


class Supervisor(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            intents=intents,
            command_prefix=commands.when_mentioned_or(bot_prefix),
            help_command=None,
        )

        self.logger = logger
        self.db = Database(os.path.join(data_dir, "milkman.db"))
        self.bot_prefix = bot_prefix

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
                        f"Failed to load extension: {extension}: Error: {exception}"
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
        Setup the bot.
        """
        self.logger.info(f"Logged in as {self.user.name}")
        await self.load_cogs()
        self.update_status.start()
        await self.db.connect()
        await self.db.create_tables()

    async def on_command_completion(self, context: Context) -> None:
        """
        The code in this event is executed every time a normal command has been *successfully* executed.

        Args:
            context (Context): The context of the command that has been executed.
        """
        full_command_name = context.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])
        kwargs = context.kwargs
        args = context.args
        if context.guild is not None:
            self.logger.info(
                f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id}) with args: {args if args else '(empty)'} and kwargs: {kwargs if kwargs else '(empty)'}"
            )
        else:
            self.logger.info(
                f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs with args: {args if args else '(empty)'} and kwargs: {kwargs if kwargs else '(empty)'}"
            )

    async def on_command_error(
        self, ctx: Context, exception: commands.CommandError
    ) -> None:
        """
        The code in this event is executed every time a command has *failed*.

        Args:
            context (Context): The context of the command that failed.
            exception (Exception): The exception that was raised.
        """
        if isinstance(exception, commands.CommandOnCooldown):
            minutes, seconds = divmod(exception.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = discord.Embed(
                title="Slow down!",
                description=f"You are being rate limited. Please wait {f'{hours} hours, ' if round(hours) > 0 else ''}{f'{minutes} minutes, ' if round(minutes) > 0 else ''}{f'{seconds} seconds' if round(seconds) > 0 else ''}.",
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
            missing_permissions = [perm.name for perm in exception.missing_permissions]
            embed = discord.Embed(
                title="Missing Permissions",
                description=f"You do not have permission to use this command. Required permission(s): `{', '.join(missing_permissions)}`.",
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)
        elif isinstance(exception, commands.BotMissingPermissions):
            missing_permissions = [perm.name for perm in exception.missing_permissions]
            embed = discord.Embed(
                title="Bot Missing Permissions",
                description=f"I am missing the following permissions to use this command: `{', '.join(missing_permissions)}`.",
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


bot = Supervisor()
bot.run(discord_token)
