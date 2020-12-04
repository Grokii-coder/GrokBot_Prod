import os
import keep_alive
#import discord
#import typing

from discord.ext import commands 

#URL for server admins to add the bot:
#https://discordapp.com/oauth2/authorize?client_id=778661268939735060&scope=bot

client = commands.Bot(command_prefix = '?')

@client.event 
async def on_ready():
    print('Bot ready')

#Development function to help get properties/methods of objects
async def whatIs(myObj):
  for stuff in dir(myObj):
    print(stuff)

@client.event
async def on_message(message):
  if 1==0:
    print("Message received: " + str(message.content))
    print("Message author:  " + str(message.author))
    print("Client User:  " + str(client.user))
    print("")

  if message.author != client.user:
  #if str(message.author) != str(client.user):
  #if not message.author.bot:
    if 'Hellosdfsdf'.upper() in message.content.lower():
      await message.channel.send('Say hello!')

  await client.process_commands(message)



#Get token from .env file
TOKEN = os.getenv('DISCORD_TOKEN')

#Run the keepalive script so it can be pinged every 30 minutes and kept alive
keep_alive.keep_alive()

#Load cogs
client.load_extension('cogs.GrokBotCommands')
#start the bot
client.run(TOKEN)