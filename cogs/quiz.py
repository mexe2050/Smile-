import discord
from discord.ext import commands
import asyncio
from utils.database import add_question, get_all_questions, remove_question, update_points

class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.quiz_channel_id = None

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_quiz_channel(self, ctx, channel: discord.TextChannel):
        self.quiz_channel_id = channel.id
        await ctx.send(f"Quiz channel set to {channel.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_question(self, ctx, question: str, answer: str, points: int):
        add_question(question, answer, points)
        await ctx.send(f"Question added: {question} (Answer: {answer}, Points: {points})")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def remove_question(self, ctx, index: int):
        if remove_question(index):
            await ctx.send(f"Removed question at index {index}")
        else:
            await ctx.send("Invalid question index.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def list_questions(self, ctx):
        questions = get_all_questions()
        if not questions:
            await ctx.send("No questions available.")
            return
        questions_list = "\n".join([f"{i}. {q['question']} (Answer: {q['answer']}, Points: {q['points']})" for i, q in enumerate(questions)])
        await ctx.send(f"Questions:\n{questions_list}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def quiz(self, ctx, index: int):
        questions = get_all_questions()
        if 0 <= index < len(questions):
            question = questions[index]
            await ctx.send(f"Quiz time! Question: {question['question']}")
           
            def check(m):
                return m.channel == ctx.channel and m.content.lower() == quest