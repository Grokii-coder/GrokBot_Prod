


def whatIs(myObj):
  print(type(myObj))
  for stuff in dir(myObj):
    print(stuff)

class WFH_Magelo:
  def __init__(self):
    self.baseUrl = "https://magelo.wayfarershaven.com/index.php"

    self.pagecontent = {
      "character" : "LEVEL",
      "aas" : "AA_POINTS",
      #{"DIETITLE":"Keys","TEXT":"This character has no keys on the keyring"}
      "keys" : "keys",
      "skills" : "section",
      "flags" : "mainhead",
      "guild" : "GUILD_NAME"
      }
    self.majorKeys = {
      "Key of Veeshan" : "Veeshan's Peak",
      "Sleeper's Key" : "Kerafyrm's Lair",
      "The Scepter of Shadows" : "Vex Thal",
      "Ring of the Shissar" : "Ssraeshza Emperor's Chamber"
      }


    self.popFlag = {
    "PreFlag Hedge":{"Text":"You have said 'Tortured by nightmares' to Adroha Jezith, in the Plane of Tranquility sick bay.","Requirement":[],"Level":46},
    "Hedge":{"Text":"You have killed the construct of nightmares in the Hedge event in the Plane of Nightmare.","Requirement":["PreFlag Hedge"]},
    "PreFlag PoJ Trial":{"Text":"You have talked to Mavuin, and have agreed to plea his case to The Tribunal.","Requirement":[],"Level":46},
    "PostFlag PoJ Trial 1":{"Text":"You have showed the Tribunal the mark from the trail you have completed.","Requirement":["PreFlag PoJ Trial"]},
    "PostFlag PoJ Trial 2":{"Text":"You have returned to Mavuin, letting him know the tribunal will hear his case.","Requirement":["PostFlag PoJ Trial 1"]},
    "Terris Thule":{"Text":"You have killed Terris Thule.","Requirement":["Hedge"]},
    "PostFlag Terris Thule":{"Text":"You have hailed Elder Poxbourne in the Plane of Tranquility after defeating Terris Thule.","Requirement":["Terris Thule"]},
    "PreFlag Grummus":{"Text":"You have talked to Adler Fuirstel outside of the Plane of Disease.","Requirement":[],"Level":46},
    "Grummus":{"Text":"You have defeated Grummus","Requirement":["PreFlag Grummus"], "Level":46},
    "PostFlag Grummus":{"Text":"You have talked to Elder Fuirstel in the plane of Tranquility sick bay.","Requirement":["Grummus"]},
    "PreFlag BoT":{"Text":"You have shown your prowess in battle to Askr, now you must make strides to get to the Bastion of Thunder.","Requirement":["PreFlag PoJ Trial"]},
    "BoT Flag":{"Text":"You have obtained the Talisman of Thunderous Foyer from Askr.","Requirement":["PreFlag BoT"]},
    "Agnarr":{"Text":"You have defeated Agnarr, the Storm Lord.","Requirement":["BoT Flag"],"Level":62},
    "AerinDar":{"Text":"You have defeated the prysmatic dragon, Aerin`Dar within the Plane of Valor.","Requirement":["PostFlag PoJ Trial 2"],"Level":55},
    "HoH Trial, RD":{"Text":"You have completed Trydan Faye's trial by defeating Rydda'Dar.","Requirement":["AerinDar"],"Level":62},
    "HoH Trial, Villagers":{"Text":"You have completed Rhaliq Trell's trial by saving the villagers.","Requirement":["AerinDar"],"Level":62},
    "HoH Trial, Maidens":{"Text":"You have completed Alekson Garn's trial by protecting the maidens.","Requirement":["AerinDar"],"Level":62},
    "Carpryn Cycle":{"Text":"You have completed the Carpryn cycle within Ruins of Lxanvom.","Requirement":["PostFlag Grummus"],"Level":55},
    "Bertox":{"Text":"You have killed Bertox within the Crypt of Decay.","Requirement":["Carpryn Cycle"]},
    "PostFlag Bertox":{"Text":"You have hailed Elder Fuirstel in the Plane of Tranquility after defeating Bertox.","Requirement":["Bertox"]},
    "PreFlag Keeper of Sorrows":{"Text":"You have said 'I will go' to Fahlia Shadyglade in the Plane of Tranquility","Requirement":["PostFlag Bertox", "PostFlag Terris Thule"]},
    "Saryrn":{"Text":"You have killed Saryrn.","Requirement":["PreFlag Keeper of Sorrows"]},
    "Keeper of Sorrows":{"Text":"You have killed The Keeper of Sorrows.","Requirement":["PreFlag Keeper of Sorrows"]},
    "PostFlag Saryrn and KoS":{"Text":"You have hailed Fahlia Shadyglade after defeating The Keeper of Sorrows and Saryrn.","Requirement":["Saryrn", "Keeper of Sorrows"]},
    "Ralloz Zek":{"Text":"You have killed Ralloz Zek the Warlord.","Requirement":["MB"]},
    "Lord Mithaniel Marr":{"Text":"You have defeated Lord Mithaniel Marr within his temple.","Requirement":["HoH Trial, Maidens", "HoH Trial, Villagers", "HoH Trial, RD"]},
    "PreFlag Elementals":{"Text":"You have spoken with the grand librarian to receive access to the Elemental Planes.","Requirement":["BoT Flag", "Agnarr", "Lord Mithaniel Marr", "Ralloz Zek", "Vallon Zek", "Tallon Zek"]},
    "PreFlag MB":{"Text":"You have told Giwin Mirakon, 'I will test the machine' within the Plane of Innovation factory.","Requirement":[],"Level":46},
    "MB":{"Text":"You have defeated the Behemoth within Plane of Innovation and then QUICKLY hailed Giwin Mirakon in the factory.","Requirement":["PreFlag MB"],"Level":46},
    "Tallon Zek":{"Text":"You have killed Tallon Zek.","Requirement":["MB"]},
    "Vallon Zek":{"Text":"You have killed Vallon Zek.","Requirement":["MB"]},
    "SolRol Mini, Arlyxir":{"Text":"You have defeated Arlyxir within the Tower of Solusk Ro.","Requirement":["Tallon Zek", "Vallon Zek", "PostFlag Saryrn and KoS","Lord Mithaniel Marr"]},
    "SolRol Mini, Protector":{"Text":"You have defeated The Protector of Dresolik within the Tower of Solusk Ro.","Requirement":["Tallon Zek", "Vallon Zek", "PostFlag Saryrn and KoS","Lord Mithaniel Marr"]},
    "SolRol Mini, Jiva":{"Text":"You have defeated Jiva within the Tower of Solusk Ro.","Requirement":["Tallon Zek", "Vallon Zek", "PostFlag Saryrn and KoS","Lord Mithaniel Marr"]},
    "SolRol Mini, Rizlona":{"Text":"You have defeated Rizlona within the Tower of Solusk Ro.","Requirement":["Tallon Zek", "Vallon Zek", "PostFlag Saryrn and KoS","Lord Mithaniel Marr"]},
    "SolRol Mini, Xuzl":{"Text":"You have defeated Xuzl within the Tower of Solusk Ro.","Requirement":["Tallon Zek", "Vallon Zek", "PostFlag Saryrn and KoS","Lord Mithaniel Marr"]},
    "Solusek Ro":{"Text":"You have defeated Soluesk Ro within his own tower.","Requirement":["Ralloz Zek", "SolRol Mini, Arlyxir", "SolRol Mini, Protector", "SolRol Mini, Jiva", "SolRol Mini, Rizlona", "SolRol Mini, Xuzl"]},
    "ZoneInto PoNb":{"Text":"Zoned Into - Lair of Terris Thule (Plane of Nightmare B)","Requirement":["Hedge"]},
    "ZoneInto Tactics":{"Text":"Zoned Into - Drunder, Fortress of Zek (Plane of Tactics)","Requirement":["MB"]},
    "ZoneInto CoD":{"Text":"Zoned Into - Ruins of Lxanvom (Crypt of Decay)","Requirement":["PostFlag Grummus"]},
    "ZoneInto PoValor PoStorms":{"Text":"Zoned Into - Plane of Valor & Plane of Storms","Requirement":["PostFlag PoJ Trial 2"]},
    "ZoneInto HoHa":{"Text":"Zoned Into - Halls of Honor","Requirement":["AerinDar"]},
    "ZoneInto BoT":{"Text":"Zoned Into - Bastion of Thunder","Requirement":["BoT Flag"]},
    "ZoneInto HoHb":{"Text":"Zoned Into - Temple of Marr","Requirement":["HoH Trial, RD", "HoH Trial, Villagers", "HoH Trial, Maidens"]},
    "ZoneInto PoTorment":{"Text":"Zoned Into - Plane of Torment","Requirement":["PreFlag Keeper of Sorrows"]},
    "ZoneInto SolRoTower":{"Text":"Zoned Into - Tower of Solusek Ro","Requirement":["Tallon Zek", "Vallon Zek", "PostFlag Saryrn and KoS","Lord Mithaniel Marr"]},
    "ZoneInto PoFire":{"Text":"Zoned Into - Plane of Fire","Requirement":["Solusek Ro"]},
    "ZoneInto PoAirEarthWater":{"Text":"Zoned Into - Planes of Air, Earth and Water","Requirement":["PreFlag Elementals"]},
    "FenninRo":{"Text":"You have defeated Fennin Ro, the Tyrant of Fire.","Requirement":["Solusek Ro"]},
    "Xegony":{"Text":"You have defeated Xegony, the Queen of Air.","Requirement":["PreFlag Elementals"]},
    "Coirnav":{"Text":"You have defeated Coirnav, the Avatar of Water.","Requirement":["PreFlag Elementals"]},
    "Arbitor":{"Text":"You have defeated the arbitor within Plane of Earth A.","Requirement":["PreFlag Elementals"]},
    "Rathe Council":{"Text":"You have defeated the Rathe Council within Plane of Earth B","Requirement":["Arbitor"]},
    "ZoneInto PoTime":{"Text":"Zoned Into - Plane of Time","Requirement":["FenninRo", "Xegony", "Coirnav", "Rathe Council"]}}

  async def flaglist(self):
    myOutput = ""
    for aFlag in self.popFlag:
      myOutput += "{}: {}\r".format(aFlag, self.popFlag[aFlag]["Text"])
    return myOutput



  async def flagPoPFlag_PreReq(self, paramFlag):
    #Create output dictionary
    myOutput = ""

    #Loop through flags and see if flag exists, fixing case sensitivty
    inList = 0
    for aflag in self.popFlag:
      if aflag.lower() == paramFlag.lower():
        inList = 1
        baseFlagShort = aflag
        baseFlagLong = self.popFlag[aflag]["Text"]

    #Check to see if flag in list
    if inList == 1:
      #First call, print out header with short flag name
      myOutput = "Short Name: {}\rMagelo: {}\r\rPreRequirements:\r".format(baseFlagShort, baseFlagLong)


      #Flag in list, check to see if it has any requirements
      myReq = ""
      if len(self.popFlag[baseFlagShort]["Requirement"]) > 0:
        #Iterate through each flag and call this recursively
        for aPreReq in self.popFlag[baseFlagShort]["Requirement"]:
          myShort = aPreReq
          myLong = self.popFlag[aPreReq]["Text"]
          print("{}: {}".format(myShort, myLong))
          myReq += "{}: {}\r".format(myShort, myLong)
      else:
        #Flag doesn't exist, something wrong with my dictionary, debug it
        print("flagPoPFlag_Decode shouldn't happen {}".format(paramFlag))     
    else:
      #Flag not in list, return none
      myOutput = None
    
    if myOutput is None:
      myOutput = "No flags by that name, try using ?flag to get a short flag name"
    else:
      myOutput += myReq
    return myOutput

  async def getURL(self, paramPage, paramItem, forAPI):
    if paramPage == "guild":
      myItemType = "guild"
    else:
      myItemType = "char"
    
    if forAPI == 1:
      #https://magelo.wayfarershaven.com/index.php?api&page=guild
      myUrl = "{}?api&page={}&{}={}".format(self.baseUrl, paramPage, myItemType, paramItem)
    else:
      #https://magelo.wayfarershaven.com/index.php?page=flags&char=Uthok
      myUrl = "{}?page={}&{}={}".format(self.baseUrl, paramPage, myItemType, paramItem)

    return myUrl

  async def queryMagelo(self, myPage, myChar):
    #This function performs the actual http call    
    import aiohttp
    import json
    print("  Query Magelo {} for {}".format(myPage, myChar))
    myUrl = await self.getURL(myPage, myChar, 1)
    dicResponse = {}

    async with aiohttp.ClientSession() as session:
      async with session.get(myUrl) as r:        
        strText = await r.text()
        
        strText = strText.replace('[]', '')
        dicResponse = json.loads(strText)

        return dicResponse
      return {"Status": "failed session.get", "Response" : dicResponse}
    return {"Status": "failed aiohttp.ClientSession()", "Response" : dicResponse}

  async def getMageloData(self, myName, myAttr, myOutput):   
    #Check if myAttr already in myOutput
    if not myAttr in myOutput:
      #Create a getMageloData key with empty data
      myOutput[myAttr] = {}

    #Check if myName already in myAttr in myOutput
    if not myName in myOutput[myAttr]:
      #Create a getMageloData key with empty data
      myOutput[myAttr][myName] = {}

    #Check if this URL attribute is already defined
    if myAttr in self.pagecontent:
      #Query Magelo to new dictionary object myQuery
      myQuery = await self.queryMagelo(myAttr, myName)      

      #Check if default key exists for this page content
      if self.pagecontent[myAttr] in myQuery:
        #print("Success {} for {}".format(myAttr, myName))
        myOutput[myAttr][myName]["Status"] = "Success"
        myOutput[myAttr][myName]["Response"] = myQuery
      else:
        #print("Failed {} for {}".format(myAttr, myName))
        myOutput[myAttr][myName]["Status"] = "Failure"
        myOutput[myAttr][myName]["Response"] = myQuery        
    else:
      #Set the query response manually     
      #print("Didn't try {} for {}".format(myAttr, myName)) 
      myOutput[myAttr][myName]["Status"] = "Failed, invalid ULR attribute:  {}".format(myAttr)
      myOutput[myAttr][myName]["Response"] = {}
  
  async def getCharacterLevel(self, myName):
    #Create Output dictionary
    dicCharData = {}

    #Set URL attribute    
    myAttrib = 'character'
    
    #Query Magelo with data going to dicCharData by reference
    await self.getMageloData(myName, myAttrib, dicCharData)
    
    #Check if it was a success
    if dicCharData[myAttrib][myName]["Status"] == "Success":
      return int(dicCharData[myAttrib][myName]["Response"]["LEVEL"])
    else:
      #Likely anonymous or roleplaying, return -1
      return -1

  async def parseCharacterResponse(self, paramResponse, paramName, myOutputDict):
    print("  Parse response for {}".format(paramName))
    #Check if response was a success
    if paramResponse["character"][paramName]["Status"] == "Success":
      #Set charData dictionary to the character data in the response
      charData = paramResponse["character"][paramName]["Response"]

      #Update the myOutputDict dictionary with this character data
      myOutputDict["Name"] = charData["FIRST_NAME"]
      myOutputDict["Class"] = charData["CLASS"]
      myOutputDict["Level"] = int(charData["LEVEL"])
      myOutputDict["Race"] = charData["RACE"]
      myOutputDict["Guild"] = charData["GUILD_NAME"]
      if "item" in charData:
        myOutputDict["Items"] = charData["item"]
      else:
        myOutputDict["Items"] = {}
      #"Rank":guilddumpRank,
      #"LastLogin":guilddumpLastLogin,
      #"DaysSinceLastLogin":guilddumpDaysSinceLastLogin,
      #"PublicNote":guilddumpPublicNote,
      myOutputDict["ATK"] = int(str(charData["ATK"]).replace(",", ""))
      myOutputDict["Mana"] = int(str(charData["MANA"]).replace(",", ""))
      myOutputDict["HP"] = int(str(charData["HP"]).replace(",", ""))
      myOutputDict["AC"] = int(str(charData["AC"]).replace(",", ""))
      myOutputDict["Mit_AC"] = int(str(charData["MIT_AC"]).replace(",", ""))
      myOutputDict["PoisonRes"] = int(str(charData["POISON"]).replace(",", ""))
      myOutputDict["FireRes"] = int(str(charData["FIRE"]).replace(",", ""))
      myOutputDict["MagicRes"] = int(str(charData["MAGIC"]).replace(",", ""))
      myOutputDict["DiseaseRes"] = int(str(charData["DISEASE"]).replace(",", ""))
      myOutputDict["ColdRes"] = int(str(charData["COLD"]).replace(",", ""))

  async def parseFlagResponse_getRaw(self, paramResponse):
    #Create dictionary to store raw PoP data
    popRaw = {}

    #Loop through pop flags
    for ZoneFlags in paramResponse["head"]:
      #10 PoFire, 11 air/earth/water, 12 PoTime
      if ZoneFlags["ID"] >= 10 and ZoneFlags["ID"] <= 12:
        for aFlag in ZoneFlags["head.flags"]:
          #Get the raw text for a flag and the state (0/1) of that flag
          flagText = aFlag['TEXT']
          flagState = aFlag['FLAG']
          #Write raw PoP flag data to popRaw
          popRaw[flagText] = flagState

    #Loop through each expansion
    for myExpansion in paramResponse["mainhead"]:
      #Loop through each flagged zone
      for myZone in myExpansion["mainhead.main"]:
        #Extract data from myZone to local variables
        myZoneID = myZone["ID"]
        myZoneFlag = myZone["FLAG"]
        myZoneName = myZone["TEXT"]

        #restrict to PoP zones (IDs 1-12)
        if myZoneID <= 12:
            popRaw["Zoned Into - " + myZoneName] = myZoneFlag

    return popRaw

  async def parseFlagResponse_haveDone(self, paramPopRaw):
    #Create array for PoP steps the character has done
    haveDone = []

    #Iterate through popShort
    for aFlag in self.popFlag:
      #Get the raw name for this flag from self.popFlag
      myRawName = self.popFlag[aFlag]["Text"]

      #Get the status for this flag from popRaw
      flagStatus = paramPopRaw[myRawName]

      #Check to see if this character has that flag (flag==1)
      if flagStatus == 1:
        #Write the short name of this flag to the haveDone array
        haveDone.append(aFlag)
    return haveDone

  async def parseFlagResponse(self, paramResponse, paramName, paramLevel, myOutputDict):     
    #Check if response was a success
    if paramResponse["flags"][paramName]["Status"] == "Success":
      #Create a dictionary to hold the raw flag data for this character
      popRaw = await self.parseFlagResponse_getRaw(paramResponse["flags"][paramName]["Response"])
      
      #Create array for PoP steps the character has done
      haveDone = await self.parseFlagResponse_haveDone(popRaw)
      #print(haveDone)
      #Create dictionary for needed PoP steps the character can do 
      canDo = []

      #Iterate through each flag
      for aFlag in self.popFlag:
        #Check to see if it is done already
        if not aFlag in haveDone:
          #Iterate through requirments for this flag and trip notMet if any requirement not met
          notMet = 0
          for aReq in self.popFlag[aFlag]["Requirement"]:
            #Check if they are NOT in haveDone
            if not aReq in haveDone:
              #A requirement not met, set notMet to 0
              notMet = 1

          #check if all of the requirments were met (notmet = 0)
          if notMet == 0:
            #Add this flag to the canDo list
            canDo.append(aFlag)
          else:              
            #Check if there is an option to skip requirements by level        
            if "Level" in self.popFlag[aFlag]:
              #There is an option to bypass requirement by level
              #print("checking if can add to canDo list by level "+aFlag)
              #print(str(paramLevel) + " >= " + str(self.popFlag[aFlag]["Level"]))

              #Check to see if it is available by level 
              if int(paramLevel) >= self.popFlag[aFlag]["Level"]:                  
                #Add this flag to the canDo list
                canDo.append(aFlag)
                #print("Yes added, can skip to "+aFlag)
              else:
                #print("Nope not added, I cannot skip "+aFlag)
                pass

      myOutputDict["PoPFlagsCanDo"] = canDo

      #Set Progression status
      progressionStatus = "notset"
      if "ZoneInto PoTime" in haveDone:
          progressionStatus = "TimeFlagged"
      elif "ZoneInto PoFire" in haveDone and "ZoneInto PoAirEarthWater" in haveDone:
          progressionStatus = "Elemental, Full"
      elif "ZoneInto PoFire" in haveDone and "ZoneInto PoAirEarthWater"in haveDone:
          progressionStatus = "Elemental, FireOnly"
      elif "ZoneInto PoFire" in haveDone and "ZoneInto PoAirEarthWater" in haveDone:
          progressionStatus = "Elemental, NotFire"
      else:
          progressionStatus = "PreElemental"

      myOutputDict["ProgressionStatus"] = progressionStatus    


  async def getBasicData(self, pName):
    #Basic data means character and flag data, identify roleplaying, and anonymous

    #Dictionary to store data from query
    queryResponse = {}

    #Query Magelo for character data and flags data
    await self.getMageloData(pName, "character", queryResponse)
    await self.getMageloData(pName, "flags", queryResponse)

    #Dictionary to store specific character data
    dictChar = {}

    #Parse the raw character data with the processed data in dictChar
    await self.parseCharacterResponse(queryResponse, pName, dictChar)

    #Check to see if character was parsed
    if "Level" in dictChar:
      myLevel = dictChar["Level"]
    else:
      #Assume level 65 for any character that can't read character data
      myLevel =  65

    #Parse the raw flag data, function will add it to the data already in dictChar
    await self.parseFlagResponse(queryResponse, pName, myLevel, dictChar)

    #Set default value for custom field of MageloStatus
    dictChar["MageloStatus"] = "Error, this should be defined"
    
    #MageloStatus four values: Normal, Roleplaying, Anonymous, Doesn't Exist, , or Unknown
    #Check for Normal:  both success
    if queryResponse["flags"][pName]["Status"] == "Success" and queryResponse["character"][pName]["Status"] == "Success":
      dictChar["MageloStatus"] = "Normal" 
    #Check for Roleplaying:  works for flags, fails for character
    elif queryResponse["flags"][pName]["Status"] == "Success" and queryResponse["character"][pName]["Status"] == "Failure":
      dictChar["MageloStatus"] = "Roleplaying"
    #Anonymous for anonymous:  flags failed with response text of Server settings prevent you from viewing this item.
    elif queryResponse["flags"][pName]["Status"] == "Failure":
      if queryResponse["flags"][pName]["Response"]["TEXT"] == "Server settings prevent you from viewing this item.":
        dictChar["MageloStatus"] = "Anonymous"
      elif queryResponse["flags"][pName]["Response"]["TEXT"] == "Could not find that character.":
        dictChar["MageloStatus"] = "Doesn't Exist"
      else:
        dictChar["MageloStatus"] = "Unknown"
        print("MageloStatus Unknown:  " + queryResponse["flags"][pName]["Response"]["TEXT"])
    else:
      print(pName)
      print(queryResponse)
      dictChar["MageloStatus"] = "Unknown"
      print("MageloStatus Unknown:  " + queryResponse["flags"][pName]["Response"]["TEXT"])

    #Return the character data
    return dictChar




  async def getKeyData(self, pName, pDictChar):
    #Create blank arrays to store key data
    majorKeys = []
    allKeys = []

    #Check if MageloStatus in pDictChar
    if "MageloStatus" in pDictChar:
      #Get the current status
      myMageloStatus = pDictChar["MageloStatus"]
      #Check if the character is normal or roleplaying
      if myMageloStatus == "Normal" or myMageloStatus == "Roleplaying":
        #Create a blank dictionary to send as reference
        queryResponse = {}

        #Query Magelo for the keys data
        await self.getMageloData(pName, "keys", queryResponse)
        
        #Write status of the query to myStatus
        myResponseStatus = queryResponse["keys"][pName]["Status"]

        #Check if the status was a success
        if myResponseStatus == "Success":
          #Iterate through each key in the response
          for aKey in queryResponse["keys"][pName]["Response"]["keys"]:
            #Add key to allKeys array
            allKeys.append(aKey['KEY'])

            #Check if this key is in the list of major keys
            if aKey['KEY'] in self.majorKeys:
              #Add key to majorKeys array
              majorKeys.append(self.majorKeys[aKey['KEY']])
    
    #Update pDictChar with new values
    pDictChar["All Keys"] = allKeys
    pDictChar["Major Keys"] = majorKeys


  async def getAAData(self, pName, pDictChar):
    #Create blank arrays to store key data
    aaSpent = -1
    aaBanked = -1
    aaTotal = -1
    dictAA = []

    #Check if MageloStatus in pDictChar
    if "MageloStatus" in pDictChar:
      #Get the current status
      myMageloStatus = pDictChar["MageloStatus"]
      #Check if the character is normal
      if myMageloStatus == "Normal":
        #Create a blank dictionary to send as reference
        queryResponse = {}

        #Query Magelo for the AAs data
        await self.getMageloData(pName, "aas", queryResponse)
        
        #Write status of the query to myStatus
        myResponseStatus = queryResponse["aas"][pName]["Status"]

        #Check if the status was a success
        if myResponseStatus == "Success":
          #Get spent, banked, and calculate total AAs
          aaSpent = int(queryResponse["aas"][pName]["Response"]["AA_POINTS"])
          aaBanked = int(queryResponse["aas"][pName]["Response"]["POINTS_SPENT"])
          aaTotal = aaSpent + aaBanked
          
          #Loop through each AA tab          
          for aTab in queryResponse["aas"][pName]["Response"]["boxes"]:
            #Loop through each AA in this tab
            for anAA in aTab["boxes.aas"]:
              #Set the name with current and max rank values
              aaName = anAA["NAME"]
              aaRank = "{} of {}".format(anAA["CUR"], anAA["MAX"])
              
              #Check if current points in AA is 0
              if anAA["CUR"] == 0:
                aaStatus = "Not Started"
              
              #Check if current rank equals max ranks
              elif anAA["CUR"] == anAA["MAX"]:
                aaStatus = "Completed"
              
              #Anything that has at least one rank purchased, but not max ranks
              else:
                aaStatus = "InProgress"
              
              dictAA.append({"Name" : aaName, "Rank" : aaRank, "Status" : aaStatus})

    #Create blank arrays to store key data
    pDictChar["aaSpent"] = aaSpent
    pDictChar["aaBanked"] = aaBanked
    pDictChar["aaTotal"] = aaTotal
    pDictChar["AA"] = dictAA


  async def getSkillData(self, pName, pDictChar):    
    #Create blank arrays to store key data
    dictSkills = []

    #Check if MageloStatus in pDictChar
    if "MageloStatus" in pDictChar:
      #Get the current status
      myMageloStatus = pDictChar["MageloStatus"]
      #Check if the character is normal
      if myMageloStatus == "Normal":
        #Create a blank dictionary to send as reference
        queryResponse = {}

        #Query Magelo for the keys data
        await self.getMageloData(pName, "skills", queryResponse)
        
        #Write status of the query to myStatus
        myResponseStatus = queryResponse["skills"][pName]["Status"]

        #Check if the status was a success
        if myResponseStatus == "Success":
          
          for aSkill in queryResponse["skills"][pName]["Response"]["section"]:
            #print(queryResponse["skills"][pName]["Response"]["section"][aSkill]["section.skillrow"])
            skillName = queryResponse["skills"][pName]["Response"]["section"][aSkill]["section.skillrow"][0]['NAME']
            skillValue = int(queryResponse["skills"][pName]["Response"]["section"][aSkill]["section.skillrow"][0]['VALUE'])
            #print("{}: {}".format(skillName, skillValue))
            if skillValue > 0:
              dictSkills.append({"Name" : skillName, "Value" : skillValue})
    
    pDictChar["Skills"] = dictSkills
    

  async def getGuildList(self, myGuild):
    #Create Output dictionary
    queryResponse = {}

    #Convert underscores in guild name to %20    
    myGuild = myGuild.replace('_', '%20')
    
    #Query Magelo with data going to dicCharData by reference
    await self.getMageloData(myGuild, "guild", queryResponse)

    #Check if query was a success
    if queryResponse["guild"][myGuild]["Status"] == "Success":
      #Create dictionary to parsed data for guild list
      parsedGuildList = {}
      #Loop through ...
      for aChar in queryResponse["guild"][myGuild]["Response"]["guildmembers"]:
        #Create output dictionary
        dictChar = {}   
        #print(aChar['NAME'])
        #Check if anonymous
        if aChar['NAME'] == 'Anonymous':       
          #Anonymous character, set state as such
          dictChar['State'] = "Anonymous"
          dictChar['LEVEL'] = -1
        else:
          #Parse the 'Name' object to remove the extra HTML
          #   from:  <a href="index.php?page=character&char=Abbz">Abbz</a>
          #   to: Abbz
          arrLeftOfName = aChar['NAME'].split('>')
          arrRightOfName = arrLeftOfName[1].split('<')
          charName = arrRightOfName[0]
          
          print(charName)
          #Set level
          charLevel = aChar['LEVEL']

          #Add character information from Magelo for this character into dicData:
          print("  Query Magelo Character data")
          await self.getMageloData(charName, "character", queryResponse)
          await self.parseCharacterResponse(queryResponse, charName, dictChar)
          #print(dictChar)
          if int(charLevel) < 46:
            #Skip getting PoP flag data for characters under level 46
            dictChar['PoPFlagsCanDo'] = {}
            dictChar['ProgressionStatus'] ='PreElemental'
          else:
            print("  Query Magelo Flags data")
            await self.getMageloData(charName, "flags", queryResponse)
            await self.parseFlagResponse(queryResponse, charName, charLevel, dictChar)

          if "PreFlag Hedge" in dictChar['PoPFlagsCanDo']:
            #Purge all flagging data for any character that hasn't done hedge
            #Think level 55 cothbots
            #print("No hedge, clearing PoP CanDo")
            dictChar['PoPFlagsCanDo'] = {}
          
          charStatus = 0
          flagStatus = 0
          #Set State of Normal or Roleplaying
          if "character" in queryResponse:
            if charName in queryResponse["character"]:
              if queryResponse["character"][charName]["Status"] == "Success":
                charStatus = 1

          if "flags" in queryResponse:
            if charName in queryResponse["flags"]:
              if queryResponse["flags"][charName]["Status"] == "Success":
                flagStatus = 1          
          
          if charStatus and flagStatus:
            dictChar['State'] = "Normal"
          elif not charStatus and flagStatus:              
            dictChar['State'] = "Roleplaying"
          else:
            dictChar['State'] = "Anonymous"

          #Add character dictionary to parsedGuildList
          parsedGuildList[charName] = dictChar
          print("  Added: {} ({}) ({})".format(charName, str(charLevel), dictChar['State']))



        
      





  