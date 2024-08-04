import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Cog setup
initial_extensions = ['cogs.ranking', 'cogs.quiz', 'cogs.missions', 'cogs.achievements']

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Connected to {len(bot.guilds)} guilds:')
    for guild in bot.guilds:
        print(f' - {guild.name} (id: {guild.id})')

@bot.event
async def setup_hook():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f'Loaded extension: {extension}')
        except Exception as e:
            print(f'Failed to load extension {extension}: {e}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use '!help' to see available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing required argument. Please check the command usage with '!help {ctx.command.name}'")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument provided. Please check the command usage.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the required permissions to use this command.")
    else:
        print(f"An error occurred: {type(error).__name__}: {str(error)}")
        await ctx.send(f"An error occurred: {type(error).__name__}")

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! Latency: {round(bot.latency * 1000)}ms')

@bot.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    try:
        await bot.reload_extension(f"cogs.{extension}")
        await ctx.send(f"The extension {extension} was reloaded successfully!")
    except commands.ExtensionError as e:
        await ctx.send(f"An error occurred while reloading {extension}: {e}")

if __name__ == "__main__":
    bot.run(TOKEN)