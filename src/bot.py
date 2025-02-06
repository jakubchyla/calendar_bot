from typing import List, Dict
import datetime
import dateutil
import dateutil.parser
import discord
import json
import pathlib


class Bot:
    def __init__(self, token: str, calendar_link: str):
        self.bot = discord.Bot()
        self.calendar_link = calendar_link
        self.calendar: Dict = self.download_calendar_data()
        self.token = token
        self.init_commands()
        self.init_events()

    def init_events(self):
        @self.bot.event
        async def on_ready():
            print(f"Logged in as {self.bot.user}")

    def init_commands(self):
        event = self.bot.create_group("event", "events related commands")

        @event.command(description="Adds event to the calendar")
        async def add(ctx, name: str, description: str, time: str, date: str):
            try:
                date = dateutil.parser.isoparse(date).date().isoformat()
            except ValueError:
                await ctx.respond("wrong date specified, use iso format (YYYY-MM-DD)")
                return
            time = dateutil.parser.parse(time).time().isoformat()[:-3]
            event = {
                "title": name,
                "description": description,
                "time": time
            }
            if date not in self.calendar:
                self.calendar[date] = []
            self.calendar[date].append(event)
            self.write_json()
            await ctx.respond(f"event {name} added at {date} {time}")


        @event.command(description="Remove event from the calendar")
        async def remove(ctx, name: str, date: str):
            try:
                date = dateutil.parser.isoparse(date).date().isoformat()
            except ValueError:
                await ctx.respond("wrong date specified, use iso format (YYYY-MM-DD)")
                return
            if date not in self.calendar:
                await ctx.respond(f"no event at {date} in calendar")
                return
            if name not in [event["title"] for event in self.calendar[date]]:
                await ctx.respond(f"no event named {name} at {date} in calendar")
                return

            self.calendar[date] = [event for event in self.calendar[date] if event["title"] != name]
            if not self.calendar[date]:
                del self.calendar[date]
            self.write_json()
            await ctx.respond(f"event {name} removed from {date}")


        @event.command(description="Print events")
        async def print(ctx):
            events = ""
            INDENT = (" " * 4)
            for date in self.calendar:
                if datetime.date.fromisoformat(date) < datetime.date.today():
                    continue
                events = events + f"{date}\n"
                for event in self.calendar[date]:
                    events = events + f"{INDENT}{event["title"]}\n"
                    events = events + f"{INDENT}{INDENT}{event["time"]}\n"
                    events = events + f"{INDENT}{INDENT}{event["description"]}\n"
                events = events + "\n"
            await ctx.respond(events)

    def write_json(self):
        json_data = json.dumps(self.calendar, indent=4)
        pathlib.Path(self.calendar_link).write_text(json_data)

    def run(self):
        self.bot.run(self.token)

    def download_calendar_data(self):
        calendar_data = pathlib.Path(self.calendar_link).read_text()
        calendar_data = json.loads(calendar_data)
        return calendar_data
