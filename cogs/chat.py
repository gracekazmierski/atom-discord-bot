import discord
from discord.ext import commands
from ollama_client import query_ollama

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore bot messages
        if message.author.bot:
            return

        # Process commands like !ask
        await self.bot.process_commands(message)

        # Only respond in DMs
        if isinstance(message.channel, discord.DMChannel):
            await message.channel.typing()
            response = await query_ollama(message.content)

            MAX_LENGTH = 2000
            if len(response) <= MAX_LENGTH:
                await message.channel.send(response)
            else:
                for i in range(0, len(response), MAX_LENGTH):
                    await message.channel.send(response[i:i+MAX_LENGTH])

async def setup(bot):
    await bot.add_cog(Chat(bot))
