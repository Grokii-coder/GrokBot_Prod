
class Everquest:
  def __init__(self):
    self.guildDiscordToEQ = {
      "key1" : "Spirit of Potato",
      "key2" : "Value"
      }

  async def getEQGuildName(self, ctx):
    #Check if ctx object has a guild component
    if ctx.guild:
      myDiscordName = ctx.guild.name
    else:
      print("replitDB.getEQGuildName:  DM, not channel, return None")
      return None
    
    if myDiscordName in self.guildDiscordToEQ:
      return self.guildDiscordToEQ[myDiscordName]
    else:
      return ""

  
  async def parseGuildDump(self, pDump):
    import datetime
    print("Convert guild dump to dictionary")
    #Create dictionary for in-game guild dump data
    myData = {}
    
    #Split guild dump into lines    
    f = pDump.split('\\r\\n')

    #read in each line
    for line in f:
        #split line by tab
        items = line.split("\\t")
        
        #Check to see if line had 15 elements
        if len(items) == 15:
            #Get the information needed from the dump
            myName = items[0]
            myLevel =  items[1]
            myClass = items[2]
            myRank = items[3]                
            myLastOn = datetime.datetime.strptime(items[5], '%m/%d/%y')
            myToday = datetime.datetime.today()
            myDaysSinceLastOn = abs((myToday - myLastOn).days)
            myPublicNote = items[7]
            #Write the data to the myData dictionary
            myData[myName] = {
                "Level":myLevel,
                "Class":myClass,
                "Rank":myRank,
                "LastOn":str(myLastOn),
                "DaysSinceLastOn":myDaysSinceLastOn,
                "PublicNote":myPublicNote}
    return myData
  