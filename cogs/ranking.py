import discord
from discord.ext import commands
from utils.database import get_user_points, get_top_users

class Ranking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rank(self, ctx):
        print(f"Rank command called by {ctx.author} (ID: {ctx.author.id})")
        points, rank = get_user_points(ctx.author.id)
        print(f"Retrieved points: {points}, rank: {rank}")
        await ctx.send(f"{ctx.author.mention}, you have {points} points and are ranked #{rank}.")
        print("Rank command response sent")

    @commands.command()
    async def top10(self, ctx):
        print(f"Top10 command called by {ctx.author}")
        top_users = get_top_users(10)
        if not top_users:
            await ctx.send("No users ranked yet.")
            return
        top_10 = "\n".join([f"{i+1}. <@{user['_id']}>: {user['points']} points" for i, user in enumerate(top_users)])
        await ctx.send(f"Top 10 Users:\n{top_10}")

async def setup(bot):
    await bot.add_cog(Ranking(bot))
    print("Ranking cog loaded")