from discord.ext import commands

def whatIs(myObj):
  print(type(myObj))
  for stuff in dir(myObj):
    print(stuff)

def setup(paramBot):
  paramBot.add_cog(GrokBotBidding(paramBot))

class GrokBotBidding(commands.Cog):
  def __init__(self, paramBot):
    self.bot = paramBot
    self.auction = None
    self.queuedItems = {}
    self.deleteSeconds =  1800

  @commands.Cog.listener()
  async def on_message(self, message):
    import re

    #Check if the message was NOT made by the bot itself
    if message.author != self.bot.user:
      
      #Echo message and channel id
      myMsg = "{} ({}:{})".format(message.content, message.channel.name, message.channel.id, )
      #echo message
      print(myMsg)
      #print(message.content)

      #Check if the message was made to 'in-game-chat' channel id 690269605524013127
      if message.channel.id == 690269605524013127:
        #Parse the name of the person saying the message
        pattern = "\*\*(.*) guild:\*\* (.*)"
        result = re.search(pattern, message.content)
        myGuildMate = result.group(1)
        myMessage = result.group(2)
        #print(myGuildMate)
        #print(myMessage)

        #Split message by space
        arrMsg = myMessage.split()
     
        #Check to see if the first character starts with !
        if myMessage[0] == '!':
          #Set the command name to lowercase                        
          myCommand = arrMsg[0].lower() 
          print("myCommand is ({})".format(myCommand))

          #Check to see if the command is open
          if myCommand == "!loot" and len(arrMsg) >= 3:
            #Get item name(s) to queue up
            arrLootItemList = []
            await self.getItems(myMessage, arrLootItemList)            
            
            #Check to see if there is at least one item
            if len(arrLootItemList) > 0:
              print(arrLootItemList)
              #Queue the items
              await self.queueItems(arrLootItemList)

              #Write queued items to channel
              await self.printQueued()

              #Check to see if an item is open
              if self.auction == None:            
                #Open bidding for this item
                await self.parseOpen(myGuildMate, message.created_at)

            else:
              myMsg = "Couldn't parse any items from !loot command\r{}".format(myMessage)
              await self.msgToChannel(781591411094454273, myMsg, self.deleteSeconds) 
              
          elif myCommand == "!cancel":
            if self.auction == None:
              myMsg = "No active auction, cannot cancel it"
              await self.msgToChannel(781591411094454273, myMsg, self.deleteSeconds) 
            else:
              print("Entered cancel")
              #Build message to send to channel
              myMsg = "Auction for {} cancelled by {}".format(self.auction["ItemName"], myGuildMate)
              
              #Send to channel:
              await self.msgToChannel(781591411094454273, myMsg, self.deleteSeconds)   
              #Cancel the auction
              self.auction = None
              #Try to open a new item
              await self.parseOpen(myGuildMate, message.created_at)

          elif myCommand == "!dutch":
            if self.auction == None:
              myMsg = "No active auction, cannot change dutch value"
              await self.msgToChannel(781591411094454273, myMsg, self.deleteSeconds) 
            else:
              print("Entered dutch")
              myDutchParam = arrMsg[1]
              #Check if parameter after dutch is a number              
              if myDutchParam.isdigit():
                #Convert to integer
                myDutchParam = int(myDutchParam)

                #Check if requested dutch level is greater than current
                if myDutchParam > self.auction["DutchIndex"]:
                  #Update to new dutch value
                  myMsg = "Changing dutch from {} to {} for current auction of {}".format(self.auction["DutchIndex"], myDutchParam, self.auction["ItemName"])
                  self.auction["DutchIndex"] = myDutchParam
                else:
                  #Throw error, cannot make the dutch value less
                  myMsg = "Dutch value currently {} for item {}, cannot lower it to requested value of {}".format(self.auction["DutchIndex"], self.auction["ItemName"], myDutchParam)
                #Write response to channel                
                await self.msgToChannel(781591411094454273, myMsg, self.deleteSeconds)

          elif myCommand == "!rollback":
            if self.auction == None:
              myMsg = "No active auction, cannot roll it back"
              await self.msgToChannel(781591411094454273, myMsg, self.deleteSeconds) 
            else:
              #Check if there are no bids
              if(len(self.auction["TopBids"]) == 0):
                #Cannot roll back, build message
                myMsg = "Rollback by {}, Cannot rollback, currently no bids".format(myGuildMate)              
              #Check if there is only one bid in history
              elif(len(self.auction["History"]) == 1):
                #Only one item in history, clear current bid and history
                self.auction["History"].pop()
                self.auction["TopBids"].pop()

                #Build message
                myMsg = "Rollback by {}\r{}: No bids, currently rotting".format(myGuildMate, self.auction["ItemName"])
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
                myMsg = "Rollback by {}\r{}: {}".format(myGuildMate, self.auction["ItemName"], myList)
              
              #Send the message built to the channel:
              await self.msgToChannel(781591411094454273, myMsg, message.created_at) 

          elif myCommand == "!close":            
            #Calculate the time since last bid
            secSinceLastBid = abs(message.created_at - self.LastBid).seconds
            
            if self.auction == None:
              myMsg = "{} tried to !close.  No active auction, cannot close it".format(myGuildMate)
              await self.msgToChannel(781591411094454273, myMsg, self.deleteSeconds)
            elif secSinceLastBid <= 10:              
              myMsg = "{} tried to !close.  Less than 10 seconds since last bid, cannot close it".format(myGuildMate)
              await self.msgToChannel(781591411094454273, myMsg, self.deleteSeconds)
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
              myMsg = "Auction closed by {}\r".format(myGuildMate)
              myMsg += "Grats on {}: {}".format(self.auction["ItemName"], myList)

              await self.msgToChannel(781591411094454273, myMsg)

              #Close the auction
              self.auction = None
              self.LastBid = None

              #Check to see if there are new items to queue
              if len(self.queuedItems) > 0:
                #Open a new item
                await self.parseOpen(myGuildMate, message.created_at)

        #Check to see if this is a bid
        elif len(arrMsg) == 1 and arrMsg[0].isdigit():
          await self.parseBid(myGuildMate, myMessage, int(arrMsg[0]), message.created_at)

  async def echoBidDone(self, pMyDateTime, pMsg):
    import asyncio

    #Wait for 30 seconds        
    await asyncio.sleep(30)
    
    #See if this bid is still the top bid
    if pMyDateTime == self.LastBid:
      #It is the top bid, send message
      myMsg = "Closing soon:  {}".format(pMsg)
      #print(myMsg)
      await self.msgToChannel(781591411094454273, myMsg)
      await self.echoBidDone(pMyDateTime, pMsg)
    else:
      print("Newer bid, do nothing")
    
    

  #Send a message to a specific channel
  #grok-bot-spam is 781591411094454273
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

  async def parseBid(self, pGuildMate, pGuildMessage, pBid, pLastBidCreatedAt):
    print("parseBid started")
    #Check if self.auction is ready to run an auction
    if self.auction is None:
      myMsg = "Auction not running, do nothing"
      print(myMsg)
    else:
      #Check to see if number of bids is less than DutchIndex
      if len(self.auction["TopBids"]) < self.auction["DutchIndex"]:
          #No competition, Add bid to TopBids and History
          await self.addBid([pGuildMate, pBid], pLastBidCreatedAt)
          print("No competition, Add bid to TopBids and History")  

          #Get list of current top bidders  
          myList = await self.echoTopBids()
          #Build message to send to channel
          myMsg = "{}: {}".format(self.auction["ItemName"], myList)
          #Send to channel:
          await self.msgToChannel(781591411094454273, myMsg, self.deleteSeconds)

          #Update the LastBid variable and start echo for bidding done
          self.LastBid = pLastBidCreatedAt          
          await self.echoBidDone(pLastBidCreatedAt, myMsg)        
      else:
        #Bids are full, see if this is higher than the lowest bid

        #Set default values for lowBid and lowIndex
        lowBid = 10000
        lowIndex = -1

        #Loop through TopBids and set lowBid and lowIndex
        for i, aBid in enumerate(self.auction["TopBids"]):
          #Get bidder name and their bid          
          loopBid = aBid[1]
          #print("lowBid ({}) loopBid ({})".format(lowBid, loopBid))
          #Check if lowBid is lower than or equal to loopBid
          if lowBid >= loopBid:
            print("Setting lowbid to loopbid!")
            lowBid = loopBid
            lowIndex = i
        #print("lowBid ({}) pBid ({})".format(lowBid, pBid))
        #Check to see if pBid is higher than the lowest TopBid
        if pBid > lowBid:
          #Remove lowBid
          #print("Remove low bid (next two lines)")
          #print(self.auction["TopBids"])
          self.auction["TopBids"].pop(lowIndex)
          #print(self.auction["TopBids"])
          
          #Add bid to TopBids and History
          await self.addBid([pGuildMate, pBid], pLastBidCreatedAt)

          #Get list of current top bidders  
          myList = await self.echoTopBids()
          #Build message to send to channel
          myMsg = "{}: {}".format(self.auction["ItemName"], myList)
          #Send to channel:
          await self.msgToChannel(781591411094454273, myMsg, self.deleteSeconds)

          #Update the LastBid variable and start echo for bidding done
          self.LastBid = pLastBidCreatedAt          
          await self.echoBidDone(pLastBidCreatedAt, myMsg)          
        else:   
          myMsg = "{} had a weak bid of {}, cannot add it".format(pGuildMate, pBid)
          await self.msgToChannel(781591411094454273, myMsg, self.deleteSeconds)
          print(myMsg)
    print("parseBid ending")          
    #print(self.auction["TopBids"])

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
    #Iterate over new items to add
    for anItem in pItemList:
      #Check to see if this item is already in self.queuedItems
      if anItem in self.queuedItems:
        #Increment the count of this item
        self.queuedItems[anItem] = 1 + self.queuedItems[anItem]
      else:
        #Enter the new item with count of 1
        self.queuedItems[anItem] = 1

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
      await self.msgToChannel(781591411094454273, myMsg, self.deleteSeconds)

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
    await self.msgToChannel(781591411094454273, myMsg, self.deleteSeconds) 