import discord
from discord.ext import commands
import typing

def whatIs(myObj):
  print(type(myObj))
  for stuff in dir(myObj):
    print(stuff)

def setup(paramBot):
  paramBot.add_cog(GrokBotCommands(paramBot))


#add property to class a way to track history of commands and commands in progress
#  discord server, discord user, command timestart/timeend, no timeend means it is in process

class GrokBotCommands(commands.Cog):
  def __init__(self, paramBot):
    self.bot = paramBot
    self.history = {}
    self.help = {}
    self.help["needs"] = {"Scope" : "Guild"}
    self.help["topten"] = {"Scope" : "Guild"}
    self.help["upload"] = {"Scope" : "Guild"}
    self.help["flag"] = {"Scope" : "Global"}

    helpText = "format: !needs <optional # of days> <backflag encounter>\r\r"
    helpText += "Examples:\r"
    helpText += "!needs MB\r"
    helpText += "!needs 7 hoh\r"
    helpText += "!needs 45 jiva\r"
    helpText += "\rEncounter will match partial, needs to be at least 3 characters long"
    self.help["needs"]["Text"] = helpText

    helpText = "format: !topten <optional # of days> <optional Public note>\r\r"
    helpText += "Examples:\r"
    helpText += "!topten\r"
    helpText += "!topten 7\r"
    helpText += "!topten 45 nacho\r"
    self.help["topten"]["Text"] = helpText

    helpText = "format: !upload <required v3 EQ guild dump as only attachment>\r\r"
    helpText += "Examples:\r"
    helpText += "!upload\r"
    self.help["upload"]["Text"] = helpText

    helpText = "format: !flag <character1> <character2> <character3>\r\r"
    helpText += "Examples:\r"
    helpText += "!flag\r"
    helpText += "!flag Grokii\r"
    helpText += "!flag Trust Grokii Hazel\r"
    self.help["flag"]["Text"] = helpText

  

  async def largeDM(self, ctx, paramMsg):
    #Setup variable to hold message under 2000 characters
    myMsg = ""

    #Iterate through each line of paramMsg
    for aLine in paramMsg.splitlines():       
      #Check to see if this line is over 2000 characters
      if len(aLine) > 1999:
        print("Error, a single line is over 2000 characters long")
        print(aLine)
      else:
        #Try to append this line to the current message
        myTestMsg = myMsg + "\r" + aLine

        #Check to see if this is over 2000
        if len(myTestMsg) > 1999:
          #Current message plus this line is over 2000, send previous
          await ctx.message.author.send(myMsg)

          #Start message with current line
          myMsg = aLine
        else:
          #Test message isn't over 1999, use it
          myMsg = myTestMsg
      
    #Check to see if any data left in myMsg to send
    if len(myMsg) > 0:
      #Send it
      await ctx.message.author.send(myMsg)
        

  async def parsedArgs(self, ctx):
    #Create local variables for args from context
    myArgs = ctx.args

    #Build string for the args as processed by the discord command object   
    myReturn = ""
    for anArg in myArgs:
      #Check if there is a space in the line
      if " " in str(anArg):
        #This is header information from the discord.py object, ignore it
        pass
      else:
        #Append this argument to the parsedArg string
        myReturn += " " + str(anArg)
    return myReturn

  async def echoCommand(self, ctx):
    import discord

    #Build the response message
    myArgMsgLineOne =  "Received: {}\r".format(ctx.message.content.splitlines()[0])
    myArgMsgLineTwo =  "Parsed as: ?{}{}\r".format(ctx.command, await self.parsedArgs(ctx))
    myArgMsg = myArgMsgLineOne + myArgMsgLineTwo

    #Build an @mention to be used in non-DM channels
    msgWithMention = myArgMsg + "Response sent as DM to {}".format(ctx.message.author.mention)

    #Send to console the command and author
    print(ctx.message.author)
    print(myArgMsgLineOne)
    print(myArgMsgLineTwo)

    #Check if we're in a DM channel
    if isinstance(ctx.channel, discord.DMChannel):
      #In DM channel, echo command in this channel
      await ctx.channel.send(myArgMsg)
    else:
      #In guild channel, echo command in this channel and echo the DM
      await ctx.channel.send(msgWithMention, delete_after=120)
      await ctx.message.author.send(myArgMsg, delete_after=120)
      await ctx.message.delete() 

  def isCommandSpam(self, ctx, paramThreshold: typing.Optional[int] = 5):
    #print(self.history)
    #Create variables from ctx object
    myAuthor = ctx.message.author
    myServer = ctx.message.guild.name if ctx.message.guild else "DM"
    myCmd = ctx.message.content.splitlines()[0].split(" ")[0]
    myCreatedAt = ctx.message.created_at
    myFullCmd = ctx.message.content.splitlines()[0]

    #Create dictionary objects for this message
    dictTime_Cmd = {myCreatedAt : myFullCmd}
    dictcmd = {myCmd : dictTime_Cmd}
    dictServer = {myServer: dictcmd}
    
    #variable to track delta, default to paramThreshold
    myDelta = paramThreshold

    #Check if this is the first time this author issued a command
    if not myAuthor in self.history:
      #Add new author
      self.history[myAuthor] = dictServer
    #Check if this is the first time the author issued any command on this server
    elif not myServer in self.history[myAuthor]:
      #Add new server
      self.history[myAuthor][myServer] = dictcmd
    #Check if this is the first time the author issued this command on this server
    elif not myCmd in self.history[myAuthor][myServer]:
      #Add new command
      self.history[myAuthor][myServer][myCmd] = dictTime_Cmd
    else:
      #Get the command time for this author
      myTimes = []
      #print("Discovery")
      for aServer in self.history[myAuthor]:
        for aCmd in self.history[myAuthor][aServer]:
          for aTime in self.history[myAuthor][aServer][aCmd]:
            #print(aServer + ":  " + str(aTime))
            myTimes.append(aTime)

      #Get the most recent time for this command from the history
      #mostRecent = max(self.history[myAuthor][myServer][myCmd].keys())
      mostRecent = max(myTimes)

      if str(myAuthor) == "Grokii#6581":
        #set myDelta to 0 regardless of reality
        myDelta = 0
      else:
        #Get number of seconds the most recent historical command and this command
        myDelta = (myCreatedAt - mostRecent).total_seconds()

      if myDelta < paramThreshold:
        #Command is spam, return number of seconds
        return myDelta
      else:
        #Command isn't spam, add it to the existing command history
        self.history[myAuthor][myServer][myCmd][myCreatedAt] = myFullCmd
    return 0   

