class Raid:
  def __init__(self):
    from classes.Bidding import Bidding
    self.bidding = Bidding()

    from classes.Listener import Listener
    self.listener = Listener()    

    self.tranServerToGuild = {
      "GrokBot Dev" : "Spirit of Potato",
      "Potatoville" : "Spirit of Potato"
      }
  
  async def cmdRaid(self, message, pSource):
    if pSource == "EQ":
      msgParsed = await self.listener.parseMessage(message)
      #Already know it is an officer, or they wouldn't have gotten here
      myOfficer = msgParsed["GuildMate"]
      
      #Already know message starts with !raid, trim that out
      myRaidArgument = msgParsed["Message"].replace("!raid ", "")
    else:
      #Only works from in-game for now...
      return
    
    #Possible raid commands:  start and end

    print("Officer ({}), RaidArgument ({})".format(myOfficer, myRaidArgument))
    
    if myRaidArgument == "start":
      self.raidStart()
    elif myRaidArgument == "end":
      self.raidEnd()
  
  #async def cmdRaid(self, message, pSource):
  #  pass

    

    #Get gui

