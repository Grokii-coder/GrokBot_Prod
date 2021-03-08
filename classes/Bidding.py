class Bidding():
  def __init__(self):
    self.bot = None
    self.guild = None
    self.auction = None
    self.queuedItems = {}
    self.deleteSeconds =  1800
    self.channel = {"Spam" : None, "Bids" : None, "History" : None, "inGame" : None}   


#        orgMessage = {"command" : None
#                    , "guildmate" : myGuildMate
#                    , "message" : myMessage
#                    , "dutch" : None
#                    , 'bid' : None
#                    , "channelName" : myChannel
#                    , "channelID" : message.channel.id
#        }

  def setBot(self, pBot):
    self.bot = pBot

  def setChannel(self, pChannel, pID):
    if pChannel == "Spam":
      self.channel["Spam"] = pID
    if pChannel == "Bids":
      self.channel["Bids"] = pID
    if pChannel == "History":
      self.channel["History"] = pID
    if pChannel == "inGame":
      self.channel["inGame"] = pID

  def getChannel(self, pChannel):
    if pChannel == "Spam":
      return self.channel["Spam"]
    if pChannel == "Bids":
      return self.channel["Bids"]
    if pChannel == "History":
      return self.channel["History"]
    if pChannel == "inGame":
      return self.channel["inGame"]
    else:
      return None

  async def cmdLoot(self, dMessage, pMessage):
    print("Starting cmdLoot")
    #Get item name(s) to queue up
    arrLootItemList = []
    await self.getItems(pMessage["message"], arrLootItemList)
    
    #Check to see if there is at least one item
    if len(arrLootItemList) > 0:
      print("Item Count: {}, ItemList: {}".format(len(arrLootItemList), arrLootItemList))
      
      
      #Iterate over new items to add
      for anItem in arrLootItemList:
        print("Start of for loop:  {}".format(anItem))
        #Check if auction is already running this item
        if not self.auction is None:
          if self.auction["ItemName"] == anItem:
            print("Auction running same item ({}), increase dutch".format(anItem))
            #New item to add is already the current item being bid on
            #Increase the dutch index
            self.auction["DutchIndex"] = self.auction["DutchIndex"] + 1

            #Check if bidders is less than dutch
            while len(self.auction["TopBids"]) < self.auction["DutchIndex"]:
              #add rot to self.auction["TopBids"]
              self.auction["TopBids"].append(["Rot", 0])
              self.LastBid = None

            #Output that the dutch index was increased
            myMsg = "Another instance of current auction added, increasing dutchIndex of current item"          
            await self.msgToChannel(self.channel["Bids"], myMsg, self.deleteSeconds)

            #Output new current state of bids
            myList = await self.echoTopBids()
            #Build message to send to channel
            myMsg = "{}: {}".format(self.auction["ItemName"], myList)
            #Send to channel:
            await self.msgToChannel(self.channel["Bids"], myMsg, self.deleteSeconds)
            await self.echoBidDone(myMsg, dMessage.created_at) 
        
        #Auction isn't already running this item
        #Check if item is already in the queue
        if anItem in self.queuedItems:
          #Increment the count of this item
          print("Auction not running, item ({}) already queued, add to it".format(anItem))
          self.queuedItems[anItem] = 1 + self.queuedItems[anItem]
        else:
          #Enter the new item with count of 1
          print("Auction not running, item ({}) not in queue, add it".format(anItem))
          self.queuedItems[anItem] = 1

      #Write queued items to channel
      await self.printQueued()

      #Check if an auction is NOT running
      if self.auction is None:
        #Open bidding for a queue'd item
        await self.parseOpen(pMessage["guildmate"], dMessage.created_at)

           
  async def cmdCancel(self, dMessage, pMessage):
    print("Starting cmdCancel")
    if self.auction == None:
      myMsg = "No active auction, cannot cancel it"
      await self.msgToChannel(self.channel["Bids"], myMsg, self.deleteSeconds) 
    else:
      print("Entered cancel")
      #Build message to send to channel
      myMsg = "Auction for {} cancelled by {}".format(self.auction["ItemName"], pMessage["guildmate"])
      
      #Send to channel:
      await self.msgToChannel(self.channel["Bids"], myMsg, self.deleteSeconds)

      #Cancel the auction
      self.auction = None
      self.LastBid = None

      #Try to open a new item
      await self.parseOpen(pMessage["guildmate"], dMessage.created_at)

  async def checkForDutch(self):
    print("Starting Dutch check")
    if not self.auction == None:
      print("Entered dutch")
      myDutchParam = pMessage["dutch"]

    #Iterate over all the items

    if 1==2:
      #Check if requested dutch level is greater than current
      if myDutchParam > self.auction["DutchIndex"]:
        #Update to new dutch value
        myMsg = "Changing dutch from {} to {} for current auction of {}".format(self.auction["DutchIndex"], myDutchParam, self.auction["ItemName"])
        self.auction["DutchIndex"] = myDutchParam
      else:
        #Throw error, cannot make the dutch value less
        myMsg = "Dutch value currently {} for item {}, cannot lower it to requested value of {}".format(self.auction["DutchIndex"], self.auction["ItemName"], myDutchParam)
      #Write response to channel                
      await self.msgToChannel(self.channel["Bids"], myMsg, self.deleteSeconds)

  async def cmdRollback(self, dMessage, pMessage):
    print("Starting cmdRollback")
    if self.auction == None:
      myMsg = "No active auction, cannot roll it back"
      await self.msgToChannel(self.channel["Bids"], myMsg, self.deleteSeconds)
    else:
      #Check if there are no bids
      if(len(self.auction["TopBids"]) == 0):
        #Cannot roll back, build message
        myMsg = "Rollback by {}, Cannot rollback, currently no bids".format(pMessage["guildmate"])
      #Check if there is only one bid in history
      elif(len(self.auction["History"]) == 1):
        #Only one item in history, clear current bid and history
        self.auction["History"].pop()
        self.auction["TopBids"].pop()

        #Build message
        myMsg = "Rollback by {}\r{}: No bids, currently rotting".format(pMessage["guildmate"], self.auction["ItemName"])
      else:
        #Remove last bid from the history
        self.auction["History"].pop()
        #Get last good bid
        lastGood = self.auction["History"].pop()

        #Set last good bid to TopBids and back into History
        self.auction["TopBids"] = lastGood
        self.auction["History"].append(lastGood)

        #Get list of current top bidders  
        myList = await self.echoTopBids()

        #Build message to send to channel
        myMsg = "Rollback by {}\r{}: {}".format(pMessage["guildmate"], self.auction["ItemName"], myList)
      
      #Send the message built to the channel:
      await self.msgToChannel(self.channel["Bids"], myMsg, self.deleteSeconds)

  async def cmdClose(self, dMessage, pMessage):
    print("Starting cmdClose")
    #Calculate the time since last bid
    secSinceLastBid = abs(dMessage.created_at - self.LastBid).seconds
    
    if self.auction == None:
      myMsg = "{} tried to !close.  No active auction, cannot close it".format(pMessage["guildmate"])
      await self.msgToChannel(self.channel["Bids"], myMsg, self.deleteSeconds)
    elif secSinceLastBid <= 10:              
      myMsg = "{} tried to !close.  Less than 10 seconds since last bid, cannot close it".format(pMessage["guildmate"])
      await self.msgToChannel(self.channel["Bids"], myMsg, self.deleteSeconds)
    else:
      #Write auction to the db
        #Need to have a raid start command to get date of raid
        #Dictionary {"Raid" : "RaidDateTime", "DKP" : []}
        #Each auction added to an array of auctions named DKP?

      #Check if bidders is less than dutch
      while len(self.auction["TopBids"]) < self.auction["DutchIndex"]:
        #add rot to self.auction["TopBids"]
        self.auction["TopBids"].append(["Rot", 0])

      #Get list of winner(s)
      myList = await self.echoTopBids()

      #Create two line message with congrats
      myMsgClosedBy = "Auction closed by {}".format(pMessage["guildmate"])
      myMsg = "Grats on {}: {}".format(self.auction["ItemName"], myList)

      #Write messages to discord      
      await self.msgToChannel(self.channel["Bids"], myMsgClosedBy, self.deleteSeconds)
      await self.msgToChannel(self.channel["Bids"], myMsg, self.deleteSeconds)
      await self.msgToChannel(self.channel["History"], myMsg)

      #Close the auction
      self.auction = None
      self.LastBid = None

      #Check to see if there are new items to queue
      if len(self.queuedItems) > 0:
        #Open a new item
        await self.parseOpen(pMessage["guildmate"], dMessage.created_at)

  async def cmdBid(self, dMessage, pMessage):
    print("Starting cmdBid")

    #Set variables from parameters    
    pGuildMate = pMessage["guildmate"]    
    pBid = int(pMessage["bid"])
    pLastBidCreatedAt = dMessage.created_at

    #Check if self.auction is ready to run an auction
    if self.auction is None:
      myMsg = "cmdBid: Auction not running, do nothing"
      print(myMsg)
    else:
      print("Auction Running")
      #Check to see if number of bids is less than DutchIndex
      if len(self.auction["TopBids"]) < self.auction["DutchIndex"]:
        print("cmdBid: number of bids is less than DutchIndex")
        #No competition, Add bid to TopBids and History
        await self.addBid([pGuildMate, pBid], pLastBidCreatedAt)
        print("No competition, Add bid to TopBids and History")  

        #Get list of current top bidders  
        myList = await self.echoTopBids()
        #Build message to send to channel
        myMsg = "{}: {}".format(self.auction["ItemName"], myList)
        #Send to channel:
        await self.msgToChannel(self.channel["Bids"], myMsg, self.deleteSeconds)

        #Update the LastBid variable and start echo for bidding done
        self.LastBid = pLastBidCreatedAt          
        await self.echoBidDone(pLastBidCreatedAt, myMsg)        
      else:
        print("cmdBid: Bids are full")
        #Bids are full, see if this is higher than the lowest bid

        #Set default values for lowBid and lowIndex
        lowBid = 10000
        lowIndex = -1

        #Loop through TopBids and set lowBid and lowIndex
        for i, aBid in enumerate(self.auction["TopBids"]):
          #Get bidder name and their bid          
          loopBid = aBid[1]
          
          #Check if lowBid is lower than or equal to loopBid
          if lowBid >= loopBid:
            print("Setting lowbid to loopbid!")
            lowBid = loopBid
            lowIndex = i
        
        print("cmdBid: Check to see if pBid is higher than the lowest TopBid")
        #Check to see if pBid is higher than the lowest TopBid
        if pBid > lowBid:
          print("cmdBid: Bid is higher, remove lowBid")
          #Remove lowBid
          self.auction["TopBids"].pop(lowIndex)
          
          #Add bid to TopBids and History
          await self.addBid([pGuildMate, pBid], pLastBidCreatedAt)

          #Get list of current top bidders  
          myList = await self.echoTopBids()

          #Build message to send to channel
          myMsg = "{}: {}".format(self.auction["ItemName"], myList)

          #Send to channel:
          await self.msgToChannel(self.channel["Bids"], myMsg, self.deleteSeconds)

          #Update the LastBid variable and start echo for bidding done
          self.LastBid = pLastBidCreatedAt          
          await self.echoBidDone(pLastBidCreatedAt, myMsg)          
        else:
          print("cmdBid: Weak bid")   
          myMsg = "{} had a weak bid of {}, cannot add it".format(pGuildMate, pBid)
          await self.msgToChannel(self.channel["Bids"], myMsg, self.deleteSeconds)
          print(myMsg)

  async def cmdNonDkp(self, dMessage, pMessage):

    #Set encounter and raid leader from pMessage object
    myRaidLeader = pMessage["guildmate"]
    myEncounter = pMessage["message"].replace('!nondkp ', '').replace('!nondkp', '')
    myRollCount = 0
    myMsg = ""
    
    #Check to see if encounter is blank
    if myEncounter == '':
      myEncounter = "nondkploot command error, No Encounter Specified"
      await self.msgToChannel(self.channel["Bids"], myEncounter, 60)
    else:
      #Loop through each voice channel in a guild
      for aChannel in dMessage.guild.voice_channels:
        print(aChannel.id, aChannel)
        import random

        #Get channel object by id
        myChannel = self.bot.get_channel(aChannel.id)

        #Get the number of people are in the channel
        population = len(myChannel.members)

        #Check if population is greater than 1
        if population > 1:
          #Found people in a voice channel, increment roll count
          myRollCount = myRollCount + 1
          #Get a roll for each discord voice connection
          rolls = random.sample(range(0, 100), len(myChannel.members))

          #Create collection for member and roll
          myRoll = {}

          #Iterate through members
          for aMember in myChannel.members:
            #If nick, use it, otherwise name
            if aMember.nick is None:
              myName = aMember.name
            else:
              myName = aMember.nick
            
            
            #Assign roll to person
            myRoll[rolls.pop()] = myName

          #Build a message
          myHeader = "{} - {} - {}\r".format(aChannel, myRaidLeader, myEncounter)
          await self.msgToChannel(self.channel["Bids"], myHeader)

          for aRoll in myRoll:
            myOneRoll = "{} rolls a {}".format(myRoll[aRoll], aRoll)
            await self.msgToChannel(self.channel["Bids"], myOneRoll)


          for count, aRoll in enumerate(sorted(myRoll, reverse=True)):
            myMsg += "{}) {} [{}]  ".format(count+1, myRoll[aRoll] ,aRoll)
            #myMsg += "{}-{}    ".format(aRoll, dkpRoll[aRoll])
            #myMsg += "{})-{}, ".format(aRoll, dkpRoll[aRoll])
            #myMsg += "{}) {}  ".format(count+1, dkpRoll[aRoll])
            #1) huffin (97)  2) Grokii (79)  3) Malk (38)  4) Kohelm (33)  5) Jams (13)


      if myRollCount == 0:
        myMsg = "!nondkp command failed, no one in any voice channels"
        await self.msgToChannel(self.channel["Bids"], myMsg, 60)
      else:
        await self.msgToChannel(self.channel["Bids"], myMsg)
        
      

  async def cmdTest(self, dMessage, pMessage):

    print(pMessage)
    print(pMessage["command"])
    print(pMessage["guildmate"])
    print(pMessage["message"])
    print(pMessage["arrMsg"])
    print(pMessage["channelName"])
    print(pMessage["channelID"])

    #await self.synthesize_text("Hello World!")
    
    #for aChannel in myGuild.voice_channels:
    #  print(aChannel.id, aChannel)
    #  if aChannel.id == 650875260618407956:
    #    aChannel.send("Hello", tts=True)
        

        #Either use this bot or rip code from this bot
        #https://github.com/Gnome-py/Discord-TTS-Bot/blob/master/cogs/events_main.py

    #from gtts import gTTS
    #Try this answer:
    #https://stackoverflow.com/questions/62494399/how-to-play-gtts-mp3-file-in-discord-voice-channel-the-user-is-in-discord-py
    
    #await client.send_message(message.channel, "3\n2\n\1\nTime's up!", tts=True)


    #https://stackoverflow.com/questions/58614450/is-there-a-module-that-allows-me-to-make-python-say-things-as-audio-through-the


  async def echoBidDone(self, pMyDateTime, pMsg):
    import asyncio

    #Wait for 30 seconds        
    await asyncio.sleep(30)
    
    #See if this bid is still the top bid
    if pMyDateTime == self.LastBid:
      #It is the top bid, send message
      myMsg = "Closing soon:  {}".format(pMsg)
      #print(myMsg)
      await self.msgToChannel(self.channel["Bids"], myMsg, self.deleteSeconds)
      await self.echoBidDone(pMyDateTime, pMsg)

  #Send a message to a specific channel
  async def msgToChannel(self, pChannelID, pMsg, pPurge = 0):
    print(pMsg)
    myChannel = self.bot.get_channel(pChannelID)
    if pPurge > 0:
      await myChannel.send(pMsg, delete_after=pPurge)
    else:
      await myChannel.send(pMsg)
    
  async def echoTopBids(self):
    myOutput = ""

    #Loop through TopBids and set lowBid and lowIndex
    for i, aBid in enumerate(self.auction["TopBids"]):
      loopBidder = aBid[0]
      loopBid = aBid[1]

      if i>0:
        myOutput += ", "
      myOutput += "{} at {} dkp".format(loopBidder, loopBid)
    
    if myOutput == "":
      myOutput = "rot"

    return myOutput

  async def addBid(self, pBid, pLastBidCreatedAt):
    #Update the new topbid       
    self.auction["TopBids"].append(pBid)
    
    #Update history with a copy of the current state of topbid
    self.auction["History"].append(self.auction["TopBids"].copy())

  

  async def getItems(self, pMessage, pItemList):
    #Check to see if text surrounded by ( is in the message:
    if "(" in pMessage and ")" in pMessage:
      #Get item name by splitting by (
      myItemName = pMessage.split("(")[1]
      #Trim off )
      myItemName = myItemName.split(")")[0]

      pItemList.append(myItemName)

      #Remove this item name from the message
      pMessage = pMessage.replace("({})".format(myItemName), "", 1)

      #Check to see if another item remains in the message
      if "(" in pMessage and ")" in pMessage:
        await self.getItems(pMessage, pItemList)

  async def queueItems(self, pItemList):
    pass

  async def parseOpen(self, pGuildMate, pLastBidCreatedAt):
    #Format:    !open OptInt URL (item name with spaces)
    #Examples:
    #!open 2 https://allaclone.wayfarershaven.com/?a=item&id=68199 (Timeless Coral Greatsword) 
    #!open https://allaclone.wayfarershaven.com/?a=item&id=22826 (Skydarkener)

    #Check if self.auction is ready to run an auction
    if self.auction is None and len(self.queuedItems) > 0:
      #Iterate through all items in self.queuedItems
      myItemName = ""
      for anItem in self.queuedItems:
        #Set the item name, overwriting if many items only last will remain
        myItemName = anItem

      #Set the dutchIndex for this item removing it from the dictionary
      myDutchIndex = self.queuedItems.pop(anItem)          

      #Update self.auction with this information:
      self.auction = {"OpenedAuction" : pGuildMate,
                      "ItemName" : myItemName,                      
                      "DutchIndex" : int(myDutchIndex),
                      "TopBids" : [],
                      "History" : []}
      
      #Create open message to send to channel
      myMsg = "Open for bidding _____ <<< {} >>>".format(self.auction["ItemName"])
      
      #Check if this is a dutch
      if self.auction["DutchIndex"] > 1:
        #Add dutch text to the end of the message
        myDutchMsg = " dutch x{}".format(self.auction["DutchIndex"])
        myMsg += myDutchMsg

      #Send the message
      await self.msgToChannel(self.channel["Bids"], myMsg, self.deleteSeconds)

      #Update the LastBid variable and start echo for bidding done
      self.LastBid = pLastBidCreatedAt          
      await self.echoBidDone(pLastBidCreatedAt, "No bids on {}".format(self.auction["ItemName"]))

  async def printQueued(self):
  #Build list of queued items
    myList = ""
    myCount = 0
    for anItem in self.queuedItems:
      myItemName = anItem
      myDutchIndex = self.queuedItems[anItem]

      if myCount > 0:
        myList += ", "
      
      myList += myItemName

      if myDutchIndex > 1:
        myList += "x{}".format(myDutchIndex)

      myCount = myCount + 1
    myMsg = "Queued items:  {}".format(myList)
    await self.msgToChannel(self.channel["Bids"], myMsg, self.deleteSeconds) 

  async def synthesize_text(self, text):
    import os    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./keys/GrokBot TTS-c68dba04055d.json"

    """Synthesizes speech from the input string of text."""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    with open("./mp3/open/output.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')
