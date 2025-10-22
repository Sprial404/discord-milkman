from discord.ext import commands

from milkman.constants import REACTION_ROLES_COG_NAME


class ReactionRoles(commands.Cog, name=REACTION_ROLES_COG_NAME):
    """
    This cog handles adding and removing reaction roles to a message so that users can react to a message to get a role.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot


async def setup(bot: commands.Bot) -> None:
    """
    Set up the ReactionRoles cog.

    Args:
        bot (commands.Bot): The bot instance.
    """
    await bot.add_cog(ReactionRoles(bot))
