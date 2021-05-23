import discord
from discord.ext import commands
import os
intents = discord.Intents.default()

bot = commands.Bot(command_prefix = ".", intents = intents)

@bot.event
async def on_ready():
    print("Bot is ready")


#Load cog command
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

#Unload cog command
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

#Reload specific cog
@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'cogs.{extension}')

  

@bot.command(aliases=['r'])
async def rel(ctx, extension="connectfour"):
    bot.reload_extension(f'cogs.{extension}')


bot.load_extension(f'cogs.connectfour')



bot.run(TOKEN)
