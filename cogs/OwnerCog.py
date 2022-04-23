import nextcord
from nextcord.ext import commands, application_checks

from config import Config


class OwnerCog(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @nextcord.slash_command(
        description="Shutdown the client", guild_ids=Config.GUILD_IDs
    )
    @application_checks.is_owner()
    async def shutdown(self, interaction: nextcord.Interaction):
        await interaction.response.send_message("Bye owo!")
        self.bot.loop.stop()
