import discord
from discord.ext import commands
import sqlite3
from datetime import datetime

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="addtask")
    async def add_task(self, ctx, *, task):
        conn = sqlite3.connect("database/atom.db")
        c = conn.cursor()
        c.execute("INSERT INTO tasks (user_id, description) VALUES (?, ?)", (ctx.author.id, task))
        task_id = c.lastrowid
        conn.commit()
        conn.close()
        await ctx.send(f"✅ Task added (ID: `{task_id}`): **{task}**")


    @commands.command(name="tasks")
    async def view_tasks(self, ctx):
        conn = sqlite3.connect("database/atom.db")
        c = conn.cursor()
        c.execute("SELECT id, description, is_done FROM tasks WHERE user_id = ?", (ctx.author.id,))
        rows = c.fetchall()
        conn.close()

        if not rows:
            await ctx.send("📭 You have no tasks.")
            return

        msg = "\n".join(
            [f"[{'✅' if done else '❌'}] {task_id}: {desc}" for task_id, desc, done in rows]
        )
        await ctx.send(f"📋 **Your tasks:**\n{msg}")

    @commands.command(name="done")
    async def mark_done(self, ctx, task_id: int):
        conn = sqlite3.connect("database/atom.db")
        c = conn.cursor()
        c.execute("UPDATE tasks SET is_done = 1 WHERE id = ? AND user_id = ?", (task_id, ctx.author.id))
        conn.commit()
        conn.close()
        await ctx.send(f"✅ Marked task {task_id} as done.")

    @commands.command(name="deletetask")
    async def delete_task(self, ctx, task_id: int):
        conn = sqlite3.connect("database/atom.db")
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, ctx.author.id))
        conn.commit()
        conn.close()
        await ctx.send(f"🗑️ Deleted task {task_id}.")

async def setup(bot):
    await bot.add_cog(Tasks(bot))
