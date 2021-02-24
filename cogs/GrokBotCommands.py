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
    self.badList = ["penis", 'richard', 'dick']
    self.history = {}
    self.ignore = 510907044513972227


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

  
  async def badword(self, plist): 
    check = False

    # Iterate self.badList 
    for m in self.badList: 

      # Iterate pList 
      for n in plist: 

        # if there is a match
        if m.lower() in n.lower(): 
            check = True
                
    return check 

  async def largeDM(self, ctx, paramMsg, pChannel=0):
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
          if pChannel==0:
            await ctx.message.author.send(myMsg)
          else:
            await ctx.channel.send(myMsg)

          #Start message with current line
          myMsg = aLine
        else:
          #Test message isn't over 1999, use it
          myMsg = myTestMsg
      
    #Check to see if any data left in myMsg to send
    if len(myMsg) > 0:
      #Send it
      if pChannel==0:
        await ctx.message.author.send(myMsg)
      else:
        await ctx.channel.send(myMsg)

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
      #await ctx.message.delete() 

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

  @commands.command(name='roleaudit', aliases=['Roleaudit'], help='TBD')
  @commands.has_role("leadership")
  async def botCommand_roleaudit(self, ctx):
    print("roleaudit cmd")
    from classes.Role import Role
    role = Role()

    #myMsg = await role.multiMutuallyExclusive(ctx)
    #await ctx.channel.send(myMsg)

    myMsg = await role.setManagedRoles(ctx)
    #await ctx.channel.send(myMsg)
    await self.largeDM(ctx, myMsg, 1)


  @commands.command(name='itemstat', aliases=['Itemstat'], help='TBD')
  async def botCommand_stat(self, ctx, pName = None):
    #Check if a character name was sent
    #Check if this is in #general
    if self.ignore == ctx.channel.id:
      myMsg = "Use grok-bot-spam channel instead"
      await ctx.channel.send(myMsg, delete_after=5)
      await ctx.message.delete()       
    elif pName is None:
      myMsg = "Must enter a character name"
      await ctx.channel.send(myMsg)
    else:
      from classes.Inventory import Inventory     
      inv = Inventory()
      myMsg = await inv.getWornItems(pName, 'ATK')
      await ctx.channel.send(myMsg)

  @commands.command(name='spell', aliases=['Spell'], help='TBD')
  async def botCommand_spell(self, ctx, pClass = None):
    await self.echoCommand(ctx)
    #Check if a character class was sent
    if pClass is None:
      myMsg = "Must enter a character class"
      await ctx.channel.send(myMsg)
    #Check if there is at least one attachment
    elif not ctx.message.attachments:
      myMsg = "No attached character spellbook.  To generate, in game type:  /outputfile spellbook charnameClassOrWhatever.txt"
      await ctx.channel.send(myMsg)
    else:
      #Received both a class and an attachment
      #myMsg = "Class {} and attachment".format(pClass)
      
      #Read context of text file
      attachment_contents = await ctx.message.attachments[0].read()  

      #Set the data to a string
      attachmentData = str(attachment_contents)
      #Remove left two characters (b')
      attachmentData = attachmentData[2:] 
      #Remove the final character (') 
      attachmentData = attachmentData[:-1]

      #Parse data with Everquest class
      from classes.Everquest import Everquest
      EQ = Everquest()

      print("Parsing spellobok")
      spellbookData = await EQ.parseSpellBook(attachmentData)
      
      #Check if data was parsed
      if spellbookData is None:
        myMsg = "Error processing guild dump: {}".format(ctx.message.attachments[0].filename)
        print(myMsg)
      else:
        #spellbookData looks good
        print("Spellbook looks good")
        #Create a spell class object
        from classes.Spell import Spell     
        mySpells = Spell()

        #Compare spell data
        print("Comparing start")
        myMsg = await mySpells.compare(pClass, spellbookData)
        print("Compare end")

        #Send response as DM
        await self.largeDM(ctx, myMsg)
      #await ctx.channel.send(myMsg)

  @commands.command(name='vt', aliases=['VT', 'Vt'], help='Checks VT Status')
  async def botCommand_vt(self, ctx, pChar = None):
    if pChar is None:
      print("Must enter a character's name")
    else:
      await self.echoCommand(ctx)

      print(pChar)
      from classes.Inventory import Inventory     
      inv = Inventory()
      myMsg = await inv.VexThalStatus(pChar)
      #await ctx.channel.send(myMsg)
      await self.largeDM(ctx, myMsg)

  @commands.command(name='find', aliases=['Find'], help='Searches for an item')
  async def botCommand_find(self, ctx, *pItem):    
    #Check if this is in #general
    if self.ignore == ctx.channel.id:
      myMsg = "Use grok-bot-spam channel instead"
      await ctx.channel.send(myMsg, delete_after=5)
      await ctx.message.delete() 
    
    #Check if no argument was passed to pItem
    elif len(pItem) == 0:
      myMsg = "No search parameter passed to '?find' command"
      await ctx.channel.send(myMsg, delete_after=5)
      await ctx.message.delete()
    #Check if one argument passed and it is 'guild'
    elif len(pItem) == 1 and pItem[0].lower() == 'guild':
      myMsg = "No search parameter passed to '?find guild' command"
      await ctx.channel.send(myMsg, delete_after=5)
      await ctx.message.delete()
    else:    
      #Check if the first argument is 'guild'
      if pItem[0].lower() == 'guild':
        
        #Remove the first item
        myItem = " ".join(pItem[1:])
        print("Search guild for {}".format(myItem))

        #Get the list of guild characters
        charList = await self.getChars(ctx, 1)
      else:
        charList = await self.getChars(ctx)
        myItem = " ".join(pItem)

      from classes.Inventory import Inventory     
      inv = Inventory()

      ignoredChar = []
      myMsg = "Looking for ({}) for the following characters: {}".format(myItem, " ".join(charList))
      await ctx.channel.send(myMsg)
      for aChar in charList:
        #Use inventory object to search for the item
        myMsg = await inv.findItemByName(aChar, myItem)

        #Check if character was ignored due to character status
        if "Invalid MageloStatus" in myMsg:
          myMsg = ""
          ignoredChar.append(aChar)
          
        if len(myMsg) > 0:
          await ctx.channel.send(myMsg)
    
    #Check if any characters were ignored
    if len(ignoredChar) > 0:
      myIgnored = " ".join(ignoredChar)
      myMsg = "Role/Anon chars ignored: {}".format(myIgnored)
      await ctx.channel.send(myMsg)
        


  @commands.command(name='prereq', aliases=['Prereq', 'prereqs', 'Prereqs'], help='Looks up prerequisites for a PoP flag')
  #async def botCommand_test(self, ctx, parmDays: typing.Optional[int] = 30, parmPlayer: typing.Optional[str] = None):
  async def botCommand_test(self, ctx, *args):

    #Check if command too spammy
    numSec = 7
    if self.isCommandSpam(ctx, numSec):
      myMsg = "Come on {}, lets give more than {} seconds between commands".format(ctx.message.author.mention, numSec)
      await ctx.channel.send(myMsg)
    #elif self.badword(args):
    #  myMsg = "I'm not responding to prophane arguments, are you in Unity or something?"
    #  await ctx.channel.send(myMsg)
    else:
      #Start the ... typing for the bot in the channel
      async with ctx.channel.typing():
        #Not spam, echo command 
        await self.echoCommand(ctx)
        
        #Get data from WFH_Magelo class
        from classes.WFH_Magelo import WFH_Magelo
        WFH = WFH_Magelo()
        myOutput = await WFH.flagPoPFlag_PreReq(' '.join(args))

        if not len(myOutput) > 0:
          myOutput = "No flags by that name, try using ?flag to get a short flag name"

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
    elif pEncounter == "":
      myMsg = "No encounter specified for ?needs command"
      await ctx.channel.send(myMsg)
    else:
      #Not spam, echo command 
      await self.echoCommand(ctx)

      from classes.Flags import Flags
      myFlags = Flags()

      myDump = await myFlags.getGuildDump(ctx)
      myMsg = await myFlags.loopNeeds(myDump, pDays, pEncounter)
      
      #Send DM to author
      #await ctx.message.author.send(myMsg) 
      await self.largeDM(ctx, myMsg, 1)

  @commands.command(name='topten', help='Reviews recent guild dump and top ten encounters needed for the guild or a player')
  async def botCommand_topten(self, ctx, pDays: typing.Optional[int] = 30, pWhom: typing.Optional[str] = ""):
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
      #Not spam, echo command 
      await self.echoCommand(ctx)

      from classes.Flags import Flags
      myFlags = Flags()

      myDump = await myFlags.getGuildDump(ctx)
      
      #Check if pWhom is a form of tater tot
      myTot = ["tot", "tots", "tatertot", "tatertots"]
      if pWhom.lower() in myTot:
        pWhom = "TaterTots"

        #Create a role object
        from classes.Role import Role
        myRole = Role()

        #Get list of public notes for role of TaterTots
        publicNotesRoleTaterTot = await myRole.getPublicNoteOfRole(ctx, pWhom)

        #Filter myDump for only TaterTots
        await myFlags.dumpFilterForPublicNote(myDump, publicNotesRoleTaterTot)
      
      #Check if nothing sent for pWhom
      elif pWhom == "":
        #Don't need to filter anything; the entire guild dump will be used
        #await ctx.channel.send("Entire Guild!")
        pass
      else:
        #await ctx.channel.send("PublicNote: {}".format(pWhom))
        #Filter everything out of the guild dump except for the publicNote in pWhom
        await myFlags.dumpFilterForPublicNote(myDump, [pWhom])

      myMsg = await myFlags.loopTopTen(myDump, pDays, pWhom)
      
      #Send DM to author
      #await ctx.message.author.send(myMsg)      
      await self.largeDM(ctx, myMsg, 1)

  async def botCommand_toptenOLD(self, ctx, pDays: typing.Optional[int] = 30, pWho: typing.Optional[str] = ""):
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
          myDebugCount = 0
          #iterate through each character in the dump
          for aChar in myDump:
            myDebugCount = myDebugCount + 1
            print(myDebugCount, " ", aChar)
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

  @commands.command(name='flag', aliases=['Flag', 'Flags', 'flags'], help='Queries Magelo for up to 3 characters and displays flag information for them')
  async def botCommand_flag(self, ctx, parmPlayerOne: typing.Optional[str] = None, parmPlayerTwo: typing.Optional[str] = None, parmPlayerThree: typing.Optional[str] = None):
    #Check if command too spammy
    numSec = 7
    if self.isCommandSpam(ctx, numSec):
      myMsg = "Come on {}, lets give more than {} seconds between commands".format(ctx.message.author.mention, numSec)
      await ctx.channel.send(myMsg)
    #Check if help was requested
    if str(parmPlayerOne).lower() == 'help':
      await ctx.channel.send(self.help["flag"]["Text"])
    #elif self.badword([parmPlayerOne, parmPlayerTwo, parmPlayerThree]):
    #  myMsg = "I'm not responding to prophane arguments, are you in Unity or something?"
    #  await ctx.channel.send(myMsg)      
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
  @commands.has_role("leadership")
  async def uploadGuildDump(self, ctx, pDays: typing.Optional[int] = 9999):
    print("Command Upload received")
    #Check if command too spammy
    numSec = 7
    if self.isCommandSpam(ctx, numSec):
      myMsg = "Come on {}, lets give more than {} seconds between commands".format(ctx.message.author.mention, numSec)
      await ctx.channel.send(myMsg)
    else:
      myMsg = "Undefined message"
      #Start the ... typing for the bot in the channel
      async with ctx.channel.typing():

        author = str(ctx.message.author)

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

                #Remove items from dictChar
                dictChar.pop('Items', None)

                #Get Key data
                await WFH.getKeyData(aChar, dictChar)
                #await WFH.getAAData(aChar, dictChar)
                #await WFH.getSkillData(aChar, dictChar)

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

            print("Finished for loop of each character")

            #begin error trap for previous dump
            while True:
              try:
                #Upload previous dump (newestGuildDUmp) to previous dump
                print("Upload previous dump to previous dump")
                await repDB.setGuildProperty(ctx, "PreviousGuildDump", newestGuildDump)
                print("Upload complete")
                break
              except:
                print("Failed to upload previous dump:")
                break
                

            #begin error trap for newest dump
            while True:
              try:
                #Upload guild dump just built to newest dump
                print("Upload newest dump that was just created")
                await repDB.setGuildProperty(ctx, "NewestGuildDump", buildingDump)
                print("Upload complete")
                break
              except:
                print("Failed to upload newest dump:")
                break
            
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


  async def getChars(self, ctx, pGuild=0):
    #Get data from replitDB
    from classes.replitDB import replitDB
    repDB = replitDB()
        
    #Get newestDump from database
    newestDump = await repDB.getGuildProperty(ctx, "NewestGuildDump")
    links = await repDB.getGuildProperty(ctx, "Links")
    
    print("Looking for ({})".format((ctx.author.id)))
    
    print("pGuild = {}".format(pGuild))
    myPublicNote = ""
    #Check if guild is 1
    if pGuild == 1:
      #Use public note of Guild
      myPublicNote = 'Guild'
    else:
      #Get public note from linked magelo accounts
      arrOutput = []
      for aLink in links:      
        if aLink["DiscordMemberID"] == ctx.author.id:
          #print("Foudn it")
          myPublicNote = aLink["PublicNote"]
    
    #Check if guild has been set
    if myPublicNote == "":
      #No match
      print("No Match, need to link")
    else:
      print("myPublicNote is {}".format(myPublicNote))
      #Match found, get list of characters
      print("List of characters for {}:".format(myPublicNote))
      arrOutput = []
      for aChar in newestDump["Data"]:
        aPublicNote = newestDump["Data"][aChar]["PublicNote"].lower()
        #print("Checking {}:  {}".format(aChar, aPublicNote))

        if aPublicNote.lower() == myPublicNote.lower():
          arrOutput.append(aChar)
    
    return arrOutput
  

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

        #If a mention was passed as an argument, remove the wrappings <@!123> = 123
        pName = pName.replace('<@!', '').replace('>', '')

        #Check if public note or discord name matches
        if myPublicNote.lower() == pName.lower():
          #Build message
          myMsg = "Removed link for public note for '{}'".format(myPublicNote)
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
    print("entering who") 
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
      from GrokBotClasses.GrokBot_who import GrokBot_who
      GrokBot_who = GrokBot_who()
      myMsg = await GrokBot_who.getWho(ctx, pName)

      #Send message to channel
      await ctx.send(myMsg)

  @commands.command(name='stat', help="Outputs link stats")
  @commands.has_role("leadership")
  async def botCommand_linkstats(self, ctx, pName=""):
    myMsg = ""
    
    #Echo command and send message
    await self.echoCommand(ctx)

    from GrokBotClasses.GrokBot_who import GrokBot_who
    GrokBot_who = GrokBot_who()
    myMsg = await GrokBot_who.getRoleStatus(ctx)

    await self.largeDM(ctx, myMsg)
    
    

  @commands.command(name='aa', help="Compares two character's AAs")
  #async def botCommand_test(self, ctx, parmDays: typing.Optional[int] = 30, parmPlayer: typing.Optional[str] = None):
  async def botCommand_aa(self, ctx, pLeft: typing.Optional[str] = None, pRight: typing.Optional[str] = None):
    #Check if command too spammy
    numSec = 7
    if self.isCommandSpam(ctx, numSec):
      myMsg = "Come on {}, lets give more than {} seconds between commands".format(ctx.message.author.mention, numSec)
      await ctx.channel.send(myMsg)
    else:
      await self.echoCommand(ctx)

      myMsg = ""
      #Check to see if pLeft and pRight have data
      if not pLeft is None:
        from GrokBotClasses.GrokBot_aa import GrokBot_aa
        GrokBot_aa = GrokBot_aa(pLeft, pRight)
        myMsg = await GrokBot_aa.Output()
      else:
        #Atleast one of pLeft and pRight are None
        myMsg = "Need two valid characters as arguments"
      

      #Send DM to author
      await ctx.message.author.send(myMsg)  

  @commands.command(name='flaglist', help="Provides short names and Magelo text for all flags")
  async def botCommand_flaglist(self, ctx):
    #Check if command too spammy
    numSec = 7
    if self.isCommandSpam(ctx, numSec):
      myMsg = "Come on {}, lets give more than {} seconds between commands".format(ctx.message.author.mention, numSec)
      await ctx.channel.send(myMsg)
    else:
      await self.echoCommand(ctx)
      #Get Magelo class object
      from classes.WFH_Magelo import WFH_Magelo
      WFH = WFH_Magelo()
      myMsg = await WFH.flaglist()

      #Send DM to author
      await self.largeDM(ctx, myMsg)        