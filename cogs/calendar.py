import discord
from discord.ext import commands
import sqlite3
import requests
import recurring_ical_events
from icalendar import Calendar as iCalParser
from datetime import datetime, timedelta, date
import pytz

class CalendarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="linkcalendar")
    async def link_calendar(self, ctx, ical_url: str):
        """Links your iCalendar (.ics) URL."""
        conn = sqlite3.connect('database/atom.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO calendars (user_id, ical_url, timezone)
            VALUES (?, ?, COALESCE((SELECT timezone FROM calendars WHERE user_id = ?), 'America/Denver'))
            ON CONFLICT(user_id) DO UPDATE SET ical_url = excluded.ical_url
        ''', (str(ctx.author.id), ical_url, str(ctx.author.id)))
        conn.commit()
        conn.close()
        await ctx.send("✅ Your calendar has been linked. Run `!checkcalendar` to see your upcoming events.")

    @commands.command(name="deletecalendar")
    async def delete_calendar(self, ctx):
        """Deletes your linked iCalendar."""
        conn = sqlite3.connect('database/atom.db')
        c = conn.cursor()
        c.execute("DELETE FROM calendars WHERE user_id = ?", (str(ctx.author.id),))
        conn.commit()
        conn.close()
        await ctx.send("🗑️ Your linked calendar has been deleted.")

    @commands.command(name="settimezone")
    async def set_timezone(self, ctx, tz: str):
        """Sets your timezone for event times."""
        if tz not in pytz.all_timezones:
            await ctx.send("❌ Invalid timezone. Please use a valid TZ database name from here: <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones>")
            return

        conn = sqlite3.connect('database/atom.db')
        c = conn.cursor()
        c.execute("UPDATE calendars SET timezone = ? WHERE user_id = ?", (tz, str(ctx.author.id)))
        conn.commit()
        conn.close()
        await ctx.send(f"✅ Your timezone has been set to `{tz}`.")

    @commands.command(name="checkcalendar")
    async def check_calendar_now(self, ctx):
        """Checks your calendar for upcoming events with titles in the next 3 days."""
        await ctx.send("🔍 Checking your calendar for events in the next 3 days...")
        await self.check_and_send_calendar_updates(ctx)

    async def check_and_send_calendar_updates(self, ctx):
        """The core logic that is ONLY called by the !checkcalendar command."""
        conn = sqlite3.connect('database/atom.db')
        c = conn.cursor()
        c.execute('SELECT user_id, ical_url, timezone FROM calendars WHERE user_id = ?', (str(ctx.author.id),))
        row = c.fetchone()
        conn.close()

        if not row:
            await ctx.send("You don't have a calendar linked. Use `!linkcalendar <URL>` first.")
            return
            
        user_id, ical_url, tz = row
        user = ctx.author

        now = datetime.now(pytz.utc)
        cutoff = now + timedelta(days=3)

        try:
            r = requests.get(ical_url)
            r.raise_for_status()
            parsed_cal = iCalParser.from_ical(r.text)
            user_tz = pytz.timezone(tz or "America/Denver")
            events = recurring_ical_events.of(parsed_cal).between(now, cutoff)
            
            lines = []
            for event in sorted(events, key=lambda e: e.start):
                # --- CORRECTED LOGIC ---
                # Access the standard 'SUMMARY' field directly. This is the most reliable way.
                event_name = event.get('SUMMARY')

                # Skip any event that doesn't have a SUMMARY field.
                if not event_name:
                    continue
                # --- END CORRECTION ---

                start_time = event.start
                if isinstance(start_time, datetime):
                    local_time = start_time.astimezone(user_tz)
                    if getattr(event, 'all_day', False) or (hasattr(event, 'end') and (event.end - event.start).days >= 1):
                        lines.append(f"• **{event_name}** on {local_time.strftime('%A, %b %d')} (All day)")
                    else:
                        lines.append(f"• **{event_name}** on {local_time.strftime('%A, %b %d')} at {local_time.strftime('%I:%M %p')}")
                elif isinstance(start_time, date):
                    lines.append(f"• **{event_name}** on {start_time.strftime('%A, %b %d')} (All day)")

            if not lines:
                await user.send("I checked your calendar but couldn't find any events with titles in the next 3 days.")
                return

            header = "📆 **Your upcoming events for the next 3 days:**"
            await user.send(f"{header}\n" + "\n".join(lines))

        except Exception as e:
            error_message = f"An error occurred while checking your calendar: {e}"
            print(f"[Calendar Error] {user_id}: {e}")
            if "404" in str(e) or "Not Found" in str(e):
                error_message = "Your calendar link returned a 'Not Found' error. Please check the URL."
            await user.send(f"❌ {error_message}")


async def setup(bot):
    await bot.add_cog(CalendarCog(bot))