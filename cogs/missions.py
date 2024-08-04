import discord
from discord.ext import commands
from utils.database import add_mission, get_all_missions, get_user_missions, complete_mission, update_points

class Missions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_mission(self, ctx, *, data: str):
        """Add a new mission. Usage: !add_mission description | points"""
        try:
            description, points = [item.strip() for item in data.split('|')]
            points = int(points)
            add_mission(description, points)
            await ctx.send(f"Mission added: {description} - {points} points")
        except ValueError:
            await ctx.send("Invalid format. Use: !add_mission description | points")

    @commands.command()
    async def missions(self, ctx):
        """Display all available missions."""
        missions = get_all_missions()
        if not missions:
            await ctx.send("No missions available. Add some missions first!")
            return
        missions_text = "\n".join([f"{i+1}. {m['description']} - {m['points']} points" for i, m in enumerate(missions)])
        await ctx.send(f"Available Missions:\n{missions_text}")

    @commands.command()
    async def my_missions(self, ctx):
        """Check your completed missions."""
        user_missions = get_user_missions(ctx.author.id)
        if not user_missions:
            await ctx.send("You haven't completed any missions yet.")
            return
        missions_text = "\n".join([f"{m['description']} - {m['points']} points" for m in user_missions])
        await ctx.send(f"Your completed missions:\n{missions_text}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def complete_mission(self, ctx, user: discord.Member, mission_index: int):
        """Mark a mission as completed for a user."""
        missions = get_all_missions()
        if 0 <= mission_index < len(missions):
            mission = missions[mission_index]
            if complete_mission(user.id, mission):
                update_points(user.id, mission['points'])
                await ctx.send(f"{user.mention} has completed the mission: {mission['description']} and earned {mission['points']} points!")
            else:
                await ctx.send(f"{user.mention} has already completed this mission.")
        else:
            await ctx.send("Invalid mission index.")

async def setup(bot):
    await bot.add_cog(Missions(bot))
    print("Missions cog loaded")