class GrokBot_bidding():
  def __init__(self):
    self.guild = None
    self.auction = None
    self.queuedItems = {}
    self.deleteSeconds =  1800
    self.channel = {"Spam" : None, "Bids" : None, "History" : None, "inGame" : None}

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


  async def bidding_Loot(self, ctx, pName):
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
