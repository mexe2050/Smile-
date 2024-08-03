import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MONGO_URI = os.getenv('MONGO_URI')

print(f"Token loaded: {'YES' if TOKEN else 'NO'}")
print(f"MongoDB URI loaded: {'YES' if MONGO_URI else 'NO'}")

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Cog setup
initial_extensions = ['cogs.ranking', 'cogs.quiz', 'cogs.missions']

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Connected to {len(bot.guilds)} guilds:')
    for guild in bot.guilds:
        print(f' - {guild.name} (id: {guild.id})')

@bot.event
async def setup_hook():
    for extension in initial_extensions:
        if extension not in bot.extensions:
            try:
                await bot.load_extension(extension)
                print(f'Loaded extension: {extension}')
            except Exception as e:
                print(f'Failed to load extension {extension}: {e}')

@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    try:
        await bot.reload_extension(f"cogs.{extension}")
        await ctx.send(f"The extension {extension} was reloaded!")
    except commands.ExtensionError as e:
        await ctx.send(f"Error reloading {extension}: {e}")

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! Latency: {round(bot.latency * 1000)}ms')

if __name__ == "__main__":
    bot.run(TOKEN)