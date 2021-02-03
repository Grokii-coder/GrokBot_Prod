import os
import keep_alive
import discord
#import typing 

from discord.ext import commands 

intents = discord.Intents.default()
intents.members = True

#URL for server admins to add the bot:
#https://discordapp.com/oauth2/authorize?client_id=778661268939735060&scope=bot

client = commands.Bot(command_prefix = '?', intents=intents)

@client.event 
async def on_ready():
    print('Bot ready')

#Development function to help get properties/methods of objects
async def whatIs(myObj):
  for stuff in dir(myObj):
    print(stuff)

#Get token from .env file
TOKEN = os.getenv('DISCORD_TOKEN')

#Run the keepalive script so it can be pinged every 30 minutes and kept alive
keep_alive.keep_alive()

#Load cogs
client.load_extension('cogs.GrokBotCommands')
client.load_extension('cogs.GrokBotListening')
#start the bot
client.run(TOKEN)