#Add command for WFH.flagPoPFlag_PreReq

  @commands.command(name='prereq', help='Looks up prerequisites for a PoP flag')
  #async def botCommand_test(self, ctx, parmDays: typing.Optional[int] = 30, parmPlayer: typing.Optional[str] = None):
  async def botCommand_test(self, ctx, pFlag: typing.Optional[str]):
    #Check if command too spammy
    numSec = 7
    if self.isCommandSpam(ctx, numSec):
      myMsg = "Come on {}, lets give more than {} seconds between commands".format(ctx.message.author.mention, numSec)
      await ctx.channel.send(myMsg)
    else:
      #Start the ... typing for the bot in the channel
      async with ctx.channel.typing():
        #Not spam, echo command 
        await self.echoCommand(ctx)
        
        #Get data from WFH_Magelo class
        from classes.WFH_Magelo import WFH_Magelo
        WFH = WFH_Magelo()
        myOutput = await WFH.flagPoPFlag_PreReq(pFlag, 1, 1)

        if not len(myOutput) > 0:
          myOutput = "No flags by that name, try using !flag to get a short flag name"

        #Send DM to author
        await ctx.message.author.send(myOutput)        

  @commands.command(name='needs', help='Reviews recent guild dump and lists players/characters that need a PoP flagging encounter')
  #async def botCommand_test(self, ctx, parmDays: typing.Optional[int] = 30, parmPlayer: typing.Optional[str] = None):
  async def botCommand_Needs(self, ctx, pDays: typing.Optional[int] = 30, pEncounter: typing.Optional[str] = ""):
    #Get data from replitDB
    from classes.replitDB import replitDB
    repDB = replitDB()

    #Check if command too spammy
    numSec = 7
    if self.isCommandSpam(ctx, numSec):
      myMsg = "Come on {}, lets give more than {} seconds between commands".format(ctx.message.author.mention, numSec)
      await ctx.channel.send(myMsg)
    elif await repDB.getEQGuildName(ctx) is None:
      #Do nothing
      pass
    else:
      #Start the ... typing for the bot in the channel
      async with ctx.channel.typing():
        #Not spam, echo command 
        await self.echoCommand(ctx)
        

              
        newestDump = await repDB.getGuildProperty(ctx, "NewestGuildDump")        
        if newestDump is None:
          myOutput = "No guild dump avaialble, is this a DM channel?"
          print(myOutput)
          await ctx.message.author.send(myOutput)
        else:
          myDump = newestDump["Data"]
          myDumpDate = newestDump["MetaData"]["DateTime"]
          
          dictOutput = {}
          #iterate through each character in the dump
          for aChar in myDump:
            #Check to see if this character has logged in the last 30 Days
            if int(myDump[aChar]["DaysSinceLastLogin"]) <= pDays:
              #Check to see if the character has a PoP flagging dictionary
              if "PoPFlagsCanDo" in myDump[aChar]:
                #Check to see if they have done at least hedge pre flag
                if not "PreFlag Hedge" in myDump[aChar]["PoPFlagsCanDo"]:
                  #Iterate through this character's flags
                  for aFlag in myDump[aChar]["PoPFlagsCanDo"]:
                    #Check to see if this is the encounter we're looking for
                    if pEncounter.lower() in aFlag.lower() and not "ZoneInto" in aFlag:
                      #Create output string            
                      myCharName = aChar
                      myPlayer = myDump[aChar]["PublicNote"]
                      myClass = myDump[aChar]["Class"]
                      myLevel = myDump[aChar]["Level"]

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
          
          #Check if there is data in the output                                          
          if len(dictOutput) == 0:
            #No data, write an error
            myOutput = "No characters match the critera"
            print(myOutput)
            await ctx.message.author.send(myOutput)
          else:
            #Loop through each matching encounter in dictOutput
            for aFlag in dictOutput:
              #Create a header for this flag
              myHeader = "{}\rLogged in within the last {} days from guild dump:  \r".format(aFlag, pDays, myDumpDate)  

              #Create variables for playerlist, output, and a counter
              myPlayerList = ""
              myCharList = ""            
              myCount = 0

              #Loop through each player in dictOutput
              for aPlayer in sorted(dictOutput[aFlag]):
                #Build a comma delimited list:  myPlayerList
                if myCount > 0:
                  myPlayerList = myPlayerList + ', '
                myCount = myCount + 1
                myPlayerList = myPlayerList + aPlayer

                #Loop through each character in dictOutput  
                for aChar in sorted(dictOutput[aFlag][aPlayer]):
                  #Append character name to output
                  myCharList += aChar

              #Combine header, the player list, and the list of characters.
              myOutput = myHeader + myPlayerList + "\r" + myCharList

              #Send DM to author
              await ctx.message.author.send(myOutput) 

  @commands.command(name='topten', help='Reviews recent guild dump and top ten encounters needed for the guild or a player')
  #async def botCommand_test(self, ctx, parmDays: typing.Optional[int] = 30, parmPlayer: typing.Optional[str] = None):
  async def botCommand_topten(self, ctx, pDays: typing.Optional[int] = 30, pWho: typing.Optional[str] = ""):
    #Check if command too spammy
    numSec = 7
    if self.isCommandSpam(ctx, numSec):
      myMsg = "Come on {}, lets give more than {} seconds between commands".format(ctx.message.author.mention, numSec)
      await ctx.channel.send(myMsg)
    else:
      #Start the ... typing for the bot in the channel
      async with ctx.channel.typing():
        #Not spam, echo command 
        await self.echoCommand(ctx)
        
        #Get data from replitDB
        from classes.replitDB import replitDB
        repDB = replitDB()
              
        newestDump = await repDB.getGuildProperty(ctx, "NewestGuildDump")        
        if newestDump is None:
          myOutput = "No guild dump avaialble, is this a DM channel?"
        else:
          myDump = newestDump["Data"]
          myDumpDate = newestDump["MetaData"]["DateTime"]
          
          dicTally = {}
          #iterate through each character in the dump
          for aChar in myDump:
            #Check to see if player is blank or player matches public next
            myPublicNote = myDump[aChar]["PublicNote"]
            if pWho == "" or pWho.lower() == myPublicNote.lower():
              #Check to see if this character has logged in the last 30 Days
              if int(myDump[aChar]["DaysSinceLastLogin"]) <= pDays:
                #Check to see if the character has a PoP flagging dictionary
                if "PoPFlagsCanDo" in myDump[aChar]:
                  #Check to see if they have done at least hedge pre flag
                  if not "PreFlag Hedge" in myDump[aChar]["PoPFlagsCanDo"]:
                    #Iterate through this character's flags
                    for aFlag in myDump[aChar]["PoPFlagsCanDo"]:
                      if aFlag in dicTally:
                        #Already in the dictionary, increase the count
                        dicTally[aFlag] = dicTally[aFlag] + 1
                      else:
                        #Not in the dictionary, add it
                        dicTally[aFlag] = 1
          if len(dicTally) == 0:
            myEncounterList = "No encounters match the critera"
          else:
            myLoopCount = 0
            myEncounterList = ""
            for aFlag in sorted(dicTally.items(), key=lambda x: x[1], reverse=True):
              myLoopCount += 1
              if myLoopCount <= 10:
                myEncounter = aFlag[0]
                myEncounterCount = str(aFlag[1])
                myEncounterList += myEncounterCount + ":  " + myEncounter + "\r"
          
          #Build header either for guild or a player
          myHeader = "Top 10 available backflags for characters in game within " + str(pDays) + " days for "
          if pWho == "":
            myHeader += "the guild"
          else:
            myHeader += pWho 
          myHeader += "\rGuild Dump ({})\r".format(myDumpDate)
          
          myOutput = myHeader + myEncounterList

        #Send DM to author
        await ctx.message.author.send(myOutput)        

  @commands.command(name='flag', help='Queries Magelo for up to 3 characters and displays flag information for them')
  async def botCommand_flag(self, ctx, parmPlayerOne: typing.Optional[str] = None, parmPlayerTwo: typing.Optional[str] = None, parmPlayerThree: typing.Optional[str] = None):
    #Check if command too spammy

    numSec = 7
    if self.isCommandSpam(ctx, numSec):
      myMsg = "Come on {}, lets give more than {} seconds between commands".format(ctx.message.author.mention, numSec)
      await ctx.channel.send(myMsg)
    #Check if help was requested
    if str(parmPlayerOne).lower() == 'help':
      await ctx.channel.send(self.help["flag"]["Text"])
    else:
      #Start the ... typing for the bot in the channel
      async with ctx.channel.typing():
        #Not spam, echo command 
        await self.echoCommand(ctx)

        #Setup regex and regex filter to sanitize anything not alpha
        import re
        alpha = re.compile('[^a-zA-Z]')
  
        #add up to 3 sanitized player names to charList
        charList = {}
        
        #Add player one
        if parmPlayerOne:
          sanitizedName = alpha.sub('', parmPlayerOne)
          if len(sanitizedName) > 1:
            charList[sanitizedName] = ""
          else:
            #zero length, use discord username
            charList[ctx.message.author.name] = ""
        else:
          #no argument, use discord username
          charList[ctx.message.author.name] = ""
     
        #Add player two if had characters after sanitized
        if parmPlayerTwo:
          sanitizedName = alpha.sub('', parmPlayerTwo)
          if len(sanitizedName) > 1:
            charList[sanitizedName] = ""

        #Add player two if had characters after sanitized
        if parmPlayerThree:
          sanitizedName = alpha.sub('', parmPlayerThree)
          if len(sanitizedName) > 1:
            charList[sanitizedName] = ""

        #Create output dictionaries
        cData = {}

        #Loop through charList
        for charName in charList:
          dictChar = {}
          
          #Setup WFH Magelo object
          from classes.WFH_Magelo import WFH_Magelo
          WFH = WFH_Magelo()

          #Get basic data for this character and populate dictChar with the data 
          dictChar = await WFH.getBasicData(charName)
          
          #Add this character's data to the completed data dictionary
          cData[charName] = dictChar
        
        for aChar in cData:
          #Build flag data
          myFlags = ""
          
          #Check if flag can do exists
          if "PoPFlagsCanDo" in cData[aChar]:
            #Check if data in FlagsCanDo
            if cData[aChar]["PoPFlagsCanDo"]:
              #loop over every item and append to myFlags
              for canDoFlag in cData[aChar]["PoPFlagsCanDo"]:
                myFlags += "      {}\r".format(canDoFlag)

          #Check if no flags found, then say say
          if myFlags == "":
            myFlags = "      " + "No flags available"

          outputStatus = cData[aChar]["MageloStatus"]
          if outputStatus == "Roleplaying" or outputStatus == "Normal":
            statusOrElementalProgress = cData[aChar]["ProgressionStatus"]
          else:
            statusOrElementalProgress = outputStatus

          #Line1:  charname (MageloStatus or ElementalStatus)
          #Line2:  
          #line2:  URL
          #line3:  Current Status: (popflagstatus)
          #line4:  Available PoP flags to obtain:
          #line5+  (Flags)
          
          myOutput = "{} ({})\r".format(aChar.capitalize(), statusOrElementalProgress)
          myOutput += "   {}\r".format(await WFH.getURL("flags", aChar, 0))
          #Check if character is roleplaying or normal
          if outputStatus == "Roleplaying" or outputStatus == "Normal":
            #Output flag data
            myOutput += "   Available PoP flags to obtain:\r"
            myOutput += myFlags
          
          #Send DM to author
          await ctx.message.author.send(myOutput)

  @commands.command(name='upload', help='Uploads v3 guild dump to database')
  async def uploadGuildDump(self, ctx, pDays: typing.Optional[int] = 0):

    #Check if command too spammy
    numSec = 7
    if self.isCommandSpam(ctx, numSec):
      myMsg = "Come on {}, lets give more than {} seconds between commands".format(ctx.message.author.mention, numSec)
      await ctx.channel.send(myMsg)
    else:
      myMsg = "Undefined message"
      #Start the ... typing for the bot in the channel
      async with ctx.channel.typing():

        #Build list of approved people to upload
        lstApproved = []
        lstApproved.append('Grokii#6581')

        author = str(ctx.message.author)

        if not author in lstApproved:
          myMsg = "Not in approved list to upload"
          print(myMsg)
        else:
          #Check if there is at least one attachment
          if not ctx.message.attachments:
            myMsg = "No attachment"
            print(myMsg)
          else:
            print("There is at least one attachment, try to parse it ")

            #process only the first attachment with processAttachment
            myGuildDump = await self.processGuildDump(ctx.message.attachments[0])
            
            #Set myDumpName to DATE-TIME from the meta data of the file attachment
            myDumpName = "{}-{}".format(myGuildDump["Metadata"]["Date"], myGuildDump["Metadata"]["Time"])
            print("Current Dump Name:  " + myDumpName)

            #Get data from replitDB
            from classes.replitDB import replitDB
            repDB = replitDB()

            #Wipe data for a guild
            #await repDB.wipeGuild(ctx)
            
            newestGuildDump = await repDB.getGuildProperty(ctx, "NewestGuildDump")

            #Check to make sure data was extracted from the file
            if myGuildDump is None:
              myMsg = "processAttachment unable to process file"
              print(myMsg)
            #Check if guild dumps from the DB is None
            elif newestGuildDump is None:
              myMsg = "No guild dumps in DB, likely because tried upload from DM"
              print(myMsg)            
            #Query Magelo and write the data back to the database
            else:
              guildCharList = {}              
              #Iterate through each character in the guild dump
              for aChar in myGuildDump["Data"]:
                if myGuildDump["Data"][aChar]["DaysSinceLastOn"] <= pDays:
                  #Setup WFH Magelo object
                  from classes.WFH_Magelo import WFH_Magelo
                  WFH = WFH_Magelo()

                  #Get Magelo data for this character
                  dictChar = await WFH.getBasicData(aChar)
                  await WFH.getKeyData(aChar, dictChar)
                  await WFH.getAAData(aChar, dictChar)
                  await WFH.getSkillData(aChar, dictChar)

                  #Add guild dump data to dictChar (overwrite level/class because /roleplaying and /anon)
                  dictChar["Level"] = myGuildDump["Data"][aChar]["Level"]
                  dictChar["Class"] = myGuildDump["Data"][aChar]["Class"]
                  dictChar["Rank"] = myGuildDump["Data"][aChar]["Rank"]
                  dictChar["DaysSinceLastLogin"] = myGuildDump["Data"][aChar]["DaysSinceLastOn"]
                  dictChar["PublicNote"] = myGuildDump["Data"][aChar]["PublicNote"]

                  #Add this character to guildCharList
                  guildCharList[aChar] = dictChar
              
              buildingDump = {}
              #Prep myGuildDumps read from db with new data              
              buildingDump = {"Data" : guildCharList}

              #Get current date/time and set meta data
              from datetime import datetime, timedelta              
              now = datetime.now() - timedelta(hours=5, minutes=0)
              buildingDump["MetaData"] = {"Uploader" : author, "DateTime" : now.strftime("%m/%d/%Y %H:%M:%S")}              

              #Upload previous dump (newestGuildDUmp) to previous dump
              await repDB.setGuildProperty(ctx, "PreviousGuildDump", newestGuildDump)

              #Upload guild dump just built to newest dump
              await repDB.setGuildProperty(ctx, "NewestGuildDump", buildingDump)

              print("Finished for loop of each character, send msg")
              myMsg = "Successly uploaded!\r\rToDo\r1) Change this is a DM?\r"

        #Echo command 
        await self.echoCommand(ctx)
        
        #Send DM to author
        await ctx.message.author.send(myMsg)        

  async def processGuildDump(self, pAttachment):
    #Set dumpFileName
    #example: Spirit of Potato-20201121-183443.txt)
    dumpFileName = pAttachment.filename.replace('.txt', '')

    splitDumpFileName = dumpFileName.split('-')
    if len(splitDumpFileName) == 3:
      #Create dictionary to contain meta data from filename
      dumpMeta = {"Guild" : splitDumpFileName[0], "Date" : splitDumpFileName[1], "Time" : splitDumpFileName[2]}
    else:
      print("Filename not valid:  ".format(pAttachment.filename))
      return None

    print("Attempting to read contents")
    #Read context of text file
    attachment_contents = await pAttachment.read()  
    print("Contents read")

    #Clean up the data that discord adds
    dumpData = str(attachment_contents)
    dumpData = dumpData[2:]  #Remove left two characters (b')
    dumpData = dumpData[:-1]  #remove the final character (')

    #Filename appears good, likely valid try to parse it with Everquest class
    from classes.Everquest import Everquest
    EQ = Everquest()
    dictGuildDump = {"Metadata" : dumpMeta}
    dictGuildDump["Data"] = await EQ.parseGuildDump(dumpData)

    if dictGuildDump["Data"] is None:
      print("Error processing guild dump:  " + pAttachment.filename)
    else:
      #Guild dump parsed successfully, return it
      return dictGuildDump

  @commands.command(name='ch', help='Creates Ch chain from raid dump')
  async def commandCH(self, ctx, pLength: typing.Optional[int] = 0, *args):

    #Check if command too spammy
    numSec = 7
    if self.isCommandSpam(ctx, numSec):
      myMsg = "Come on {}, lets give more than {} seconds between commands".format(ctx.message.author.mention, numSec)
      await ctx.channel.send(myMsg)
    else:
      myMsg = "Undefined message"
      #Start the ... typing for the bot in the channel
      async with ctx.channel.typing():
        #Check if there is at least one attachment
        if not ctx.message.attachments:
          myMsg = "No attachment"
          print(myMsg)
        else:  
          #Read context of text file
          attachment_contents = await ctx.message.attachments[0].read()  

          #Clean up the data that discord adds
          dumpData = str(attachment_contents)
          dumpData = dumpData[2:]  #Remove left two characters (b')
          dumpData = dumpData[:-1]  #remove the final character (')

          #Try to parse it with Everquest class
          from classes.Everquest import Everquest
          EQ = Everquest()    
          dictGuildDump = await EQ.parseRaidDump(dumpData)

          if dictGuildDump is None:
            print("Error processing raid dump")
          else:
            #set dumpClerics with list of 65 clerics from the raid dump
            dumpClerics = []
            for aChar in dictGuildDump:
              myClass = dictGuildDump[aChar]['Class']
              myLevel = int(dictGuildDump[aChar]['Level'])
              if myClass == 'Cleric' and myLevel == 65:
                dumpClerics.append(aChar)
            
            #Preserve raw dump of 65 clerics in the raid
            rawDumpClerics = dumpClerics.copy()
            
            print("Looping through excluded args")
            
            #Loop through args for clerics to be excluded
            for aCleric in args:
              #Santize the cleric's name
              mySanitizedClericName = str(aCleric).lower().capitalize()
              print(mySanitizedClericName)

              #Loop through clerics in dumpClerics
              for i, dCleric in enumerate(dumpClerics):
                #Check if arg cleric is equal to dump cleric
                if mySanitizedClericName == dCleric:
                  #Remove cleric from dumpClerics
                  dumpClerics.pop(i)                          
            
            #Check if the length of the CH chain has to be calculated
            if pLength == 0:
              #Set the length to the number of non-excluded clerics available
              pLength = len(dumpClerics)

            #Check if there aren't enough clerics given the requested length
            if len(dumpClerics) < pLength:
              myMsg = "Requested {} only {} non-excluded clerics".format(pLength, len(dumpClerics))
              print(myMsg)
            else:
              #Create array of the proper size, each value will be None
              myCH = [None] * pLength

              #Define Cleric to clump together
              clericClump = []
              clericClump.append(["Rezzes", "Aledrin"])
              clericClump.append(["Yvonnel","Froaki","Giblet"])
              clericClump.append(["Scarto", "Statler", "Waldorf"])

              #Define clerics prefer at the start of the chain
              #clericStart = ["Rezzes"]

              #Loop through all clerics in 'clericStart'
              #for aCleric in clericStart:
                #Check to see if this cleric is in the raid
              #  if aCleric in dumpClerics:
              #    await self.addCleric(aCleric, clericClump, dumpClerics, myCH)

              #Loop through all clerics in 'clericClump'
              for aSet in clericClump:
                #Loop through clerics in this set
                for aCleric in aSet:
                  #Check to see if this cleric is in the raid
                  if aCleric in dumpClerics:
                    await self.addCleric(aCleric, clericClump, dumpClerics, myCH)

              #Loop through the rest of the clerics in dumpClerics
              for aCleric in sorted(dumpClerics):
                await self.addCleric(aCleric, clericClump, dumpClerics, myCH)

              #Create a message from myCH:
              myMsg = "Cleric Chain:  "
              for i, aCleric in enumerate(myCH, 1):
                #Build translation for 10+ clerics in the chain
                myTranslate = {10:"A",11:"B",12:"C",13:"D",14:"E",15:"F",16:"G"}

                #Set myNum with translation
                if i in myTranslate:
                  myNum = myTranslate[i]
                else:
                  myNum = str(i)

                #Add this cleric with their number to the chain message
                myMsg += "{}) {} ".format(myNum, aCleric)

              #List clerics in the raid that are out of the chain
              myMsg += "\rNot in chain: "
              for aCleric in rawDumpClerics:
                if not aCleric in myCH:
                  myMsg += " {} ".format(aCleric)
              print(myCH)
              print(myMsg)

      #Echo command 
      await self.echoCommand(ctx)

      #Send DM to author
      await ctx.message.author.send(myMsg)        


  async def addCleric(self, pCleric, pClump, pDump, pCH):    
    #Iterate throuch each clump clerics
    for aClump in pClump:
      #Check if our cleric is in this clump
      if pCleric in aClump:
        #Iterate through each cleric in the clump
        for aCleric in aClump:
          #Check if this cleric is in the pDump and not in pCH already
          if aCleric in pDump and not aCleric in pCH:
            #Iterate through pCH to look for the first open spot
            for i, aSpot in enumerate(pCH):
              #Check to see if this spot is none
              if aSpot is None:
                #Add this cleric to this spot
                pCH[i] = aCleric

                #break out of for loop
                break
    
    #Check to see if the cleric is not already in pCH
    if not pCleric in pCH:
      #Add the cleric to the first available slot
      for i, aSpot in enumerate(pCH):
        #Check to see if this spot is none
        if aSpot is None:
          #Add this cleric to this spot
          pCH[i] = pCleric

          #break out of for loop
          break

  @commands.command(name='link', help="Links a EQ Public Note with a discord username")
  @commands.has_role("leadership")
  async def botCommand_link(self, ctx, pMember: discord.Member, pPublicNote = ""):

    #Get data from replitDB
    from classes.replitDB import replitDB
    repDB = replitDB()
    
    if 1==0:
      #How to get the member from the ID
      myMember = await ctx.guild.fetch_member(pMember.id)
      print("ID ({}) Name ({}) Nick ({})".format(myMember.id, myMember.name, myMember.nick))

    #Check if command too spammy
    numSec = 7
    if self.isCommandSpam(ctx, numSec):
      myMsg = "Come on {}, lets give more than {} seconds between commands".format(ctx.message.author.mention, numSec)
      await ctx.channel.send(myMsg)
    elif await repDB.getEQGuildName(ctx) is None:
      myMsg = "Couldn't get guild name from database"
      print(myMsg)   
    elif len(pPublicNote) > 0:
      print("{}:{}".format(pMember.id, pPublicNote))
      
      
      #Get newestDump from database
      newestDump = await repDB.getGuildProperty(ctx, "NewestGuildDump")
      links = await repDB.getGuildProperty(ctx, "Links")
      #links = []
      print(links)

      #Check to see if pPublicNote is in newestDump
      isNoteInDump = 0
      for aChar in newestDump["Data"]:
        if newestDump["Data"][aChar]["PublicNote"].lower() == pPublicNote.lower():
          isNoteInDump = 1
          pPublicNote = newestDump["Data"][aChar]["PublicNote"]
      
      if isNoteInDump == 1:
        #Check to see if either pPublicNote or pDiscordName already in links
        isNoteLinked = 0
        isDiscordLinked = 0
        for aLink in links:
          if aLink["PublicNote"].lower() == pPublicNote.lower():
            isNoteLinked = 1
          if aLink["DiscordMemberID"] == pMember.id:
            isDiscordLinked = 1
        
        #Check to see if both neither publicNote nor DiscordName is linked
        if isNoteLinked == 0:
          if isDiscordLinked == 0:
            #Link them and send to database
            myLink = {"PublicNote" : pPublicNote, "DiscordMemberID" : pMember.id}
            links.append(myLink)
            await repDB.setGuildProperty(ctx, "Links", links)
            myMember = await ctx.guild.fetch_member(myLink["DiscordMemberID"])
            myMsg = "Linked ({}) and ({})".format(myMember, pPublicNote)         
          else:
            #PublicNote isn't in most recent guild dump
            myMsg = "Discord id ({}) is already linked".format(pMember.id)
            print(myMsg)
            print(links)            
        else:
          #PublicNote isn't in most recent guild dump
          myMsg = "PublicNote ({}) is already linked".format(pPublicNote)
          print(myMsg)
          print(links)
      else:
        #PublicNote isn't in most recent guild dump
        myMsg = "PublicNote ({}) isn't in most recent guild dump".format(pPublicNote)
        print(myMsg)
    else:
      #PublicNote isn't in most recent guild dump
      myMsg = "PublicNote ({}) is zero length or DiscordName ({}) is not valid".format(pPublicNote, pMember)
      print(myMsg)

    #Echo command and send message
    await self.echoCommand(ctx)
    await ctx.send(myMsg)    

  @commands.command(name='unlink', help="Unlinks a public note from a discord user")
  @commands.has_role("leadership")
  async def botCommand_unlink(self, ctx, pName=""):
    #Get data from replitDB
    from classes.replitDB import replitDB
    repDB = replitDB()

    #Check if command too spammy
    numSec = 7
    if self.isCommandSpam(ctx, numSec):
      myMsg = "Come on {}, lets give more than {} seconds between commands".format(ctx.message.author.mention, numSec)
      await ctx.channel.send(myMsg)
    elif await repDB.getEQGuildName(ctx) is None:
      myMsg = "Couldn't get guild name from database"
      print(myMsg)   
    else:
      links = await repDB.getGuildProperty(ctx, "Links")
      #links = []
      print(links)

      #loop through links looking for a match
      isMatch = 0
      for i, aLink in enumerate(links):
        myPublicNote = aLink["PublicNote"]        
        myMember = await ctx.guild.fetch_member(aLink["DiscordMemberID"])        

        #If a mention was passed as an argument, remove the wrappings <@!123> = 123
        pName = pName.replace('<@!', '').replace('>', '')

        #Check if public note or discord name matches
        if myPublicNote.lower() == pName.lower() or str(myMember.id) == pName:
          #Build message
          myMsg = "Removed link between ({}) and ({})".format(myMember, myPublicNote)
          print(myMsg)
          #Remove from link
          links.pop(i)
          isMatch = 1
      
      #Check if there was a matches
      if isMatch == 1:
        #Upload links to database
        await repDB.setGuildProperty(ctx, "Links", links)
      else:
        #No match found
        myMsg = "No link found for ({})".format(pName)
        

    #Echo command and send message
    await self.echoCommand(ctx)
    await ctx.send(myMsg)    

  @commands.command(name='who', help="Looks up characters by discord name or public note")  
  async def botCommand_who(self, ctx, pName=""):
    #Get data from replitDB
    from classes.replitDB import replitDB
    repDB = replitDB()

    #Check if command too spammy
    numSec = 7
    if self.isCommandSpam(ctx, numSec):
      myMsg = "Come on {}, lets give more than {} seconds between commands".format(ctx.message.author.mention, numSec)
      await ctx.channel.send(myMsg)
    elif await repDB.getEQGuildName(ctx) is None:
      myMsg = "Couldn't get guild name from database"
      print(myMsg)   
    else:
      #Check if pName is in link

      #Get links and newest guild dump from db
      links = await repDB.getGuildProperty(ctx, "Links")
      newestDump = await repDB.getGuildProperty(ctx, "NewestGuildDump")

      #loop through links looking for a match
      isMatch = 0
      for aLink in links:
        myPublicNote = aLink["PublicNote"]        
        myMember = await ctx.guild.fetch_member(aLink["DiscordMemberID"])        

        #If a mention was passed as an argument, remove the wrappings <@!123> = 123
        pName = pName.replace('<@!', '').replace('>', '')

        #Check if public note or discord name matches
        if myPublicNote.lower() == pName.lower() or str(myMember.id) == pName:
          #Match found, flag it and exit for loop
          isMatch = 1          
          break
      if isMatch == 1:
        #Match found in link object, output it        
        myMsg = []
        print(myMember.nick)
        await self.outputwhoFlag(myMember.name, myMember.nick, myPublicNote, newestDump, myMsg)
        myMsg = myMsg[0]
      else:
        #Search for character in guild dump
        myPublicNote = ""
        for aChar in sorted(newestDump["Data"]):
          if aChar.lower() == pName.lower():
            #Match found, set myPublicNote and exit for loop
            myPublicNote = newestDump["Data"][aChar]["PublicNote"]
            print("Match found for {} public note is {}".format(pName, myPublicNote))
            break
        
        #Check if a match was found
        if myPublicNote == "":
          myMsg = "No character or linked discord name found ({})".format(pName)
        else:
          print("Check to see if {} in link".format(myPublicNote))
          #Match found, check to see if public note in link          
          myMember = None
          for aLink in links:            
            if aLink["PublicNote"].lower() == myPublicNote.lower():
              myMember = await ctx.guild.fetch_member(aLink["DiscordMemberID"])
              break
          
          #Check if match found in links
          if myMember is None:
            myMsg = []
            await self.outputwhoFlag("<<Need to link>>", None, myPublicNote, newestDump, myMsg)
            myMsg = myMsg[0]
          else:
            myMsg = []
            await self.outputwhoFlag(myMember.name, myMember.nick, myPublicNote, newestDump, myMsg)
            myMsg = myMsg[0]

    #Echo command and send message
    #await self.echoCommand(ctx)
    await ctx.send(myMsg)

  async def outputwho(self, pName, pNick, pPublicNote, pDump, pMsg):
    #Check to see if myPublicNote is in pDump    
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

  async def outputwhoFlag(self, pName, pNick, pPublicNote, pDump, pMsg):
    #Check to see if myPublicNote is in pDump
    myTotal = 0
    myMsg = ""    
    for aChar in sorted(pDump["Data"]):
      if pDump["Data"][aChar]["PublicNote"].lower() == pPublicNote.lower():
        myLevel = pDump["Data"][aChar]["Level"]
        myClass = pDump["Data"][aChar]["Class"]
        myStatus = pDump["Data"][aChar]["ProgressionStatus"]
        
        if myStatus == 'TimeFlagged':
          myTotal = myTotal + 1

        myMsg += "{} ({}):  {} {}\r".format(aChar, myStatus, myLevel, myClass)

    #Check if there is a nickname
    if pNick is None:
      myHeader = "Discord name {} ({})\r\r".format(pName, myTotal)
    else:
      myHeader = "Discord name {} ({})\rDiscord nickname {}\r\r".format(pName, myTotal, pNick)  
    
    myMsg = myHeader + myMsg

    pMsg.append(myMsg)         

  @commands.command(name='stats', help="Outputs link stats")
  @commands.has_role("leadership")
  async def botCommand_linkstats(self, ctx, pName=""):
    myMsg = ""
    
    #Echo command and send message
    await self.echoCommand(ctx)

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