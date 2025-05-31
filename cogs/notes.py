async def setup(bot):
    await bot.add_cog(Notes(bot))

from discord.ext import commands

class Notes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Add commands here later
