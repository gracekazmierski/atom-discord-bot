import discord
from discord.ext import commands
from config import DISCORD_TOKEN
import os
import sqlite3

# Use full intents so we capture everything, especially for presence updates
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
    def get_games_being_played(activities):
        games = set()
        if activities:
            for activity in activities:
                if activity and activity.type == discord.ActivityType.playing and activity.name:
                    games.add(activity.name)
        return games

    current_games = get_games_being_played(after.activities)
    previous_games = get_games_being_played(before.activities)

    for game_name in current_games:
        if game_name not in previous_games:
            print(f"[INFO] {after.display_name} started playing {game_name}. Triggering alerts.")
            target_user_id = after.id
            
            users_to_notify_tuples = []
            try:
                conn = sqlite3.connect('database/atom.db')
                c = conn.cursor()
                c.execute('''
                    SELECT user_id FROM alerts WHERE target_user_id = ? AND game_name = ?
                ''', (target_user_id, game_name))
                users_to_notify_tuples = c.fetchall()
                conn.close()
            except sqlite3.Error as e:
                print(f"[ERROR] Database error: {e}")
                return 

            if users_to_notify_tuples:
                print(f"[INFO] Found {len(users_to_notify_tuples)} users to notify for {after.display_name} playing {game_name}.")
                for user_id_tuple in users_to_notify_tuples:
                    user_to_alert = await bot.fetch_user(user_id_tuple[0]) 
                    if user_to_alert:
                        try:
                            await user_to_alert.send(f"🎮 {after.display_name} just started playing {game_name}!")
                        except discord.Forbidden:
                            print(f"❌ Could not send DM to {user_to_alert.name} (ID: {user_id_tuple[0]}). DMs might be disabled or bot blocked.")
                        except discord.HTTPException as e:
                            print(f"⚠️ Failed to send DM to {user_to_alert.name} (ID: {user_id_tuple[0]}): {e}")
                    else:
                        print(f"⚠️ Could not fetch user with ID {user_id_tuple[0]}. Maybe they left a shared server?")


print("🔧 Starting bot setup...")
bot.run(DISCORD_TOKEN)
