import discord
from discord.ext import commands
from config import DISCORD_TOKEN
import os
import sqlite3
from datetime import datetime

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

@bot.event
async def on_presence_update(before, after):
    print(f"[DEBUG] Presence update: {after.display_name}")
    print(f"[DEBUG] Before: {before.activities}")
    print(f"[DEBUG] After: {after.activities}")
    print(f"[DEBUG] Loaded bot commands: {bot.commands}")
    print(f"[DEBUG] Alerts cog initialized at {datetime.now()}")


    for activity in after.activities:
        if activity.type == discord.ActivityType.playing:
            game_name = activity.name
            target_user_id = after.id

            conn = sqlite3.connect('database/atom.db')
            c = conn.cursor()
            c.execute('''
                SELECT user_id FROM alerts WHERE target_user_id = ? AND game_name = ?
            ''', (target_user_id, game_name))
            users_to_notify = c.fetchall()
            conn.close()

            for user_id in users_to_notify:
                user = await bot.fetch_user(user_id[0])
                await user.send(f"🎮 {after.name} just started playing {game_name}!")

print("🔧 Starting bot setup...")
bot.run(DISCORD_TOKEN)