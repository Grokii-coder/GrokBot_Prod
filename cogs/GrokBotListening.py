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
    from classes.Role import Role 
    from classes.Listener import Listener
    self.role = Role()
    self.Listener = Listener()    

    from classes.Raid import Raid

    self.guilds = {"Potatoville" : Raid()}
    self.guilds["Potatoville"].bidding.setBot(self.bot)
    self.guilds["Potatoville"].bidding.setChannel("inGame", 690269605524013127)
    self.guilds["Potatoville"].bidding.setChannel("Spam", 781591411094454273)
    self.guilds["Potatoville"].bidding.setChannel("Bids", 804445947433975818)
    self.guilds["Potatoville"].bidding.setChannel("History", 804445815124787292)    

    self.Monitor = {
      "inGame" : [
        #690269605524013127 #Spirit of Potato
        self.guilds["Potatoville"].bidding.getChannel("inGame")
        ]
      , "discordChannel" : [
        #804445947433975818 #Spirit of Potato
        self.guilds["Potatoville"].bidding.getChannel("Bids")
      ]}

  @commands.Cog.listener()
  async def on_message(self, message):


    #Check if the message was NOT made by the bot itself
    #Check if this message is from Nazi Bot
    if message.author.name == "Grammar Nazi Bot":
      import random
      import asyncio

      myComment = [
      "You sit on a throne of lies!"
      ,"Would you like to sleep with the fishes?"
      ,"So very interesting, tell me moar?"
      ,"Well well well, what do we have here?"
      ,"Zombies eat brains, don't worry your safe"
      ,"Better grab my dumbrella its really stupid outside today"
      ]

      await message.channel.send(random.choice(myComment), delete_after=7)
      await asyncio.sleep(7)
      message.delete
    elif message.author != self.bot.user:
      #Set channel name      
      if type(message.channel) is discord.channel.DMChannel:
        myChannel = "DM"
      else:
        myChannel = message.channel.name

      #Echo message and meta data of message
      myMsg = message.content
      metaMsg = "({}:{}:{}:{})".format(message.guild.name,message.author,myChannel,message.channel.id)

      #echo message
      print(myMsg)
      print(metaMsg)
      
      #Check if the message was made to SoP 'in-game-chat' channel id 690269605524013127
      if message.channel.id in self.Monitor["inGame"]:
        msgParsed = await self.Listener.parseMessage(message)
        myGuildMate = msgParsed["GuildMate"]
        myMessage = msgParsed["Message"]

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
          await self.guilds[message.guild.name].bidding.cmdBid(message, orgMessage)
        #Check to see if the first character starts with !
        elif myMessage[0] == '!':
          #Set the command name to lowercase and add it to the original message object
          myCommand = arrMsg[0].lower()
          orgMessage["command"] = myCommand
          print("myCommand is ({})".format(myCommand))

          #Check for test command
          if myCommand == "!test":    
            print("Calling test command for {}".format(self.guilds))           
            await self.guilds[message.guild.name].bidding.cmdTest(message, orgMessage)
          #Check for nondkp command
          elif myCommand == "!nondkp":
            print("Calling nondkp command for {}".format(self.guilds))
            await self.guilds[message.guild.name].bidding.cmdNonDkp(message, orgMessage)

          #Check if role is leadership and if so check for elevated commands
          elif "leadership" in await self.role.getCharactersMageloRoles(message, myGuildMate):
            #Check for raid command
            if myCommand == "!raid":
              print("Calling loot command for {}".format(self.guilds))
              await self.guilds[message.guild.name].cmdRaid(message, "EQ") 

            #Check to see if the command is loot
            if myCommand == "!loot" and len(arrMsg) >= 3:
              print("Calling loot command for {}".format(self.guilds))
              await self.guilds[message.guild.name].bidding.cmdLoot(message, orgMessage) 
                
            elif myCommand == "!cancel":
              print("Calling cancel command for {}".format(self.guilds))
              await self.guilds[message.guild.name].bidding.cmdCancel(message, orgMessage) 

            elif myCommand == "!rollback":
              print("Calling rollback command for {}".format(self.guilds))
              await self.guilds[message.guild.name].bidding.cmdRollback(message, orgMessage)

            elif myCommand == "!close":            
              print("Calling close command for {}".format(self.guilds))
              await self.guilds[message.guild.name].bidding.cmdClose(message, orgMessage)
          

            

