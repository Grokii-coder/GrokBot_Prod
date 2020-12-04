
class replitDB:
  def __init__(self):
    self.tranServerToGuild = {
      "GrokBot Dev" : "Spirit of Potato",
      "Potatoville" : "Spirit of Potato"
      }

  async def getEQGuildName(self, ctx):
    #Check if ctx object has a guild component
    if ctx.guild:
      myDiscordName = ctx.guild.name
    else:
      print("replitDB.getEQGuildName:  DM, not channel, return None")
      return None
    
    #Check if discrod name defined in this class
    if myDiscordName in self.tranServerToGuild:
      #Return Everquest Name
      return self.tranServerToGuild[myDiscordName]
    else:
      #Return Nothing
      print("replitDB.getEQGuildName:  {} not defined in replitDB".format(myDiscordName))
      return None

  async def listGuildDumps(self, ctx):  
    from replit import db
    #Get EQ Guild Name from discord Server Name
    eqGuild = await self.getEQGuildName(ctx)

    if eqGuild is None:
      return None
    else:
      #default myDumpKeys to an empty dictionary
      myDumpKeys = []
      #Check if eqGuild in db
      if eqGuild in db:
        #check if guild property in db
        if "GuildDumps" in db[eqGuild]:
          #Get guild property
          myDumpKeys = db[eqGuild]["GuildDumps"].keys()
      else:
        #eqGuild not in DB, add it
        db[eqGuild] = {}
      
      #return myGuildProperty
      return myDumpKeys

  async def getGuildProperty(self, ctx, pProperty):  
    from replit import db
    #Get EQ Guild Name from discord Server Name
    eqGuild = await self.getEQGuildName(ctx)

    if eqGuild is None:
      return None
    else:
      #default myGuildProperty to an empty dictionary
      myGuildProperty = {}
      #Check if eqGuild in db
      if eqGuild in db:
        #check if guild property in db
        if pProperty in db[eqGuild]:
          #Get guild property
          myGuildProperty = db[eqGuild][pProperty]
      else:
        #eqGuild not in DB, add it
        db[eqGuild] = {}
      
      #return myGuildProperty
      return myGuildProperty

  async def setGuildProperty(self, ctx, pProperty, pData):  
    from replit import db
    
    #Get EQ Guild Name from discord Server Name
    eqGuild = await self.getEQGuildName(ctx)

    if eqGuild is None:      
      return 0
    else:
      #Set myGuildData to the current data from the DB
      myGuildData = db[eqGuild]
      #Update myGuildData with the new data passed
      myGuildData[pProperty] = pData
      #Write the combined date to the DB
      db[eqGuild] = myGuildData

      #return 1 for set success
      return 1

  async def wipeGuild(self, ctx):
    print("Starting wipeGuild")
    from replit import db
    
    #Get EQ Guild Name from discord Server Name
    eqGuild = await self.getEQGuildName(ctx)

    if eqGuild is None:
      print("Its none:  " + eqGuild)      
      return 0
    else:
      print("Deleting guild data " + eqGuild)      
      db[eqGuild] = {}

      #return 1 for set success
      return 1