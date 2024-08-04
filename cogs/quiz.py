import discord
from discord.ext import commands
import asyncio
import random
from utils.database import add_question, get_all_questions, remove_question, update_points

class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.quiz_channel_id = None

    # ... (other methods remain the same)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def quiz(self, ctx, index: int = None):
        questions = get_all_questions()
        if not questions:
            await ctx.send("No questions available. Please add some questions first!")
            return

        if index is None:
            # If no index is provided, choose a random question
            question = random.choice(questions)
        elif 0 <= index < len(questions):
            question = questions[index]
        else:
            await ctx.send("Invalid question index.")
            return

        await ctx.send(f"Quiz time! Question: {question['question']}")
       
        def check(m):
            return m.channel == ctx.channel and m.content.lower() == question['answer'].lower()
       
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send(f"Time's up! The correct answer was {question['answer']}.")
        else:
            update_points(msg.author.id, question['points'])
            await ctx.send(f'{msg.author.mention} got it right! You earned {question["points"]} points.')

    @quiz.error
    async def quiz_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Starting a quiz with a random question. Use '!quiz <index>' to choose a specific question.")
            await self.quiz(ctx)

async def setup(bot):
    await bot.add_cog(Quiz(bot))
    print("Quiz cog loaded")