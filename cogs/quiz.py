import discord
from discord.ext import commands
import json
from utils.database import update_points

class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.quiz_channel_id = None
        self.questions = []
        self.load_config()

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                self.quiz_channel_id = config.get('quiz_channel_id')
                self.questions = config.get('questions', [])
        except FileNotFoundError:
            pass

    def save_config(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
        config['quiz_channel_id'] = self.quiz_channel_id
        config['questions'] = self.questions
        with open('config.json', 'w') as f:
            json.dump(config, f)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_quiz_channel(self, ctx, channel: discord.TextChannel):
        self.quiz_channel_id = channel.id
        self.save_config()
        await ctx.send(f"Quiz channel set to {channel.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_question(self, ctx, question: str, answer: str, points: int):
        self.questions.append({"question": question, "answer": answer, "points": points})
        self.save_config()
        await ctx.send(f"Question added: {question} (Answer: {answer}, Points: {points})")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def remove_question(self, ctx, index: int):
        if 0 <= index < len(self.questions):
            removed = self.questions.pop(index)
            self.save_config()
            await ctx.send(f"Removed question: {removed['question']}")
        else:
            await ctx.send("Invalid question index.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def list_questions(self, ctx):
        if not self.questions:
            await ctx.send("No questions available.")
            return
        questions_list = "\n".join([f"{i}. {q['question']} (Answer: {q['answer']}, Points: {q['points']})" for i, q in enumerate(self.questions)])
        await ctx.send(f"Questions:\n{questions_list}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def quiz(self, ctx, index: int):
        if ctx.channel.id != self.quiz_channel_id:
            await ctx.send("This command can only be used in the designated quiz channel.")
            return

        if 0 <= index < len(self.questions):
            question = self.questions[index]
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
        else:
            await ctx.send("Invalid question index.")

async def setup(bot):
    await bot.add_cog(Quiz(bot))