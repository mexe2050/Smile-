import discord
from discord.ext import commands
import asyncio
import random
from utils.database import add_question, get_all_questions, remove_question, update_points

class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_quiz_question(self, ctx, *, data: str):
        """Add a new quiz question. Usage: !add_quiz_question question | answer | points"""
        try:
            question, answer, points = [item.strip() for item in data.split('|')]
            points = int(points)
            add_question(question, answer, points)
            await ctx.send(f"Question added successfully: {question}")
        except ValueError:
            await ctx.send("Invalid format. Use: !add_quiz_question question | answer | points")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def remove_quiz_question(self, ctx, index: int):
        """Remove a quiz question by index."""
        if remove_question(index):
            await ctx.send(f"Question at index {index} removed successfully.")
        else:
            await ctx.send("Invalid index. No question removed.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def quiz(self, ctx, index: int = None):
        """Start a quiz with a specific question or a random one."""
        questions = get_all_questions()
        if not questions:
            await ctx.send("No questions available. Please add some questions first!")
            return

        if index is None:
            question = random.choice(questions)
        elif 0 <= index < len(questions):
            question = questions[index]
        else:
            await ctx.send("Invalid question index.")
            return

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

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def list_questions(self, ctx):
        """List all quiz questions."""
        questions = get_all_questions()
        if not questions:
            await ctx.send("There are no quiz questions available.")
            return

        question_list = "\n".join([f"{i}. {q['question']} (Answer: {q['answer']}, Points: {q['points']})" for i, q in enumerate(questions)])
        await ctx.send(f"Quiz Questions:\n{question_list}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Command not found. Use '!help' to see available commands.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument. Please check the command usage with '!help {ctx.command.name}'")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument provided. Please check the command usage.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the required permissions to use this command.")
        else:
            await ctx.send(f"An error occurred: {type(error).__name__}")
            print(f"An error occurred in {ctx.command.name}: {str(error)}")

async def setup(bot):
    await bot.add_cog(Quiz(bot))
    print("Quiz cog loaded")