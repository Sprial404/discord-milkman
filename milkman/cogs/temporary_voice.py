"""
This cog contains the interaction for creating a temporary voice channel.
"""

import logging
from datetime import datetime

import discord
from discord.ext import commands

from milkman.constants import TEMPORARY_VOICE_COG_NAME, TEMPORARY_VOICE_CHANNEL_NAME
from milkman.util.database import TemporaryChannel

logger = logging.getLogger(__name__)

class TemporaryVoice(commands.Cog, name=TEMPORARY_VOICE_COG_NAME):
    """
    A cog for creating temporary voice channels.
    """
    def __init__(self, bot: commands.Bot):
        """
        Initializes the TemporaryVoice cog.
          Args:
            bot (commands.Bot): The bot instance to which this cog will be added.
        """
        self.bot = bot
        self.temporary_channels = {}

    async def clean_up(self):
        """
        Cleanup function to remove temporary voice channels that are no longer needed.
        """
        logger.info("Cleaning up temporary voice channels")

        channels_to_remove = []
        for channel_id, temporary_channel in list(self.temporary_channels.items()):
            channel = self.bot.get_channel(int(temporary_channel.channel_id))
            if channel is None:
                logger.warning(f"Temporary channel {temporary_channel.channel_id} not found in cache, marking for removal")
                channels_to_remove.append(channel_id)
                continue

            assert isinstance(channel, discord.VoiceChannel), "Channel is not a voice channel"

            if len(channel.members) == 0:
                try:
                    logger.info(f"Deleting temporary voice channel: {channel.name}")
                    await channel.delete(reason="Temporary voice channel cleanup")
                    channels_to_remove.append(channel_id)
                except (discord.Forbidden, discord.HTTPException) as e:
                    logger.error(f"Failed to delete temporary voice channel {channel.name}: {e}", exc_info=True)
        
        # Remove channels from the dictionary
        for channel_id in channels_to_remove:
            if channel_id in self.temporary_channels:
                logger.info(f"Removing temporary channel {channel_id} from tracking")
                await self.bot.db.remove_temporary_channel(
                    channel_id=channel_id,
                    guild_id=self.temporary_channels[channel_id].guild_id,
                )
                del self.temporary_channels[channel_id]

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """
        Listens for voice state updates to handle temporary voice channel creation.

        Args:
            member (discord.Member): The member whose voice state has changed.
            before (discord.VoiceState): The previous voice state of the member.
            after (discord.VoiceState): The new voice state of the member.
        """
        logger.debug(f"Voice state update for {member.name}: {before} -> {after}")
        
        if after.channel is not None and after.channel.name == TEMPORARY_VOICE_CHANNEL_NAME:
            member_name = member.nick or member.name 
            temporary_channel_name = f"{member_name}'s Area"
            temporary_channel = await after.channel.clone(
                name=temporary_channel_name,
                reason="Temporary voice channel",
            )
            
            channel = await self.bot.db.add_temporary_channel(
                channel_id=temporary_channel.id,
                guild_id=temporary_channel.guild.id,
                user_id=member.id,
            )
            
            self.temporary_channels[str(temporary_channel.id)] = channel# Give member permission to manage the channel
            await temporary_channel.set_permissions(member, manage_channels=True)
            logger.info(f"Created temporary voice channel: {temporary_channel.name} for {member.name}")
            await member.move_to(temporary_channel)
        
        if before.channel is not None:
            # Check if the channel being left is a temporary channel
            channel_id = str(before.channel.id)
            if channel_id in self.temporary_channels and len(before.channel.members) == 0:
                logger.info(f"Deleting temporary voice channel: {before.channel.name} as it is empty")
                await before.channel.delete(reason="Temporary voice channel empty")
                await self.bot.db.remove_temporary_channel(
                    channel_id=before.channel.id,
                    guild_id=before.channel.guild.id,
                )                # Remove the channel from the dictionary
                del self.temporary_channels[channel_id]

    async def cog_load(self):
        """
        Load the cog and set up any necessary listeners or initial state.
        """
        active_channels = await self.bot.db.get_active_temporary_channels()
        # Convert list to dictionary with channel_id as key
        self.temporary_channels = {str(channel.channel_id): channel for channel in active_channels}
        await self.clean_up()

    async def cog_unload(self):
        """
        Cleanup when the cog is unloaded.
        """
        await self.clean_up()


async def setup(bot: commands.Bot) -> None:
    """
    Setup function to add the TemporaryVoice cog to the bot.

    Args:
        bot (commands.Bot): The bot instance to add the cog to.
    """
    await bot.add_cog(TemporaryVoice(bot))