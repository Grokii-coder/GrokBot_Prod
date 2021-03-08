class Flags:
  def __init__(self):
    self.managed = {"Taters" : None
                , "TaterTots" : None
                , "Baked Potato" : None
                , "Lone Potato" : None
                , "Spud Buds" : None
                } 


  async def dumpFilterForPublicNote(self, pChars, pPublicNotes):
    
    #Make a copy of pChars["Data"]
    myCopy = pChars["Data"].copy()

    #Iterate over the copy so the original can be modified
    for aChar in myCopy:
      myPublicNote = pChars["Data"][aChar]["PublicNote"]

      if myPublicNote in pPublicNotes:
        pass
      else:
        pChars["Data"].pop(aChar)

  async def getGuildDump(self, ctx):
    from classes.replitDB import replitDB
    repDB = replitDB()
          
    newestDump = await repDB.getGuildProperty(ctx, "NewestGuildDump")        
    if newestDump is None:
      myOutput = "No guild dump avaialble, is this a DM channel?"
      print(myOutput)
      return myOutput
    else:
      return newestDump

  async def loopTopTen(self, pChars, pDays, pWho): 
    dicTally = {}    
    print("LoopTopTen Start")
    
    #iterate through each character in the dump
    for aChar in pChars["Data"]:
      #Check to see if this character has logged in since pDays
      if int(pChars["Data"][aChar]["DaysSinceLastLogin"]) <= pDays:      
        #Check to see if the character has a PoP flagging dictionary
        if "PoPFlagsCanDo" in pChars["Data"][aChar]:
          #Check to see if they have done at least hedge pre flag
          if not "PreFlag Hedge" in pChars["Data"][aChar]["PoPFlagsCanDo"]:
            #Iterate through this character's flags
            for aFlag in pChars["Data"][aChar]["PoPFlagsCanDo"]:
              if 'Flag' in aFlag or 'ZoneInto' in aFlag:
                #Skip because we don't want to report about hails or zoning
                pass
              else:
                myPublicNote = pChars["Data"][aChar]["PublicNote"]
                if aFlag in dicTally:
                  #Already in the dictionary, increase the count
                  dicTally[aFlag]["Total"] = 1 + dicTally[aFlag]["Total"]
                  #Check if current publicNotein publicNotes dictionary
                  if myPublicNote in dicTally[aFlag]["PublicNotes"]:
                    #It is, increment it
                    dicTally[aFlag]["PublicNotes"][myPublicNote] = 1 + dicTally[aFlag]["PublicNotes"][myPublicNote]
                  else:
                    #It is not, add it
                    dicTally[aFlag]["PublicNotes"][myPublicNote] = 1
                else:
                  #Not in the dictionary, add new entry int dicTally
                  dicTally[aFlag] = {"Total" : 1}
                  dicTally[aFlag]["PublicNotes"] = {myPublicNote : 1}
    
    #Check that data was found
    if len(dicTally) == 0:
      myEncounterList = "No encounters match the critera"
    else:
      myLoopCount = 0
      myEncounterList = ""

      #Get a byTotal dictionary based on dicTally, with count as the key and one to many relationship count to encounter
      byTotal = {}
      for aFlag in dicTally:
        myTotal = dicTally[aFlag]["Total"]
        
        if myTotal in byTotal:
          byTotal[myTotal].append(aFlag)
        else:
          byTotal[myTotal] = [aFlag]

      #Iterate through byTotal dictionary and its correlating flags for each total
      for aTotal in sorted(byTotal, reverse=True):
        for aFlag in byTotal[aTotal]:

          #Only return the top 10, so stop after 10
          myLoopCount += 1
          if myLoopCount <= 10:
            #Concatenate all the public notes for this encounter
            lstFormatedPublicNotes = []
            for aPublicNote in dicTally[aFlag]["PublicNotes"]:
              #print("  ", aFlag, aPublicNote)
              lstFormatedPublicNotes.append("{} ({})".format(aPublicNote, dicTally[aFlag]["PublicNotes"][aPublicNote]))
            publicNotesToString = ", ".join(lstFormatedPublicNotes)

            #Use myCoutnerList to aggregate total, flag name, and concatenated public note information
            myEncounterList += "{}: **{}**\r    {}\r".format(aTotal, aFlag,publicNotesToString)
    
    if pWho == "":
      pWho = "the guild"

    #Build header either for guild or a player
    myHeader = "Top 10 avaialble backflags for **{}**.\rCharacters have Hedge PreFlag done and logged in within the last {} days as of guild dump ({}).\r".format(pWho, pDays, pChars["MetaData"]["DateTime"])

    myOutput = myHeader + myEncounterList
    print("LoopTopTen End")
    return myOutput



  async def loopNeeds(self, pChars, pDays, pEncounter):   
    dictOutput = {}

    #iterate through each character in the dump
    for aChar in pChars["Data"]:

      #Check to see if this character has logged in the last 30 Days
      if int(pChars["Data"][aChar]["DaysSinceLastLogin"]) <= pDays:
        #Check to see if the character has a PoP flagging dictionary
        if "PoPFlagsCanDo" in pChars["Data"][aChar]:
          #Check to see if they have done at least hedge pre flag
          if not "PreFlag Hedge" in pChars["Data"][aChar]["PoPFlagsCanDo"]:
            #Iterate through this character's flags
            for aFlag in pChars["Data"][aChar]["PoPFlagsCanDo"]:
              #Check to see if this is the encounter we're looking for
              if pEncounter.lower() in aFlag.lower() and not "ZoneInto" in aFlag:
                print(aChar)
                #Create output string            
                myCharName = aChar
                myPlayer = pChars["Data"][aChar]["PublicNote"]
                myClass = pChars["Data"][aChar]["Class"]
                myLevel = pChars["Data"][aChar]["Level"]

                myLine = "    {}:{} ({} {})\r".format(myPlayer, myCharName, myLevel, myClass)

                #Write to dictOutput
                if not aFlag in dictOutput:
                  tempDict={}
                  myArr = []
                  myArr.append(myLine)
                  tempDict[myPlayer] = myArr                
                  dictOutput[aFlag] = tempDict
                elif not myPlayer in dictOutput[aFlag]:
                  myArr = []
                  myArr.append(myLine)
                  dictOutput[aFlag][myPlayer] = myArr
                else:
                  #Append output string as new element
                  dictOutput[aFlag][myPlayer].append(myLine)
    myMsg = await self.formatFlagsNeeds(dictOutput, pDays, pChars["MetaData"]["DateTime"])

    return myMsg


  async def formatFlagsNeeds(self, pCharFlags, pDays, pDumpDate): 
    
    #Check if there is data in the output
    if len(pCharFlags) == 0:
      #No data, write an error
      myOutput = "No characters match the critera"
    else:
      #Loop through each matching encounter in pCharFlags
      for aFlag in pCharFlags:
        #Create a header for this flag
        myHeader = "**{}**\rHave Hedge PreFlag done and logged in within the last {} days as of guild dump ({}).\r".format(aFlag, pDays, pDumpDate)

        #Create variables for playerlist, output, and a counter
        myPlayerList = ""
        myCharList = ""            
        myCount = 0

        #Loop through each player in dictOutput
        for aPlayer in sorted(pCharFlags[aFlag]):
          print(aPlayer)
          #Build a comma delimited list:  myPlayerList
          if myCount > 0:
            myPlayerList = myPlayerList + ', '
          myCount = myCount + 1
          myPlayerList = myPlayerList + aPlayer

          #Loop through each character in dictOutput  
          for aChar in sorted(pCharFlags[aFlag][aPlayer]):
            #Append character name to output
            myCharList += aChar

        #Combine header, the player list, and the list of characters.
        myOutput = myHeader + myPlayerList + "\r" + myCharList
    
    return myOutput