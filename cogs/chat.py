import discord
from discord.ext import commands
from ollama_client import query_ollama

CHAT_COG_LOADED = False

class Chat(commands.Cog):
    def __init__(self, bot):
        global CHAT_COG_LOADED
        if CHAT_COG_LOADED:
            return
        self.bot = bot
        CHAT_COG_LOADED = True

    @commands.Cog.listener()
    async def on_message(self, message):
        # 🚫 Ignore bot messages
        if message.author.bot:
            return

        # 🚫 Let actual commands pass through untouched
        ctx = await self.bot.get_context(message)
        if ctx.valid:
            return

        # ✅ DM or server message — respond!
        async with message.channel.typing():
            response = query_ollama(message.content)
        await message.channel.send(response)

async def setup(bot):
    await bot.add_cog(Chat(bot))
