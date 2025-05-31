import discord
from discord.ext import commands
from config import DISCORD_TOKEN
import os
import sqlite3
from datetime import datetime, timedelta

# Use full intents so we capture everything
intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)
print("bot.py is running...")

@bot.event
async def on_ready():
    print(f"✅ Atom is online as {bot.user}")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            print(f"🔄 Loading cog: {filename}")
            await bot.load_extension(f"cogs.{filename[:-3]}")
    print("📦 All cogs loaded.")

@bot.event
async def on_presence_update(before, after):
    print(f"[DEBUG] Presence update: {after.display_name}")
    print(f"[DEBUG] Before: {before.activities}")
    print(f"[DEBUG] After: {after.activities}")

    for activity in after.activities:
        if activity.type == discord.ActivityType.playing:
            game_name = activity.name
            target_user_id = after.id

            conn = sqlite3.connect('database/atom.db')
            c = conn.cursor()

            # Check if any users want to be alerted about this person playing this game
            c.execute('''
                SELECT user_id FROM alerts WHERE target_user_id = ? AND game_name = ?
            ''', (target_user_id, game_name))
            users_to_notify = c.fetchall()

            # Check and update last_alerts_sent to avoid duplicates
            for user_id in users_to_notify:
                uid = user_id[0]

                c.execute('''
                    SELECT timestamp FROM last_alerts_sent
                    WHERE user_id = ? AND target_user_id = ? AND game_name = ?
                ''', (uid, target_user_id, game_name))
                result = c.fetchone()

                now = datetime.utcnow()
                should_send = True

                if result:
                    last_sent_time = datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')
                    # Don't resend if sent in last 6 hours
                    if now - last_sent_time < timedelta(hours=6):
                        should_send = False

                if should_send:
                    user = await bot.fetch_user(uid)
                    await user.send(f"🎮 {after.name} just started playing {game_name}!")

                    # Insert or update timestamp
                    c.execute('''
                        INSERT INTO last_alerts_sent (user_id, target_user_id, game_name, timestamp)
                        VALUES (?, ?, ?, ?)
                        ON CONFLICT(user_id, target_user_id, game_name)
                        DO UPDATE SET timestamp=excluded.timestamp
                    ''', (uid, target_user_id, game_name, now.strftime('%Y-%m-%d %H:%M:%S')))

            conn.commit()
            conn.close()

print("🔧 Starting bot setup...")
bot.run(DISCORD_TOKEN)
