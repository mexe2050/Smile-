import discord
from discord.ext import commands
import asyncio
import random
from utils.database import add_question, get_all_questions, remove_question, update_points

class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_quizzes = set()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_quiz_question(self, ctx, *, data: str):
        """Add a new quiz question. Usage: !add_quiz_question question | answer | points"""
        parts = [part.strip() for part in data.split('|')]
        if len(parts) != 3:
            await ctx.send("Invalid format. Use: !add_quiz_question question | answer | points")
            return
        
        question, answer, points = parts
        try:
            points = int(points)
            add_question(question, answer, points)
            await ctx.send(f"Question added successfully: {question}")
        except ValueError:
            await ctx.send("Invalid points value. Please use a number.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def remove_quiz_question(self, ctx, index: int):
        """Remove a quiz question by index."""
        if remove_question(index - 1):
            await ctx.send(f"Question at index {index} removed successfully.")
        else:
            await ctx.send("Invalid index. No question removed.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def quiz(self, ctx):
        """Start a quiz with a random question."""
        if ctx.channel.id in self.active_quizzes:
            await ctx.send("A quiz is already active in this channel.")
            return

        questions = get_all_questions()
        if not questions:
            await ctx.send("No questions available. Please add some questions first!")
            return

        self.active_quizzes.add(ctx.channel.id)
        question = random.choice(questions)
        await ctx.send(f"Quiz time! Question: {question['question']}")
       
        def check(m):
            return m.channel == ctx.channel and not m.author.bot

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send(f"Time's up! The correct answer was: {question['answer']}")
        else:
            if msg.content.lower() == question['answer'].lower():
                update_points(msg.author.id, question['points'])
                await ctx.send(f'{msg.author.mention} got it right! You earned {question["points"]} points.')
            else:
                await ctx.send(f'Sorry, that\'s incorrect. The correct answer was: {question["answer"]}')

        self.active_quizzes.remove(ctx.channel.id)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def list_questions(self, ctx):
        """List all quiz questions."""
        questions = get_all_questions()
        if not questions:
            await ctx.send("There are no quiz questions available.")
            return

        question_list = "\n".join([f"{i+1}. {q['question']} (Answer: {q['answer']}, Points: {q['points']})" for i, q in enumerate(questions)])
        await ctx.send(f"Quiz Questions:\n{question_list}")

async def setup(bot):
    await bot.add_cog(Quiz(bot))
    print("Quiz cog loaded")