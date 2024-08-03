import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncio

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Load cogs
async def load_extensions():
    await bot.load_extension("cogs.ranking")
    await bot.load_extension("cogs.quiz")
    await bot.load_extension("cogs.missions")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await load_extensions()

# Run the bot
async def main():
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())