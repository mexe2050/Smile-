import discord
from discord.ext import commands
from utils.database import add_mission, get_all_missions, get_user_missions, complete_mission, update_points

class Missions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.missions_channel_id = None

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_missions_channel(self, ctx, channel: discord.TextChannel):
        self.missions_channel_id = channel.id
        await ctx.send(f"Missions channel set to {channel.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_mission(self, ctx, description: str, points: int):
        add_mission(description, points)
        await ctx.send(f"Mission added: {description} - {points} points")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def daily_missions(self, ctx):
        missions = get_all_missions()
        if not missions:
            await ctx.send("No missions available. Add some missions first!")
            return
        missions_text = "\n".join([f"{i}. {m['description']} - {m['points']} points" for i, m in enumerate(missions)])
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
        missions = get_all_missions()
        if mission_index < 0 or mission_index >= len(missions):
            await ctx.send("Invalid mission index.")
            return
        mission = missions[mission_index]
        if complete_mission(user.id, mission):
            update_points(user.id, mission['points'])
            await ctx.send(f"{user.mention} has completed the mission: {mission['description']} and earned {mission['points']} points!")
        else:
            await ctx.send(f"{user.mention} has already completed this mission.")

    @complete_mission.error
    async def complete_mission_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Error: Missing required argument. Usage: !complete_mission <@user> <mission_index>")

async def setup(bot):
    await bot.add_cog(Missions(bot))
    print("Missions cog loaded")