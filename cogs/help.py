import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def custom_help(self, ctx):
        embed = discord.Embed(
            title="🤖 Atom Help Menu",
            description="Here's what I can help you with (for now):",
            color=discord.Color.blurple()
        )

        # 📝 Task Commands
        embed.add_field(name="📝 `!addtask [task]`", value="Add a new task.", inline=False)
        embed.add_field(name="📋 `!tasks`", value="View your tasks.", inline=False)
        embed.add_field(name="✅ `!done [task_id]`", value="Mark a task as finished.", inline=False)
        embed.add_field(name="🗑️ `!deletetask [task_id]`", value="Delete a task.", inline=False)

        # ⏰ Reminder Commands
        embed.add_field(name="⏰ `!remindme to [thing] at [time]`", value="Set a reminder. Supports times, dates, and 'tomorrow'.", inline=False)

        # 🎮 Alert Commands
        embed.add_field(name="🎮 `!alert add @User GameName`", value="Get a DM when someone starts playing a specific game.", inline=False)
        embed.add_field(name="🗑️ `!alert remove @User GameName`", value="Remove a game alert.", inline=False)
        embed.add_field(name="📜 `!alert list`", value="View all your game alerts.", inline=False)

        # 📆 Calendar Commands
        embed.add_field(name="📆 `!linkcalendar [ical_url]`", value="Link your Google Calendar using a private iCal URL.", inline=False)
        embed.add_field(name="🕒 `!settimezone [tz_name]`", value="Set your timezone (e.g. `America/Denver`).", inline=False)
        embed.add_field(name="🔍 `!checkcalendar`", value="Check your calendar manually for upcoming events.", inline=False)
        embed.add_field(name="🗑️ `!deletecalendar`", value="Unlink and delete your saved calendar.", inline=False)


        embed.set_footer(text="If I had hands, I'd high five you for using me this well.")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
