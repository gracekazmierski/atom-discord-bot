async def setup(bot):
    await bot.add_cog(Tasks(bot))

from discord.ext import commands

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Add commands here later
