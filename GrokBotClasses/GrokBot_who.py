class GrokBot_who():
  def __init__(self):
    self.Msg = ""

  async def getWho(self, ctx, pName):
    await self.processWho(ctx, pName)
    if len(self.Msg) > 0:
      return(self.Msg)
    else:
      return("Empty Msg")

  async def processWho(self, ctx, pName):
    print("entering who") 
    print(pName)
    
    #Get database object instanced
    from classes.replitDB import replitDB
    repDB = replitDB()

    #Get links and newest guild dump from db
    links = await repDB.getGuildProperty(ctx, "Links")
    newestDump = await repDB.getGuildProperty(ctx, "NewestGuildDump")

    #Sanitize pName
    pName = pName.replace('<@!', '').replace('>', '')

    #Variables to store public note and member object when found
    myPublicNote = ""
    myMember = None

    #Iterate through the most recent guild dump
    for aChar in sorted(newestDump["Data"]):
      #Check if the character name matches
      if aChar.lower() == pName.lower():
        #Match found, set myPublicNote and exit for loop
        myPublicNote = newestDump["Data"][aChar]["PublicNote"]
        break
      
      #Check if the public note matches
      if newestDump["Data"][aChar]["PublicNote"].lower() == pName.lower():
        #Match found, set myPublicNote and exit for loop
        myPublicNote = newestDump["Data"][aChar]["PublicNote"]
        break

    #Iterate through links to try to set member object
    for aLink in links:
      print(pName)
      print("{}: {}".format(aLink["DiscordMemberID"], aLink["PublicNote"]))
      #Check if pName equals this linked ID or if the publicNote matches
      if str(pName) == str(aLink["DiscordMemberID"]) or myPublicNote == aLink["PublicNote"]:
        #Match found, get public note information
        myPublicNote = aLink["PublicNote"]
        myMember = await ctx.guild.fetch_member(aLink["DiscordMemberID"])
        break

    #Check if a match was found
    if len(myPublicNote) == 0:
      #No match found, throw error
      print("Couldn't find a match for {} by character name, public note, or discordID".format(pName))
    else:           
      #Check if member object has a value
      if myMember is None:
        #No member object, format output without link
        myMsg = []
        await self.outputwhoFlag(None, None, None, myPublicNote, newestDump, myMsg)
        self.Msg = myMsg[0]
      else:
        #Member object exists, format output with link
        myMsg = []
        await self.outputwhoFlag(myMember.mention, myMember, myMember.nick, myPublicNote, newestDump, myMsg)
        self.Msg = myMsg[0]

  async def outputwho(self, pMention, pName, pNick, pPublicNote, pDump, pMsg):
    #Check to see if myPublicNote is in pDump   
    print("entering ouutputwho") 
    myMsg = ""    
    for aChar in sorted(pDump["Data"]):
      if pDump["Data"][aChar]["PublicNote"].lower() == pPublicNote.lower():
        myLevel = pDump["Data"][aChar]["Level"]
        myClass = pDump["Data"][aChar]["Class"]        
        
        myMsg += "{}:  {} {}\r".format(aChar, myLevel, myClass)

    #Check if there is a nickname
    if pNick is None:
      myHeader = "Discord name {}\r\r".format(pName)      
    else:
      myHeader = "Discord name {}\rDiscord nickname {}\r\r".format(pName, pNick)  
    
    myMsg = myHeader + myMsg

    pMsg.append(myMsg)

  async def outputwhoAA(self, pName, pNick, pPublicNote, pDump, pMsg):
    #Check to see if myPublicNote is in pDump
    myTotal = 0
    myMsg = ""    
    for aChar in sorted(pDump["Data"]):
      if pDump["Data"][aChar]["PublicNote"].lower() == pPublicNote.lower():
        myLevel = pDump["Data"][aChar]["Level"]
        myClass = pDump["Data"][aChar]["Class"]
        myCount = pDump["Data"][aChar]["aaTotal"]

        newTotal = myTotal + myCount
        print("Total {} plus {} equals {}".format(myTotal, myCount, newTotal))
        myTotal += myCount

        
        myMsg += "{} (aa{}):  {} {}\r".format(aChar, myCount, myLevel, myClass)

    #Check if there is a nickname
    if pNick is None:
      myHeader = "Discord name {} (aa{})\r\r".format(pName, myTotal)
    else:
      myHeader = "Discord name {} (aa{})\rDiscord nickname {}\r\r".format(pName, myTotal, pNick)  
    
    myMsg = myHeader + myMsg

    pMsg.append(myMsg)

  async def outputwhoFlag(self, pMention, pName, pNick, pPublicNote, pDump, pMsg):
    #Check to see if myPublicNote is in pDump
    myTotal = 0
    myMsg = ""    
    for aChar in sorted(pDump["Data"]):
      if pDump["Data"][aChar]["PublicNote"].lower() == pPublicNote.lower():
        myLevel = pDump["Data"][aChar]["Level"]
        myClass = pDump["Data"][aChar]["Class"]

        if "ProgressionStatus" in pDump["Data"][aChar]:
          myStatus = pDump["Data"][aChar]["ProgressionStatus"]
        else:
          myStatus = pDump["Data"][aChar]["MageloStatus"]
        
        if myStatus == 'TimeFlagged':
          myTotal = myTotal + 1

        myMsg += "{} ({}):  {} {}\r".format(aChar, myStatus, myLevel, myClass)

    #Check if there is a nickname
    if pName is None:
      myHeader = "Discord name {} ({} time flagged)\r\r".format("<<Need to link>>", myTotal)
    elif pNick is None:
      myHeader = "Discord name {} ({} time flagged)\r\r".format(pMention, myTotal, pNick)  
    else:
      myHeader = "Discord name {} ({} time flagged)\rDiscord without nickname {}\r\r".format(pMention, myTotal, pName)  
    
    myMsg = myHeader + myMsg

    pMsg.append(myMsg)         

  async def getStats(self, ctx):
    #Get most recent guild dump and linked accounts from replitDB
    from classes.replitDB import replitDB
    repDB = replitDB()
    links = await repDB.getGuildProperty(ctx, "Links")
    newestDump = await repDB.getGuildProperty(ctx, "NewestGuildDump")

    #Calculate Total characters, last 30 days, 30-90 days, 90-365, 365+
    myTotal = 0
    under30 = 0
    from30to90 = 0
    from90to365 = 0
    over365 = 0

    #Get list of activity for a specific public note
    playerActive90 = {}

    #Make a list of unique PublicNotes
    uniquePublicNotes = {}

    #Loop through newestDump and get calculate data
    for aChar in newestDump["Data"]:
      #increment the total count
      myTotal = myTotal + 1

      #Get days since last logon      
      myDays = newestDump["Data"][aChar]["DaysSinceLastLogin"]
      myPublicNote = newestDump["Data"][aChar]["PublicNote"]

      #Check if public note already in uniquePublicNotes
      if myPublicNote in uniquePublicNotes:
        #Append to uniquePublicNotes
        uniquePublicNotes[myPublicNote].append(aChar)
      else:
        #Add new to uniquePublicNotes
        uniquePublicNotes[myPublicNote] = [aChar]        

      #Series of if statements for different ranges
      if myDays <= 30:        
        #30 days or less
        under30 = under30+1
        #Add/Count in playerActive90
        if myPublicNote in playerActive90:
          #Increment current counter
          playerActive90[myPublicNote] = playerActive90[myPublicNote] + 1
        else:
          #add entry with counter 1
          playerActive90[myPublicNote] = 1
      elif myDays > 30 and myDays <= 90:
        #30-90 days
        from30to90 = from30to90+1
        #Add/Count in playerActive90
        if myPublicNote in playerActive90:
          #Increment current counter
          playerActive90[myPublicNote] = playerActive90[myPublicNote] + 1
        else:
          #add entry with counter 1
          playerActive90[myPublicNote] = 1
      elif myDays > 90 and myDays <= 365:
        #90 days to a year
        from90to365 = from90to365+1
      elif myDays > 365:
        #Over a year
        over365 = over365+1

    myMsg = "Total characters:  {}\r".format(myTotal)
    myMsg += "  30 days or less:  {}\r".format(under30)
    myMsg += "  30 days to 90 days:  {}\r".format(from30to90)
    myMsg += "  90 days to a year:  {}\r".format(from90to365)
    myMsg += "  More than a year:  {}\r".format(over365)


    myActive = ""
    myInactive = ""
    myNoLinkActive = ""
    myNoLinkInActive = ""

    #Loop through uniquePublicNotes
    for aPlayer in sorted(uniquePublicNotes):
      
      #Check if this player has a link
      haveLink = 0
      for aLink in links:
        if aLink["PublicNote"] == aPlayer:
          haveLink = 1
          break

      #Get how many active characters this player has:
      myActiveChar = 0
      if aPlayer in playerActive90:
        myActiveChar = playerActive90[aPlayer]

      #Check if this player has more than three active characters
      if myActiveChar >= 3:
        #More than 3 active, add to myActive output
        myActive += "{}: {}\r".format(aPlayer, myActiveChar)
        #Check if this player has a link
        if haveLink == 0:
          #No link, add it to the NoLinkActive output
          myNoLinkActive += "{}: {}\r".format(aPlayer, myActiveChar)

          #Loop through each character
          for loopChar in uniquePublicNotes[aPlayer]:
            #Add them to the NoLinkActive output
            myNoLinkActive += " | {}".format(loopChar)
          myNoLinkActive += "\r"

      else:
        #Add to inActive otuput
        myInactive += "{}: {}\r".format(aPlayer, myActiveChar)
        #Check if this player has a link
        if haveLink == 0:
          #No link, add it to the NoLinkActive outout
          myNoLinkInActive += "{}: {}\r".format(aPlayer, myActiveChar)  

          #Loop through each character
          for loopChar in uniquePublicNotes[aPlayer]:
            #Add them to the NoLinkActive output
            myNoLinkInActive += " | {}".format(loopChar)
          myNoLinkInActive += "\r"                

    #Add sections for active/inactve players and nolink active/inactive players.
    myMsg += "\rActive Players:\r" + myActive
    myMsg += "\rInActive Players:\r" + myInactive
    myMsg += "\rNoLink Active Players:\r" + myNoLinkActive
    myMsg += "\rNoLink InActive Players:\r" + myNoLinkInActive

    #Todo
    #  1) get PopFlag Status, output any TaterTot without 3 active time flagged
    #  2) get BackedPotato to move up to Taters or TaterTots
    #  3) get Taters or TaterTots to move up to BackedPotato
    #  4) Discord members not linked to a public note
    #  5) List each character with blank PublicNote with days since last login

    #await ctx.message.author.send(myMsg)
    await self.largeDM(ctx, myMsg)