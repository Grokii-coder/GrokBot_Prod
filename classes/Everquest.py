
class Everquest:
  def __init__(self):
    self.guildDiscordToEQ = {
      "key1" : "Spirit of Potato",
      "key2" : "Value"
      }
    self.empKey = {
      19716 : "Zazuzh's Idol"
      ,19717 : "Zherozsh's Ring"
      ,19718 : "Ssraeshzian Insignia"
      ,17118 : "Taskmaster's Pouch"
      ,19719 : "Ring of the Shissar"
    }

    self.VTKey = {
      22186 : "Lucid Shard (Dat) Fungus Grove"
      ,22190 : "Lucid Shard (Dax) Akheva Ruins"
      ,22185 : "Lucid Shard (Kel) The Grey"
      ,22194 : "Lucid Shard (Kelera) Sanctus Seru or Katta"
      ,22191 : "Lucid Shard (Lor) Dawnshroud Peaks"
      ,22188 : "Lucid Shard (Raf) The Deep"
      ,22187 : "Lucid Shard (Set) The Scarlet Desert"
      ,22192 : "Lucid Shard (Tak) Maiden's Eye"
      ,22193 : "Lucid Shard (Ved) Acrylia Cavern"
      ,22189 : "Lucid Shard (Vin) Ssraeshza Temple"
      ,17323 : "Shadowed Scepter Frame"
      ,9410 : "Planes Rift"
      ,22196 : "Glowing Orb of Luclinite"
      ,22198 : "The Scepter of Shadows"
      ,17324 : "Unadorned Scepter of Shadows"
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



  async def parseSpellBook(self, pDump):
    #Create dictionary for in-game guild dump data
    myData = []
    
    #Split guild dump into lines    
    f = pDump.split('\\r\\n')

    #read in each line
    for line in f:
      #split line by tab
      items = line.split("\\t")

      #Check to see if line had 2 elements
      if len(items) == 2:
        myLevel = items[0]
        myName = items[1]

        #Print out spellbook
        #print("Level ({}) Name ({})".format(myLevel, myName))

        #Add spellname to myData
        myData.append(myName)

    return myData        


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

  async def parseRaidDump(self, pDump):    
    #Create dictionary for in-game guild dump data
    myData = {}
    
    #Split raid dump into lines    
    f = pDump.split('\\r\\n')    

    #read in each line
    for line in f:
      #split line by tab
      items = line.split("\\t")

      #Check to see if line has 6 elements
      if len(items) == 6:
        #Get the information needed from the dump
        #1	Grokii	65	Shadow Knight	Raid Leader	
        myGroup = items[0]
        myName =  items[1]
        myLevel = items[2]
        myClass = items[3]
        myRole = items[4]
        #Write the data to the myData dictionary
        myData[myName] = {
            "Group":myGroup,
            "Name":myName,
            "Level":myLevel,
            "Class":myClass,
            "Role":myRole}
    
    #Reture dictionary with the data
    return myData  