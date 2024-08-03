import discord
from discord.ext import commands
import json
from utils.database import update_points, get_user_missions, complete_mission

class Missions(commands.Cog):
    # ... rest of the code ...
    def __init__(self, bot):
        self.bot = bot
        self.missions_channel_id = None
        self.missions = []
        self.load_config()

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                self.missions_channel_id = config.get('missions_channel_id')
                self.missions = config.get('missions', [])
        except FileNotFoundError:
            pass

    def save_config(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
        config['missions_channel_id'] = self.missions_channel_id
        config['missions'] = self.missions
        with open('config.json', 'w') as f:
            json.dump(config, f)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_missions_channel(self, ctx, channel: discord.TextChannel):
        self.missions_channel_id = channel.id
        self.save_config()
        await ctx.send(f"Missions channel set to {channel.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_mission(self, ctx, description: str, points: int):
        self.missions.append({"description": description, "points": points})
        self.save_config()
        await ctx.send(f"Mission added: {description} - {points} points")

    @commands.command()
    async def daily_missions(self, ctx):
        if ctx.channel.id != self.missions_channel_id:
            await ctx.send("This command can only be used in the designated missions channel.")
            return

        if not self.missions:
            await ctx.send("No missions available. Ask an admin to add some!")
            return

        missions_text = "\n".join([f"{m['description']} - {m['points']} points" for m in self.missions])
        await ctx.send(f"Daily Missions:\n{missions_text}")

    @commands.command()
    async def check_missions(self, ctx):
        user_missions = get_user_missions(ctx.author.id)
        if not user_missions:
            await ctx.send("You haven't completed any missions yet.")
            return

        missions_text = "\n".join([f"{m['description']} - {m['points']} points" for m in user_missions])
        await ctx.send(f"Your completed missions:\n{missions_text}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def complete_mission(self, ctx, user: discord.Member, mission_index: int):
        if mission_index < 0 or mission_index >= len(self.missions):
            await ctx.send("Invalid mission index.")
            return

        mission = self.missions[mission_index]
        complete_mission(user.id, mission)
        update_points(user.id, mission['points'])
        await ctx.send(f"{user.mention} has completed the mission: {mission['description']} and earned {mission['points']} points!")

async def setup(bot):
    await bot.add_cog(Missions(bot))