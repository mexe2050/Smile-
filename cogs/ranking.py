from discord.ext import commands
from utils.database import get_user_points, get_top_users

class Ranking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rank(self, ctx):
        points, rank = get_user_points(ctx.author.id)
        await ctx.send(f"{ctx.author.mention}, you have {points} points and are ranked #{rank}.")

    @commands.command()
    async def top10(self, ctx):
        top_users = get_top_users(10)
        if not top_users:
            await ctx.send("No users ranked yet.")
            return
        top_10 = "\n".join([f"{i+1}. <@{id}>: {points} points" for i, (id, points) in enumerate(top_users)])
        await ctx.send(f"Top 10 Users:\n{top_10}")

async def setup(bot):
    await bot.add_cog(Ranking(bot))