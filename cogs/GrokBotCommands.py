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
      #Setup test message with message so far and this line
      myTestMsg = myMsg + "\r" + aLine

      #Check to see if this is over 2000
      if len(myTestMsg) > 2000:
        print("Over 2000")
        #DM myMsg before this line was added
        await ctx.message.author.send(myMsg)
        #Start myMsg over with current line
        myMsg = aLine
      else:
        #Use the test message as the message
        myMsg = myTestMsg
        #print("  " + myMsg)
      
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
    myArgMsg =  "Received: {}\rParsed as: ?{}{}\r".format(ctx.message.content.splitlines()[0], ctx.command, await self.parsedArgs(ctx))

    #Build an @mention to be used in non-DM channels
    msgWithMention = myArgMsg + "Response sent as DM to {}".format(ctx.message.author.mention)

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
    elif repDB.getEQGuildName(ctx) is None:
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
                      myCharName = myDump[aChar]["Name"]
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
  async def uploadGuildDump(self, ctx):

    #Check if command too spammy
    numSec = 7
    if self.isCommandSpam(ctx, numSec):
      myMsg = "Come on {}, lets give more than {} seconds between commands".format(ctx.message.author.mention, numSec)
      await ctx.channel.send(myMsg)
    else:
      myMsg = "Undefined message"
      #Start the ... typing for the bot in the channel
      async with ctx.channel.typing():
        #Echo command 
        await self.echoCommand(ctx)

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
            #process only the first attachment with processAttachment
            myGuildDump = await processGuildDump(ctx.message.attachments[0])
            
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
                if myGuildDump["Data"][aChar]["DaysSinceLastOn"] <= 90:
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
              
        await ctx.send(myMsg)

async def processGuildDump(pAttachment):
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

  #Read context of text file
  attachment_contents = await pAttachment.read()  

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


