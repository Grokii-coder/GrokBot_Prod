from discord.ext import commands
import discord

def whatIs(myObj):
  print(type(myObj))
  for stuff in dir(myObj):
    print(stuff)

def setup(paramBot):
  paramBot.add_cog(GrokBotListening(paramBot))

class GrokBotListening(commands.Cog):
  def __init__(self, paramBot):
    self.bot = paramBot
    
    from GrokBotClasses.GrokBot_bidding import GrokBot_bidding   
    self.guilds = {"Potatoville" : GrokBot_bidding()}
    self.guilds["Potatoville"].setBot(self.bot)
    self.guilds["Potatoville"].setChannel("inGame", 690269605524013127)
    self.guilds["Potatoville"].setChannel("Spam", 781591411094454273)
    self.guilds["Potatoville"].setChannel("Bids", 804445947433975818)
    self.guilds["Potatoville"].setChannel("History", 804445815124787292)    

    self.Monitor = {
      "inGame" : [
        #690269605524013127 #Spirit of Potato
        self.guilds["Potatoville"].getChannel("inGame")
        ]
      , "discordChannel" : [
        #804445947433975818 #Spirit of Potato
        self.guilds["Potatoville"].getChannel("Bids")
      ]}

  @commands.Cog.listener()
  async def on_message(self, message):
    import re

    #Check if the message was NOT made by the bot itself
    if message.author != self.bot.user:
      #Set channel name      
      if type(message.channel) is discord.channel.DMChannel:
        myChannel = "DM"
      else:
        myChannel = message.channel.name

      #Echo message and channel id
      myMsg = "{} ({}:{})".format(message.content, myChannel, message.channel.id, )
      #echo message
      print(myMsg)
      print(self.Monitor["inGame"])

      #Check if the message was made to SoP 'in-game-chat' channel id 690269605524013127
      if message.channel.id in self.Monitor["inGame"]:
        #Parse the name of the person saying the message
        pattern = "\*\*(.*) guild:\*\* (.*)"
        result = re.search(pattern, message.content)
        myGuildMate = result.group(1)
        myMessage = result.group(2)

        #Split message by space
        arrMsg = myMessage.split()
     
        #Create a original message object
        orgMessage = {"command" : None
                    , "guildmate" : myGuildMate
                    , "message" : myMessage
                    , 'bid' : None
                    , "channelName" : myChannel
                    , "channelID" : message.channel.id
        }

        #Check to see if this is a bid (one argument, and it is numeric)
        if len(arrMsg) == 1 and arrMsg[0].isdigit():
          print("Calling bid command for {}".format(self.guilds))
          orgMessage["bid"] = arrMsg[0]
          await self.guilds[message.guild.name].cmdBid(message, orgMessage)
        #Check to see if the first character starts with !
        elif myMessage[0] == '!':
          #Set the command name to lowercase and add it to the original message object
          myCommand = arrMsg[0].lower()
          orgMessage["command"] = myCommand
          print("myCommand is ({})".format(myCommand))

          #Check to see if the command is voice
          if myCommand == "!test":            
            print("Calling test command for {}".format(self.guilds))           
            await self.guilds[message.guild.name].cmdTest(message, orgMessage)

          #Check to see if the command is loot
          if myCommand == "!loot" and len(arrMsg) >= 3:
            print("Calling loot command for {}".format(self.guilds))
            await self.guilds[message.guild.name].cmdLoot(message, orgMessage) 
              
          elif myCommand == "!cancel":
            print("Calling cancel command for {}".format(self.guilds))
            await self.guilds[message.guild.name].cmdCancel(message, orgMessage) 

          elif myCommand == "!rollback":
            print("Calling rollback command for {}".format(self.guilds))
            await self.guilds[message.guild.name].cmdRollback(message, orgMessage)

          elif myCommand == "!close":            
            print("Calling close command for {}".format(self.guilds))
            await self.guilds[message.guild.name].cmdClose(message, orgMessage)
          
          elif myCommand == "!nondkp":
            print("Calling nondkp command for {}".format(self.guilds))
            await self.guilds[message.guild.name].cmdNonDkp(message, orgMessage)
            

