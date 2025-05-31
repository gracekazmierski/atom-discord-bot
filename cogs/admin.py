async def setup(bot):
    await bot.add_cog(Admin(bot))

from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # You can add admin commands here later
