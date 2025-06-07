import discord
from discord.ext import commands
from user_data import add_game_alert, get_game_alerts_for_user, remove_game_alert
from datetime import datetime
import traceback


class Alerts(commands.Cog):
    def __init__(self, bot):        
        self.bot = bot

    @commands.command(name="alert")
    async def alert(self, ctx, action, target_user_mention: str = None, *, game_name: str = None):

        if ctx.author.bot:
            return

        if action == "add":
            if not target_user_mention or not game_name:
                await ctx.send("Usage: `!alert add @User GameName`")
                return

            try:
                target_user = await commands.MemberConverter().convert(ctx, target_user_mention)
            except commands.MemberNotFound:
                await ctx.send("❌ Couldn't find that user. Make sure they're in the server and mentioned properly.")
                return
            add_game_alert(ctx.author.id, target_user.id, game_name)
            await ctx.send(f"✅ Alert added! You'll be notified when {target_user.name} starts playing {game_name}.")
            return

        elif action == "remove":
            if not target_user_mention or not game_name:
                await ctx.send("Usage: `!alert remove @User GameName`")
                return

            try:
                target_user = await commands.MemberConverter().convert(ctx, target_user_mention)
            except commands.MemberNotFound:
                await ctx.send("❌ Couldn't find that user. Make sure they're in the server and mentioned properly.")
                return

            remove_game_alert(ctx.author.id, target_user.id, game_name)
            await ctx.send(f"🗑️ Alert removed for {target_user.name} and {game_name}.")

        elif action == "list":
            alerts = get_game_alerts_for_user(ctx.author.id)
            if alerts:
                alert_lines = []
                for target_id, game in alerts:
                    user = await self.bot.fetch_user(target_id)
                    alert_lines.append(f"🔔 Notify me when {user.name} plays {game}")
                alert_str = "\n".join(alert_lines)

                if ctx.guild:
                    channel = discord.utils.get(ctx.guild.text_channels, name="alerts")
                    if channel:
                        await channel.send(alert_str)
                        return

                # fallback to wherever the command was issued (DM or regular channel)
                await ctx.send(alert_str)
            else:
                await ctx.send("You don’t have any game alerts set.")
        else:
            await ctx.send("Invalid action. Use `add`, `remove`, or `list`.")

async def setup(bot):
    await bot.add_cog(Alerts(bot))