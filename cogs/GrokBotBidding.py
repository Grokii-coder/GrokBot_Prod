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

  @commands.Cog.listener()
  async def on_message(self, message):
    import re

    #Check if the message was NOT made by the bot itself
    if message.author != self.bot.user:
      
      #Echo message and channel id
      myMsg = "New message in channel ({}) with ID ({})".format(message.channel.name, message.channel.id)
      #echo message
      print(myMsg)
      print(message.content)

      #Check if the message was made to 'in-game-chat' channel id 690269605524013127
      if message.channel.id == 690269605524013127:
        #Parse the name of the person saying the message
        pattern = "\*\*(.*) guild:\*\* (.*)"
        result = re.search(pattern, message.content)
        myGuildMate = result.group(1)
        myMessage = result.group(2)
        print(myGuildMate)
        print(myMessage)

        #Split message by space
        arrMsg = myMessage.split()
     
        #Check to see if the first character starts with !
        if myMessage[0] == '!':
          #Set the command name to lowercase                        
          myCommand = arrMsg[0].lower() 
          print("myCommand is ({})".format(myCommand))

          #Check to see if the command is open
          if myCommand == "!open" and len(arrMsg) >= 3:
            #Check to see if an item is open
            if self.auction == None:    
              await self.parseOpen(myGuildMate, myMessage, arrMsg)
            else:
              myMsg = "Auction already running, cannot open another"
              await self.msgToChannel(781591411094454273, myMsg) 
          elif myCommand == "!cancel":
            if self.auction == None:
              myMsg = "No active auction, cannel cancel it"
              await self.msgToChannel(781591411094454273, myMsg) 
            else:
              print("Entered cancel")
              #Build message to send to channel
              myMsg = "Auction for {} cancelled by {}".format(self.auction["ItemName"], myGuildMate)
              print(myMsg)
              #Send to channel:
              await self.msgToChannel(781591411094454273, myMsg)   
              #Cancel the auction
              self.auction = None
          elif myCommand == "!close":
            if self.auction == None:
              myMsg = "No active auction, cannel cancel it"
              await self.msgToChannel(781591411094454273, myMsg) 
            else:
              #Write auction to the db
                #Need to have a raid start command to get date of raid
                #Dictionary {"Raid" : "RaidDateTime", "DKP" : []}
                #Each auction added to an array of auctions named DKP?

              #Get list of winner(s)
              myList = await self.echoTopBids()

              #Create two line message with congrats
              myMsg = "Auction closed by {}\r".format(myGuildMate)
              myMsg += "/gu Grats on {}: {}".format(self.auction["ItemName"], myList)

              await self.msgToChannel(781591411094454273, myMsg)

              #Close the auction
              self.auction = None

        #Check to see if this is a bid
        elif len(arrMsg) == 1 and arrMsg[0].isdigit():
          await self.parseBid(myGuildMate, myMessage, int(arrMsg[0]))

  #Send a message to a specific channel
  #grok-bot-spam is 781591411094454273
  async def msgToChannel(self, pChannelID, pMsg):
    print(pMsg)
    myChannel = self.bot.get_channel(pChannelID)
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


  async def parseBid(self, pGuildMate, pGuildMessage, pBid):
    print("parseBid started")
    print(pGuildMessage)
    #Check if self.auction is ready to run an auction
    if self.auction is None:
      myMsg = "Auction not running, do nothing"
      print(myMsg)
    else:
      #Check to see if number of bids is less than DutchIndex
      if len(self.auction["TopBids"]) < self.auction["DutchIndex"]:
          #No competition, Add bid to TopBids and History
          self.auction["TopBids"].append([pGuildMate, pBid])
          self.auction["History"].append([pGuildMate, pBid])
          print("No competition, Add bid to TopBids and History")  

          #Get list of current top bidders  
          myList = await self.echoTopBids()
          #Build message to send to channel
          myMsg = "{}: {}".format(self.auction["ItemName"], myList)
          #Send to channel:
          await self.msgToChannel(781591411094454273, myMsg)          
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
          self.auction["TopBids"].append([pGuildMate, pBid])
          self.auction["History"].append([pGuildMate, pBid])

          #Get list of current top bidders  
          myList = await self.echoTopBids()
          #Build message to send to channel
          myMsg = "{}: {}".format(self.auction["ItemName"], myList)
          #Send to channel:
          await self.msgToChannel(781591411094454273, myMsg)
        else:   
          myMsg = "{} had a weak bid of {}, cannot add it".format(pGuildMate, pBid)
          await self.msgToChannel(781591411094454273, myMsg)
          print(myMsg)
    print("parseBid ending")          
    #print(self.auction["TopBids"])

  async def parseOpen(self, pGuildMate, pGuildMessage, pArrOpen):       
    #Format:    !open OptInt URL (item name with spaces)
    #Examples:
    #!open 2 https://allaclone.wayfarershaven.com/?a=item&id=68199 (Timeless Coral Greatsword) 
    #!open https://allaclone.wayfarershaven.com/?a=item&id=22826 (Skydarkener)

    #Check if self.auction is ready to run an auction
    if self.auction is None:
      #Set myDutchIndex (1 if no index given)
      myDutchIndex = pArrOpen[1]

      if myDutchIndex.isdigit():
        myUrl = pArrOpen[2]
      else:
        myDutchIndex = 1
        myUrl = pArrOpen[1]

      #Get item name by splitting by (
      myItemName = pGuildMessage.split("(")[1]
      #Trim off )
      myItemName = myItemName.split(")")[0]

      #Update self.auction with this information:
      self.auction = {"OpenedAuction" : pGuildMate,
                      "ItemName" : myItemName,
                      "ItemURL" : myUrl,
                      "DutchIndex" : int(myDutchIndex),
                      "TopBids" : [],
                      "History" : []}
      myMsg = "New auction started by {} for {}".format(self.auction["OpenedAuction"], self.auction["ItemName"])
      if self.auction["DutchIndex"] > 1:
        myDutchMsg = " dutch x{}".format(self.auction["DutchIndex"])
        myMsg += myDutchMsg
      await self.msgToChannel(781591411094454273, myMsg)
    else:
      myMsg = "Auction already running for ({}), cannot start a new auction".format(self.auction["ItemName"])
      await self.msgToChannel(781591411094454273, myMsg)
