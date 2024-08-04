import discord
from discord.ext import commands
from utils.database import get_user_achievements, add_achievement, update_points

class Achievements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.achievements = [
            {"id": 1, "name": "Chatterbox", "description": "Send 100 messages", "requirement": 100},
            {"id": 2, "name": "Verbose", "description": "Send 150 messages", "requirement": 150},
            {"id": 3, "name": "Wordsmith", "description": "Send 200 messages", "requirement": 200},
            {"id": 4, "name": "Communicator", "description": "Send 250 messages", "requirement": 250},
            {"id": 5, "name": "Orator", "description": "Send 300 messages", "requirement": 300},
            {"id": 6, "name": "Storyteller", "description": "Send 350 messages", "requirement": 350},
            {"id": 7, "name": "Narrator", "description": "Send 400 messages", "requirement": 400},
            {"id": 8, "name": "Articulate", "description": "Send 450 messages", "requirement": 450},
            {"id": 9, "name": "Eloquent", "description": "Send 500 messages", "requirement": 500},
            {"id": 10, "name": "Fluent", "description": "Send 550 messages", "requirement": 550},
            {"id": 11, "name": "Expressive", "description": "Send 600 messages", "requirement": 600},
            {"id": 12, "name": "Loquacious", "description": "Send 650 messages", "requirement": 650},
            {"id": 13, "name": "Voluble", "description": "Send 700 messages", "requirement": 700},
            {"id": 14, "name": "Garrulous", "description": "Send 750 messages", "requirement": 750},
            {"id": 15, "name": "Talkative", "description": "Send 800 messages", "requirement": 800},
            {"id": 16, "name": "Chatty", "description": "Send 850 messages", "requirement": 850},
            {"id": 17, "name": "Verbose Master", "description": "Send 900 messages", "requirement": 900},
            {"id": 18, "name": "Prolific Speaker", "description": "Send 950 messages", "requirement": 950},
            {"id": 19, "name": "Chatterbox Supreme", "description": "Send 1000 messages", "requirement": 1000},
            {"id": 20, "name": "Legendary Communicator", "description": "Send 1050 messages", "requirement": 1050},
        ]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = message.author.id
        user_achievements = get_user_achievements(user_id)
        user_message_count = len([m for m in user_achievements if m['type'] == 'message'])

        for achievement in self.achievements:
            if user_message_count + 1 >= achievement['requirement'] and achievement['id'] not in [a['id'] for a in user_achievements]:
                add_achievement(user_id, achievement['id'], 'message')
                update_points(user_id, 30)
                await message.channel.send(f"🎉 Congratulations {message.author.mention}! You've earned the '{achievement['name']}' achievement and gained 30 points!")

    @commands.command()
    async def achievements(self, ctx):
        """Display user's achievements."""
        user_achievements = get_user_achievements(ctx.author.id)
        user_achievement_ids = [a['id'] for a in user_achievements]

        achieved = "\n".join([f"✅ {a['name']}: {a['description']}" for a in self.achievements if a['id'] in user_achievement_ids])
        not_achieved = "\n".join([f"❌ {a['name']}: {a['description']}" for a in self.achievements if a['id'] not in user_achievement_ids])

        embed = discord.Embed(title=f"{ctx.author.name}'s Achievements", color=discord.Color.blue())
        embed.add_field(name="Achieved", value=achieved or "None", inline=False)
        embed.add_field(name="Not Achieved", value=not_achieved or "All achievements completed!", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Achievements(bot))
    print("Achievements cog loaded")