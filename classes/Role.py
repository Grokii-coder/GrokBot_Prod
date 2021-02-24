class Role:
  def __init__(self):
    self.managed = {"Taters" : None
                , "TaterTots" : None
                , "Baked Potato" : None
                , "Lone Potato" : None
                , "Spud Buds" : None
                } 

  async def getCharactersMageloRoles(self, ctx, aChar):
    #Character name to publicNote from dump to discord member from link to discord member roles
    #Designed to check for leadership role for commands issued in-game
    myDump = await self.getGuildDump(ctx)
    links = await self.getLinkedPublicNotes(ctx)

    if aChar in myDump["Data"]:
      myPublicNote = myDump["Data"][aChar]["PublicNote"]

      if myPublicNote in links:
        print("Public note in links!")

        myMemberID = links[myPublicNote]
        myMember = await self.getMemberfromID(ctx, myMemberID)

        listRoles = await self.getRoleNamesForMember(myMember)
        print(listRoles)

        return listRoles
      else:
        myMsg = "Cannot find public note {} for character {} in links".format(myPublicNote, aChar)
    else:
      myMsg = "Cannot find {} in guild dump".format(aChar)
    
    print(myMsg)
    return None
    
    
  async def getMemberfromID(self, ctx, memberID):
    for aMember in ctx.guild.members:
      if aMember.id == memberID:
        return aMember
    return None

  async def getGuildDump(self, ctx):
    from classes.replitDB import replitDB
    repDB = replitDB()    
    newestDump = await repDB.getGuildProperty(ctx, "NewestGuildDump")

    return newestDump

  async def getGuildDumpData(self, ctx, pActiveDays):
    from classes.replitDB import replitDB
    repDB = replitDB()    
    newestDump = await repDB.getGuildProperty(ctx, "NewestGuildDump")

    #Create a dictionary to store the data
    myData = {}


    for aChar in newestDump["Data"]:      
      #Get public note
      myPublicNote = newestDump["Data"][aChar]["PublicNote"]

      #Check to see if this public note is NOT already in self.statDict
      if not myPublicNote in myData:
        #Add this public note
        myData[myPublicNote] = {"ActiveCount" : 0, "TimeCount" : 0}

      #Get days since last logon
      myDays = newestDump["Data"][aChar]["DaysSinceLastLogin"]

      #Check if active in the last 90 days
      if myDays <= pActiveDays:        
        #It is, Increment active count of characters for this public note
        myData[myPublicNote]["ActiveCount"] = 1 + myData[myPublicNote]["ActiveCount"]
      
      #Get Time Flag status from Progression Status, if it doesnt exist use ProgressionStatus
      if "ProgressionStatus" in newestDump["Data"][aChar]:
        myStatus = newestDump["Data"][aChar]["ProgressionStatus"]
      else:
        myStatus = newestDump["Data"][aChar]["MageloStatus"]

      #Check if time flagged
      if myStatus == 'TimeFlagged':
        #Character is Time flagged, Increment TimeCount        
        myData[myPublicNote]["TimeCount"] = 1 + myData[myPublicNote]["TimeCount"]
    
    return myData

  async def getPublicNoteOfRole(self, ctx, pRole):
    #Create output object
    listOutput = []

    #Get link of ID to publicNote
    myLinks = await self.getLinkedIds(ctx)
    
    #Check if the role in paramter matches a managed role
    if pRole in self.managed:
      #Loop through each member
      for aMember in ctx.guild.members:
        #Find the managed role for current member
        currentManagedRole = await self.getManagedRole(aMember)

        #Check if currentManagedRole is pRole
        if currentManagedRole == pRole:
          #Set the public note for this member
          myPublicNote = myLinks[aMember.id]

          #this PublicNote to listOutput
          listOutput.append(myPublicNote)
    else:
      print("getPublicNoteOfRole error, {} not in self.managed")
    
    return listOutput


  async def getLinkedIds(self, ctx):
    links = await self.getLinksFromDB(ctx)

    #Create a list with linked IDs
    linkID = {}
    for aLink in links:
      linkID[aLink['DiscordMemberID']] = aLink['PublicNote']
    
    return linkID

  async def getLinkedPublicNotes(self, ctx):
    links = await self.getLinksFromDB(ctx)

    #Create a list with linked IDs
    linkID = {}
    for aLink in links:
      linkID[aLink['PublicNote']] = aLink['DiscordMemberID']
    
    return linkID

  async def getLinksFromDB(self, ctx):
    #Get database object instanced
    from classes.replitDB import replitDB    
    repDB = replitDB()

    #Get linksfrom db
    links = await repDB.getGuildProperty(ctx, "Links")

    return links

  async def setManagedRoles(self, ctx):
    print("setLonePotato")

    links = await self.getLinksFromDB(ctx)

    #Create a list with linked IDs
    linkID = {}
    for aLink in links:
      linkID[aLink['DiscordMemberID']] = aLink['PublicNote']

    #Setup output variables
    msgNoManagedRole = ""
    msgLeadership = ""
    msgLonePotato = ""
    msgBakedPotato = ""
    msgTater = ""
    msgTaterTot = ""

    activeCount = 1
    timeCount = 1
    activeDays = 30

    #Get guild dump data with activity and time flagged calculated
    myDumpData = await self.getGuildDumpData(ctx, activeDays)

    #Loop through IDs of current guild members
    for aMember in ctx.guild.members:
      currentManagedRole = await self.getManagedRole(aMember)

      if aMember.bot:
        #Bot, do nothing
        #print("{}:  Bot, do nothing\r".format(aMember))
        pass
      elif currentManagedRole is None:
        #print("{}:  No managed role, skip\r".format(aMember))
        msgNoManagedRole += "{}:  No managed role, skip\r".format(aMember)
      elif "leadership" in await self.getRoleNamesForMember(aMember):
        #print("{}:  Leadership role, skip\r".format(aMember))
        msgLeadership += "{}:  Leadership role, skip\r".format(aMember)
      else:
        
        #Check to see if they have a link
        if aMember.id in linkID:
          #Member is linked!  Determine if Baked Potato, Tater Tot, or Tater
          
          #Set public note, active count, and time flagged character count
          myPublicNote = linkID[aMember.id]
          myActiveCount = myDumpData[myPublicNote]["ActiveCount"]
          myTimeCount = myDumpData[myPublicNote]["TimeCount"]
          
          #Check to see if they are inactive
          if myActiveCount < activeCount and not currentManagedRole == 'Baked Potato':
            await self.setManagedRole(ctx, aMember, "Baked Potato")
            msgBakedPotato += "{} ({}): Set from ({}) to (Baked Potato)\r".format(aMember, myPublicNote, currentManagedRole)
          elif myActiveCount < activeCount and currentManagedRole == 'Baked Potato':
            #Do nothing, proper role
            pass
          #Check to see if they have 3 toons time flagged
          elif myTimeCount >= timeCount and not currentManagedRole == 'Taters':
            await self.setManagedRole(ctx, aMember, "Taters")
            msgTater += "{} ({}): Set from ({}) to (Taters)\r".format(aMember, myPublicNote, currentManagedRole)
          elif myTimeCount >= timeCount and currentManagedRole == 'Taters':
            #Do nothing, proper role
            pass            
          #Check if they are active, but not 3 time flagged
          elif myActiveCount >= activeCount and myTimeCount < timeCount and not currentManagedRole == 'TaterTots':
            await self.setManagedRole(ctx, aMember, "TaterTots")
            msgTaterTot += "{} ({}): Set from ({}) to (TaterTots)\r".format(aMember, myPublicNote, currentManagedRole)
          elif myActiveCount >= activeCount and myTimeCount < timeCount and currentManagedRole == 'TaterTots':
            #Do nothing, proper role
            pass   
          else:
            #This shouldn't happen
            print("{}: Role Failure in, should not have happend".format(aMember))
        else:
          #No link, check if they are a spud bud
          if currentManagedRole == "Spud Buds":
            pass
          elif not currentManagedRole == "Lone Potato":
            await self.setManagedRole(ctx, aMember, "Lone Potato")
            msgLonePotato += "{} : Set from ({}) to (Lone Potato)\r".format(aMember, currentManagedRole)
            #print(msgLonePotato)
          elif currentManagedRole == "Lone Potato":
            pass
          else:
            #This shouldn't happen
            print("{}: Role Failure in, should not have happend".format(aMember))            

      
    myMsg = ""
    if len(msgNoManagedRole) > 0:
      myMsg += "**No Managed Role:**\r{}\r".format(msgNoManagedRole)
    if len(msgLeadership) > 0:
      myMsg += "**Leadership Role, do nothing:**\r{}\r".format(msgLeadership)
    if len(msgLonePotato) > 0:
      myMsg += "**No Link, set to Lone Potato:**\r{}\r".format(msgLonePotato)
    if len(msgBakedPotato) > 0:
      myMsg += "**Inactive (not {} char last {} days) set to Baked Potato:**\r{}\r".format(activeCount, activeDays, msgBakedPotato)
    if len(msgTater) > 0:
      myMsg += "**Active and at least {} Time Flagged, set to Tater**\r{}\r".format(timeCount, msgTater)
    if len(msgTaterTot) > 0:
      myMsg += "**Active, but no Time flagged, set to Tater Tots:**\r{}\r".format(msgTaterTot)    
    return myMsg

  async def setManagedRole(self, ctx, pMember, pRoleName):

    #Get current managed role
    currentManagedRole = await self.getManagedRole(pMember)

    #Check if current role equal to requested role
    if currentManagedRole == pRoleName:
      pass
    else:
      #Get new role object
      myNewRole = None
      for aRole in ctx.guild.roles:
        if aRole.name == pRoleName:
          myNewRole = aRole
      
      if myNewRole is None:
        myMsg = "Error, couldn't find ({}) in guild, cant add ({}) to it.".format(pRoleName, pMember)
        print(myMsg)
      else:
        #Remove from old role
        msgAudit = "Changing managed role from {} to {}".format(currentManagedRole, pRoleName)
        await self.removeRole(pMember, currentManagedRole, msgAudit)

        #Add to new role
        await pMember.add_roles(myNewRole, reason=msgAudit, atomic=True)
    


  async def ManagedRoleCount(self, pMember):
    roleCount = 0
    myRoles = []
    for aRole in pMember.roles:
      if aRole.name in self.managed:
        roleCount += 1
        myRoles.append(aRole.name)
    return {"count" : roleCount, "roles" : ', '.join(myRoles)}

  async def multiMutuallyExclusive(self, ctx):
    print("multiMutuallyExclusive")    

    #msgMultiManaged = "Multi managed roles\r"
    msgNoManaged = "No managed roles\r"

    #Loop through IDs of current guild members
    for aMember in ctx.guild.members:
      #Check if this member is a bot
      if aMember.bot:
        #Bot, do nothing
        pass
      else:

        managedRole = await self.ManagedRoleCount(aMember)
        
        if managedRole["count"] > 1:
          #msgMultiManaged += "  {} ({})\r".format(aMember, managedRole["roles"])
          print(managedRole["roles"])
          await self.fixMulti(aMember)

        elif managedRole["count"] == 0:
          msgNoManaged += "  {}\r".format(aMember)

    
    myMsg = msgNoManaged

    return myMsg

  async def removeRole(self, pMember, pRoleName, pReason):
    print("removeROle called for {} to remove {}".format(pMember, pRoleName))
    #Iterate through roles
    for aRole in pMember.roles:
      #Check if this is the role to remove
      if aRole.name == pRoleName:
        #Attempt to remove the role
        await pMember.remove_roles(aRole, reason=pReason, atomic=True)

  async def getRoleNamesForMember(self, pMember):
    #Get all current roles
    myRoles = []
    for aRole in pMember.roles:
      myRoles.append(aRole.name)
    return myRoles 

  async def getManagedRole(self, pMember):
    #print("getManagedRole called for {}".format(pMember))
    #print(pMember.roles)

    #Count how many  managed roles this member has
    managedRole = await self.ManagedRoleCount(pMember)
    
    #Loop as long as they are a member of more than one role
    while managedRole["count"] > 1:
      #Get all current roles
      myRoles = await self.getRoleNamesForMember(pMember)

      #Check for each managed role and remove access from least to most permissive
      if "Spud Buds" in myRoles:
        print("Try to remove Spud Buds")
        await self.removeRole(pMember, "Spud Buds", "Multi-Managed Roles:  {}".format(managedRole["roles"]))
      elif "Lone Potato" in myRoles:
        print("Try to remove Lone Potato")
        await self.removeRole(pMember, "Lone Potato", "Multi-Managed Roles:  {}".format(managedRole["roles"]))
      elif "Baked Potato" in myRoles:
        print("Try to remove Baked Potato")
        await self.removeRole(pMember, "Baked Potato", "Multi-Managed Roles:  {}".format(managedRole["roles"]))
      elif "TaterTots" in myRoles:
        print("Try to remove TaterTots")
        await self.removeRole(pMember, "TaterTots", "Multi-Managed Roles:  {}".format(managedRole["roles"]))
      elif "Taters" in myRoles:
        print("Try to remove Taters")
        await self.removeRole(pMember, "Taters", "Multi-Managed Roles:  {}".format(managedRole["roles"]))
      
      #Set new managedRole count
      managedRole = await self.ManagedRoleCount(pMember)
    
    #Member is only a member of one manged role, find it and return it
    myRoles = await self.getRoleNamesForMember(pMember)    
    for aRole in self.managed:
      if aRole in myRoles:
        return aRole
    
    return None