class Inventory:
  async def getSlotName(self, pSlot):
    for aType in self.ItemSlots:
      if pSlot in self.ItemSlots[aType]:
        return self.ItemSlots[aType][pSlot]
    
    return "Undefined"



  async def VexThalStatus(self, pChar):
    #Setup WFH Magelo object
    from classes.WFH_Magelo import WFH_Magelo
    from classes.Everquest import Everquest
    WFH = WFH_Magelo()
    EQ = Everquest()

    #Get basic data for this character:
    dictChar = await WFH.getBasicData(pChar)

    #Check if status wasn't normal
    if not dictChar["MageloStatus"] == "Normal":
      return "Invalid MageloStatus: {}".format(dictChar["MageloStatus"])

    #Get key data and add it to dictChar
    await WFH.getKeyData(pChar, dictChar)

    #Check if VT Key already on key ring
    if "Vex Thal" in dictChar["Major Keys"]:
      return "{} is already keyed for Vex Thal".format(pChar)
    else:
      myHas = ""
      myNeeds = ""
      #Iterate through each item on the character
      for aItem in dictChar["Items"]:
        #mySlot = int(aItem["SLOT"])
        #myIcon = aItem["ICON"]
        myName = aItem["NAME"]
        #myStack = aItem["STACK"]
        myID = int(aItem["ID"])
        #myLink = aItem["LINK"]
        #myHTML = aItem["HTML"]

        print("{}: {}".format(myID, myName))

        #Check to see if Ring of the Shissar on keyring
        if not "Ssraeshza Emperor's Chamber" in dictChar["Major Keys"]: 
          #Check if this item is in EQ.empKey
          if myID in EQ.empKey:
            #Add to myHas
            myHas += "  {}\r".format(EQ.empKey[myID])
            #Remove this item from EQ.empKey
            EQ.empKey.pop(myID)

        #Check if this item is in EQ.VTKey
        if myID in EQ.VTKey:
          #Add to myHas
          myHas += "  {}\r".format(EQ.VTKey[myID])
          #Remove this item from EQ.empKey
          EQ.VTKey.pop(myID)

      #Check to see if Ring of the Shissar on keyring
      if not "Ssraeshza Emperor's Chamber" in dictChar["Major Keys"]: 
        for aItem in EQ.empKey:
          #Add to myNeeds
          myNeeds += "  {}\r".format(EQ.empKey[aItem])

      for aItem in EQ.VTKey:
        #Add to myNeeds
        myNeeds += "  {}\r".format(EQ.VTKey[aItem])
      
      myMsg = "VT key for {}:\r\rHave\r{}\rNeed\r{}".format(pChar, myHas, myNeeds)


    return myMsg


  async def findItemByName(self, pChar, pItem):
    #Setup WFH Magelo object
    from classes.WFH_Magelo import WFH_Magelo
    WFH = WFH_Magelo()
    
    #Get basic data for this character:
    dictChar = await WFH.getBasicData(pChar)

    #Check to see if doesn't exist or anon, etc
    if not dictChar["MageloStatus"] == "Normal":
      return "Invalid MageloStatus: {}".format(dictChar["MageloStatus"])
    elif not "Items" in dictChar:
      return "No Items"
    else:
      myMsg = ""
      #Iterate through each item
      for aItem in dictChar["Items"]:
        mySlot = int(aItem["SLOT"])
        #myIcon = aItem["ICON"]
        myName = aItem["NAME"]
        myStack = aItem["STACK"]
        #myID = aItem["ID"]
        #myLink = aItem["LINK"]
        #myHTML = aItem["HTML"]

        if myStack is None or not myStack.isnumeric():
          myStack = 1

        mySlotName = await self.getSlotName(mySlot)
        if mySlotName == "Undefined":
          mySlotName = "Slot {} Undefined".format(mySlot)

        if pItem.lower() in myName.lower():
          thisItem = "{} {}: {} x{}\r".format(pChar, mySlotName, myName, myStack)
          myMsg += thisItem
      return myMsg


  def __init__(self):
    self.ItemSlots = {
    "Worn" : {
      0 : "Charm"
      ,1 : "Left Ear"
      ,2 : "Head"
      ,3 : "Face"
      ,4 : "Right Ear"
      ,5 : "Neck"
      ,6 : "Shoulder"
      ,7 : "Arms"
      ,8 : "Back"
      ,9 : "Left Wrist"
      ,10 : "Right Wrist"
      ,11 : "Range"
      ,12 : "Hands"
      ,13 : "Primary"
      ,14 : "Secondary"
      ,15 : "Left Finger"
      ,16 : "Right Finger"
      ,17 : "Chest"
      ,18 : "Legs"
      ,19 : "Feet"
      ,20 : "Waist"
      ,21 : "Power Source"
      ,22 : "Ammo"
    }, "Inventory" : {
      23 : "Inv1"
      ,24 : "Inv3"
      ,25 : "Inv5"
      ,26 : "Inv7"
      ,27 : "Inv2"
      ,28 : "Inv4"
      ,29 : "Inv8"
      ,30 : "Inv8"

      #Bag in Inventory 1 (slot 23)
      ,251 : "Inv1|Bag1"
      ,252 : "Inv1|Bag2"
      ,253 : "Inv1|Bag3"
      ,254 : "Inv1|Bag4"
      ,255 : "Inv1|Bag5"
      ,256 : "Inv1|Bag6"
      ,257 : "Inv1|Bag7"
      ,258 : "Inv1|Bag8"
      ,259 : "Inv1|Bag9"
      ,260 : "Inv1|Bag10"

      #Bag in Inventory 2 (slot 27)
      ,291 : "Inv2|Bag1"
      ,292 : "Inv2|Bag2"
      ,293 : "Inv2|Bag3"
      ,294 : "Inv2|Bag4"
      ,295 : "Inv2|Bag5"
      ,296 : "Inv2|Bag6"
      ,297 : "Inv2|Bag7"
      ,298 : "Inv2|Bag8"
      ,299 : "Inv2|Bag9"
      ,300 : "Inv2|Bag10"

      #Bag in Inventory 3 (slot 24)
      ,261 : "Inv3|Bag1"
      ,262 : "Inv3|Bag2"
      ,263 : "Inv3|Bag3"
      ,264 : "Inv3|Bag4"
      ,265 : "Inv3|Bag5"
      ,266 : "Inv3|Bag6"
      ,267 : "Inv3|Bag7"
      ,268 : "Inv3|Bag8"
      ,269 : "Inv3|Bag9"
      ,270 : "Inv3|Bag10"

      #Bag in Inventory 4 (slot 28)
      ,301 : "Inv4|Bag1"
      ,302 : "Inv4|Bag2"
      ,303 : "Inv4|Bag3"
      ,304 : "Inv4|Bag4"
      ,305 : "Inv4|Bag5"
      ,306 : "Inv4|Bag6"
      ,307 : "Inv4|Bag7"
      ,308 : "Inv4|Bag8"
      ,309 : "Inv4|Bag9"
      ,310 : "Inv4|Bag10"

      #Bag in Inventory 5 (slot 25)
      ,271 : "Inv5|Bag1"
      ,272 : "Inv5|Bag2"
      ,273 : "Inv5|Bag3"
      ,274 : "Inv5|Bag4"
      ,275 : "Inv5|Bag5"
      ,276 : "Inv5|Bag6"
      ,277 : "Inv5|Bag7"
      ,278 : "Inv5|Bag8"
      ,279 : "Inv5|Bag9"
      ,280 : "Inv5|Bag10"

      #Bag in Inventory 6 (slot 29)
      ,311 : "Inv6|Bag1"
      ,312 : "Inv6|Bag2"
      ,313 : "Inv6|Bag3"
      ,314 : "Inv6|Bag4"
      ,315 : "Inv6|Bag5"
      ,316 : "Inv6|Bag6"
      ,317 : "Inv6|Bag7"
      ,318 : "Inv6|Bag8"
      ,319 : "Inv6|Bag9"
      ,320 : "Inv6|Bag10"

      #Bag in Inventory 7 (slot 26)
      ,281 : "Inv7|Bag1"
      ,282 : "Inv7|Bag2"
      ,283 : "Inv7|Bag3"
      ,284 : "Inv7|Bag4"
      ,285 : "Inv7|Bag5"
      ,286 : "Inv7|Bag6"
      ,287 : "Inv7|Bag7"
      ,288 : "Inv7|Bag8"
      ,289 : "Inv7|Bag9"
      ,290 : "Inv7|Bag10"

      #Bag in Inventory 8 (slot 30)
      ,321 : "Inv8|Bag1"
      ,322 : "Inv8|Bag2"
      ,323 : "Inv8|Bag3"
      ,324 : "Inv8|Bag4"
      ,325 : "Inv8|Bag5"
      ,326 : "Inv8|Bag6"
      ,327 : "Inv8|Bag7"
      ,328 : "Inv8|Bag8"
      ,329 : "Inv8|Bag9"
      ,330 : "Inv8|Bag10"
    }, "Bank" : {
      2000 : "Bank"
      ,2004 : "Bank"
      ,2001 : "Bank"
      ,2005 : "Bank"
      ,2002 : "Bank"
      ,2006 : "Bank"
      ,2003 : "Bank"
      ,2007 : "Bank"
      ,2008 : "Bank"
      ,2012 : "Bank"
      ,2009 : "Bank"
      ,2013 : "Bank"
      ,2010 : "Bank"
      ,2014 : "Bank"
      ,2011 : "Bank"
      ,2015 : "Bank"

      ,2031 : "Bank1|Bag1"
      ,2032 : "Bank1|Bag2"
      ,2033 : "Bank1|Bag3"
      ,2034 : "Bank1|Bag4"
      ,2035 : "Bank1|Bag5"
      ,2036 : "Bank1|Bag6"
      ,2037 : "Bank1|Bag7"
      ,2038 : "Bank1|Bag8"
      ,2039 : "Bank1|Bag9"
      ,2040 : "Bank1|Bag10"
      ,2041 : "Bank3|Bag1"
      ,2042 : "Bank3|Bag2"
      ,2043 : "Bank3|Bag3"
      ,2044 : "Bank3|Bag4"
      ,2045 : "Bank3|Bag5"
      ,2046 : "Bank3|Bag6"
      ,2047 : "Bank3|Bag7"
      ,2048 : "Bank3|Bag8"
      ,2049 : "Bank3|Bag9"
      ,2050 : "Bank3|Bag10"
      ,2051 : "Bank5|Bag1"
      ,2052 : "Bank5|Bag2"
      ,2053 : "Bank5|Bag3"
      ,2054 : "Bank5|Bag4"
      ,2055 : "Bank5|Bag5"
      ,2056 : "Bank5|Bag6"
      ,2057 : "Bank5|Bag7"
      ,2058 : "Bank5|Bag8"
      ,2059 : "Bank5|Bag9"
      ,2060 : "Bank5|Bag10"
      ,2061 : "Bank7|Bag1"
      ,2062 : "Bank7|Bag2"
      ,2063 : "Bank7|Bag3"
      ,2064 : "Bank7|Bag4"
      ,2065 : "Bank7|Bag5"
      ,2066 : "Bank7|Bag6"
      ,2067 : "Bank7|Bag7"
      ,2068 : "Bank7|Bag8"
      ,2069 : "Bank7|Bag9"
      ,2070 : "Bank7|Bag10"
      ,2071 : "Bank2|Bag1"
      ,2072 : "Bank2|Bag2"
      ,2073 : "Bank2|Bag3"
      ,2074 : "Bank2|Bag4"
      ,2075 : "Bank2|Bag5"
      ,2076 : "Bank2|Bag6"
      ,2077 : "Bank2|Bag7"
      ,2078 : "Bank2|Bag8"
      ,2079 : "Bank2|Bag9"
      ,2080 : "Bank2|Bag10"
      ,2081 : "Bank4|Bag1"
      ,2082 : "Bank4|Bag2"
      ,2083 : "Bank4|Bag3"
      ,2084 : "Bank4|Bag4"
      ,2085 : "Bank4|Bag5"
      ,2086 : "Bank4|Bag6"
      ,2087 : "Bank4|Bag7"
      ,2088 : "Bank4|Bag8"
      ,2089 : "Bank4|Bag9"
      ,2090 : "Bank4|Bag10"
      ,2091 : "Bank6|Bag1"
      ,2092 : "Bank6|Bag2"
      ,2093 : "Bank6|Bag3"
      ,2094 : "Bank6|Bag4"
      ,2095 : "Bank6|Bag5"
      ,2096 : "Bank6|Bag6"
      ,2097 : "Bank6|Bag7"
      ,2098 : "Bank6|Bag8"
      ,2099 : "Bank6|Bag9"
      ,2100 : "Bank6|Bag10"
      ,2101 : "Bank8|Bag1"
      ,2102 : "Bank8|Bag2"
      ,2103 : "Bank8|Bag3"
      ,2104 : "Bank8|Bag4"
      ,2105 : "Bank8|Bag5"
      ,2106 : "Bank8|Bag6"
      ,2107 : "Bank8|Bag7"
      ,2108 : "Bank8|Bag8"
      ,2109 : "Bank8|Bag9"
      ,2110 : "Bank8|Bag10"
      ,2111 : "Bank9|Bag1"
      ,2112 : "Bank9|Bag2"
      ,2113 : "Bank9|Bag3"
      ,2114 : "Bank9|Bag4"
      ,2115 : "Bank9|Bag5"
      ,2116 : "Bank9|Bag6"
      ,2117 : "Bank9|Bag7"
      ,2118 : "Bank9|Bag8"
      ,2119 : "Bank9|Bag9"
      ,2120 : "Bank9|Bag10"
      ,2121 : "Bank11|Bag1"
      ,2122 : "Bank11|Bag2"
      ,2123 : "Bank11|Bag3"
      ,2124 : "Bank11|Bag4"
      ,2125 : "Bank11|Bag5"
      ,2126 : "Bank11|Bag6"
      ,2127 : "Bank11|Bag7"
      ,2128 : "Bank11|Bag8"
      ,2129 : "Bank11|Bag9"
      ,2130 : "Bank11|Bag10"
      ,2131 : "Bank13|Bag1"
      ,2132 : "Bank13|Bag2"
      ,2133 : "Bank13|Bag3"
      ,2134 : "Bank13|Bag4"
      ,2135 : "Bank13|Bag5"
      ,2136 : "Bank13|Bag6"
      ,2137 : "Bank13|Bag7"
      ,2138 : "Bank13|Bag8"
      ,2139 : "Bank13|Bag9"
      ,2140 : "Bank13|Bag10"
      ,2141 : "Bank15|Bag1"
      ,2142 : "Bank15|Bag2"
      ,2143 : "Bank15|Bag3"
      ,2144 : "Bank15|Bag4"
      ,2145 : "Bank15|Bag5"
      ,2146 : "Bank15|Bag6"
      ,2147 : "Bank15|Bag7"
      ,2148 : "Bank15|Bag8"
      ,2149 : "Bank15|Bag9"
      ,2150 : "Bank15|Bag10"
      ,2151 : "Bank10|Bag1"
      ,2152 : "Bank10|Bag2"
      ,2153 : "Bank10|Bag3"
      ,2154 : "Bank10|Bag4"
      ,2155 : "Bank10|Bag5"
      ,2156 : "Bank10|Bag6"
      ,2157 : "Bank10|Bag7"
      ,2158 : "Bank10|Bag8"
      ,2159 : "Bank10|Bag9"
      ,2160 : "Bank10|Bag10"
      ,2161 : "Bank12|Bag1"
      ,2162 : "Bank12|Bag2"
      ,2163 : "Bank12|Bag3"
      ,2164 : "Bank12|Bag4"
      ,2165 : "Bank12|Bag5"
      ,2166 : "Bank12|Bag6"
      ,2167 : "Bank12|Bag7"
      ,2168 : "Bank12|Bag8"
      ,2169 : "Bank12|Bag9"
      ,2170 : "Bank12|Bag10"
      ,2171 : "Bank14|Bag1"
      ,2172 : "Bank14|Bag2"
      ,2173 : "Bank14|Bag3"
      ,2174 : "Bank14|Bag4"
      ,2175 : "Bank14|Bag5"
      ,2176 : "Bank14|Bag6"
      ,2177 : "Bank14|Bag7"
      ,2178 : "Bank14|Bag8"
      ,2179 : "Bank14|Bag9"
      ,2180 : "Bank14|Bag10"
      ,2181 : "Bank16|Bag1"
      ,2182 : "Bank16|Bag2"
      ,2183 : "Bank16|Bag3"
      ,2184 : "Bank16|Bag4"
      ,2185 : "Bank16|Bag5"
      ,2186 : "Bank16|Bag6"
      ,2187 : "Bank16|Bag7"
      ,2188 : "Bank16|Bag8"
      ,2189 : "Bank16|Bag9"
      ,2190 : "Bank16|Bag10"
    }, "Shared" : {
      2500 : "Shared1|Bag"
      ,2501 : "Shared2|Bag"
      ,2531 : "Shared1|Bag1"
      ,2532 : "Shared1|Bag2"
      ,2533 : "Shared1|Bag3"
      ,2534 : "Shared1|Bag4"
      ,2535 : "Shared1|Bag5"
      ,2536 : "Shared1|Bag6"
      ,2537 : "Shared1|Bag7"
      ,2538 : "Shared1|Bag8"
      ,2539 : "Shared1|Bag9"
      ,2540 : "Shared1|Bag10"
      ,2541 : "Shared2|Bag1"
      ,2542 : "Shared2|Bag2"
      ,2543 : "Shared2|Bag3"
      ,2544 : "Shared2|Bag4"
      ,2545 : "Shared2|Bag5"
      ,2546 : "Shared2|Bag6"
      ,2547 : "Shared2|Bag7"
      ,2548 : "Shared2|Bag8"
      ,2549 : "Shared2|Bag9"
      ,2550 : "Shared2|Bag10"
    }}
