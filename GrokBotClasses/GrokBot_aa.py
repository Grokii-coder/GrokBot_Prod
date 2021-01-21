class GrokBot_aa:
  def __init__(self, pLeft, pRight):
    self.Msg = ""
    self.Left = pLeft
    self.Right = pRight
    self.outputDict = None
    self.Error = None
    self.myMsg = ""
    self.defaultCleric = {"Class" : "Cleric", 
                "MageloStatus" : "Normal",
                "AA" : [
                  {"Name" : "Innate Run Speed", "Rank" : "3 of 3"},
                  {"Name" : "Spell Casting Mastery", "Rank" : "3 of 3"},
                  {"Name" : "Mental Clarity", "Rank" : "1 of 3"},
                  {"Name" : "Divine Arbitration", "Rank" : "3 of 3"},
                  {"Name" : "Healing Gift", "Rank" : "3 of 6"},
                  {"Name" : "Celestial Regeneration", "Rank" : "3 of 6"},
                  {"Name" : "Mass Group Buff", "Rank" : "1 of 1"},
                  {"Name" : "Spell Casting Reinforcement", "Rank" : "3 of 3"},
                  {"Name" : "Spell Casting Reinforcement Mastery", "Rank" : "1 of 1"},
                  {"Name" : "Healing Adept", "Rank" : "3 of 6"}]
                }


  async def Output(self):
    await self.getData()
    await self.formatOutput()    
    return self.myMsg

  async def getData(self):
    from classes.WFH_Magelo import WFH_Magelo
    WFH = WFH_Magelo()
    
    #Create dictionaries for the raw data from Magelo
    rawLeft = {}
    rawRight = {}

    #Check if only one character was sent
    if self.Right is None:
      #Set variable so we know if there was a default class setup
      classNotDefined = 0
      #Get the magelo data for the left character
      rawLeft = await WFH.getBasicData(self.Left)
      
      #Check if the magelo data has class information (not anon/rp)
      if rawLeft["MageloStatus"] == "Normal":
        if "Class" in rawLeft:
          #Check if class is Cleric
          if rawLeft["Class"] == "Cleric":
            #Update name to default raiding cleric
            self.Right = "Default Raiding Cleric"

            #Parse the data
            await self.parseData(rawLeft, self.defaultCleric)
            #Flag as class defined
            classNotDefined = 1
      else:
        self.Error = "{} ({}) must have a normal status, they cannot be Anonymous or Roleplaying to compare AAs".format(self.Left, rawLeft["MageloStatus"])

      #Check if class default not defined
      if classNotDefined == 0:
        #Return the URL for Magelo
        myURL = await WFH.getURL("aas", self.Left, 0)
        self.Error = "Only one character received, development for comparing one character to a basic set of AAs for raiding will be a future feature.\r\rHere is a link to Magelo's AA page for that character:\r{}".format(myURL)
    else:
      #Query magelo to get raw data for left and right terms
      rawLeft = await WFH.getBasicData(self.Left)
      rawRight = await WFH.getBasicData(self.Right)

      #Parse the data
      await self.parseData(rawLeft, rawRight)
      
  
  async def parseData(self, rawLeft, rawRight):
    from classes.WFH_Magelo import WFH_Magelo
    WFH = WFH_Magelo()

    #Create a processed dictionary that will contain left and right data
    aaProc = {}
    aaProc[self.Left] = {}
    aaProc[self.Right] = {}

    #Check status to see if we can get AA getBasicData
    if rawLeft["MageloStatus"] == "Normal" and rawRight["MageloStatus"] == "Normal":
      await WFH.getAAData(self.Left, rawLeft)

      if not "AA" in rawRight:
        await WFH.getAAData(self.Right, rawRight)

      #Check to see if the class is the same for left and right
      if rawLeft["Class"] == rawRight["Class"]:
        #Create output dictionary
        self.outputDict = {"ExactSame" : [], "SameLeftHigher" : [], "SameRightHigher" : [], "LeftOnly" : [], "RightOnly" : []}
        
        #Loop through left AAs:
        for leftAA in rawLeft["AA"]:            
          aaName = leftAA["Name"]
          aaRank = leftAA["Rank"]

          #Check first didgit is not 0 (examples 1 of 3, 3 of 3, 0 of 1)
          if not aaRank[0] == "0":
            #Has a rank, add it to aaProcessed list
            aaProc[self.Left][aaName] = aaRank

        #Loop through right AAs:
        for rightAA in rawRight["AA"]:            
          aaName = rightAA["Name"]
          aaRank = rightAA["Rank"]

          #Check first didgit is not 0 (examples 1 of 3, 3 of 3, 0 of 1)
          if not aaRank[0] == "0":
            #Has a rank, add it to aaProcessed list              
            aaProc[self.Right][aaName] = aaRank

        #loop through left lists
        for leftAA in aaProc[self.Left]:
          #Check to see if this AA is in the right            
          if leftAA in aaProc[self.Right]:
            #Get the rank of this AA for left and right
            leftRank = int(aaProc[self.Left][leftAA][0])
            rightRank = int(aaProc[self.Right][leftAA][0])

            #Check if ranks are equal
            if leftRank == rightRank:
              #Add to 'ExactSame' self.outputDict
              self.outputDict["ExactSame"].append({"aaName" : leftAA, "aaRank" : aaProc[self.Left][leftAA]})

            #Check if left greater than right
            elif leftRank > rightRank:
              #Add to 'SameRankDiffers' self.outputDict
              self.outputDict["SameLeftHigher"].append({"aaName" : leftAA, "aaRankLeft" : aaProc[self.Left][leftAA], "aaRankRight" : aaProc[self.Right][leftAA]})
            #Check if right greater than left
            elif leftRank < rightRank:
              #Add to 'SameRankDiffers' self.outputDict
              self.outputDict["SameRightHigher"].append({"aaName" : leftAA, "aaRankLeft" : aaProc[self.Left][leftAA], "aaRankRight" : aaProc[self.Right][leftAA]})      
          else:
            #Add to 'LeftOnly' self.outputDict
            self.outputDict["LeftOnly"].append({"aaName" : leftAA, "aaRank" : aaProc[self.Left][leftAA]})

        #loop through right lists
        for rightAA in aaProc[self.Right]:
          #Check to see if this AA is NOT in t he left
          if not rightAA in aaProc[self.Left]:
            #Add to 'RightOnly' self.outputDict
            self.outputDict["RightOnly"].append({"aaName" : rightAA, "aaRank" : aaProc[self.Right][rightAA]})

      else:
        self.Error = "{} ({}) and {} ({}) are not the same class, cannot compare AAs".format(self.Left, rawLeft["Class"], self.Right, rawRight["Class"])
    else:
      self.Error = "{} ({}) and {} ({}) must have a normal status, they cannot be Anonymous or Roleplaying to compare AAs".format(self.Left, rawLeft["MageloStatus"], self.Right, rawRight["MageloStatus"])


  async def formatOutput(self):
    #Check to see if there was an error
    if self.Error:
      self.myMsg = self.Error
    else:
      #No error, print header
      self.myMsg = "{} and {} comparison of AAs\r\r".format(self.Left, self.Right)

      #check if any AAs were the exact same
      if self.outputDict["ExactSame"]:
        self.myMsg += "AAs and ranks that are the same\r"        

        for aItem in self.outputDict["ExactSame"]:          
          self.myMsg += "{}: ({})\r".format(aItem["aaName"], aItem["aaRank"])
      
      #check if any AAs were the same, but left had higher ranks
      if self.outputDict["SameLeftHigher"]:
        self.myMsg += "\rAAs the same, but {} has more ranks\r".format(self.Left)

        for aItem in self.outputDict["SameLeftHigher"]:
          self.myMsg += "{} - {}: ({}) - {}: ({})\r".format(aItem["aaName"], self.Left, aItem["aaRankLeft"], self.Right, aItem["aaRankRight"])

      #check if any AAs were the same, but right had higher ranks
      if self.outputDict["SameRightHigher"]:
        self.myMsg += "\rAAs the same, but {} has more ranks\r".format(self.Right)

        for aItem in self.outputDict["SameRightHigher"]:
          self.myMsg += "{} - {}: ({}) - {}: ({})\r".format(aItem["aaName"], self.Left, aItem["aaRankLeft"], self.Right, aItem["aaRankRight"])

      #check if any AAs were left only
      if self.outputDict["LeftOnly"]:
        self.myMsg += "\rOnly {} has these AAs\r".format(self.Left)

        for aItem in self.outputDict["LeftOnly"]:
          self.myMsg += "{}: ({})\r".format(aItem["aaName"], aItem["aaRank"])

      #check if any AAs were right only
      if self.outputDict["RightOnly"]:
        self.myMsg += "\rOnly {} has these AAs\r".format(self.Right)

        for aItem in self.outputDict["RightOnly"]:
          self.myMsg += "{}: ({})\r".format(aItem["aaName"], aItem["aaRank"])
