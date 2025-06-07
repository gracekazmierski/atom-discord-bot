import discord
from discord.ext import commands, tasks
import sqlite3
from datetime import datetime
import dateparser
import re

class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_reminders.start()  # Start the background reminder checker

    @commands.command(name="remindme")
    async def remind_me(self, ctx, *, message):
        # Extract the reminder using regex
        match = re.search(r"to (.+?) at (.+)", message)
        if not match:
            await ctx.send("❌ Try `!remindme to do something at 3:00 PM`, or `on June 10 at 3:00 PM`")
            return

        reminder_text, time_str = match.groups()

        # Parse the natural language time
        remind_at = dateparser.parse(time_str, settings={'PREFER_DATES_FROM': 'future'})

        if not remind_at:
            await ctx.send("❌ I couldn’t understand the time. Try `at 2:30 PM`, `tomorrow at 10`, or `on June 10 at 5`.")
            return

        # Save it in the database
        conn = sqlite3.connect("database/atom.db")
        c = conn.cursor()
        c.execute("INSERT INTO reminders (user_id, reminder, remind_at) VALUES (?, ?, ?)",
                  (ctx.author.id, reminder_text, remind_at))
        conn.commit()
        conn.close()

        await ctx.send(f"✅ I’ll remind you to **{reminder_text}** on **{remind_at.strftime('%A %b %d at %I:%M %p')}**.")

    @tasks.loop(seconds=60)
    async def check_reminders(self):
        conn = sqlite3.connect("database/atom.db")
        c = conn.cursor()
        c.execute("SELECT id, user_id, reminder FROM reminders WHERE remind_at <= ?", (datetime.now(),))
        due = c.fetchall()

        for reminder_id, user_id, text in due:
            user = await self.bot.fetch_user(int(user_id))
            try:
                await user.send(f"⏰ Reminder: {text}")
            except Exception as e:
                print(f"❌ Failed to DM {user_id}: {e}")
            c.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))

        conn.commit()
        conn.close()

    @check_reminders.before_loop
    async def before_reminder_loop(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Reminders(bot))
