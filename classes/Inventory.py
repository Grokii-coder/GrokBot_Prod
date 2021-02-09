class Inventory:
  def __init__(self):
    self.mySlot = {
      #Todo:  Worn Slots
      #Bank Slots
      #Shared Bank Slots

      #Inventory Slots
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
      }

  async def getSlotName(self, pSlot):
    if pSlot in self.mySlot:
      return self.mySlot[pSlot]
    else:
      return "Undefined"
