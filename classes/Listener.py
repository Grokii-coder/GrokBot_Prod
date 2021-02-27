class Listener:
  def __init__(self):
    self.tranServerToGuild = {
      "GrokBot Dev" : "Spirit of Potato",
      "Potatoville" : "Spirit of Potato"
      }
  
  async def parseMessage(self, message):
    import re
    #Parse the name of the person saying the message
    pattern = "\*\*(.*) guild:\*\* (.*)"
    result = re.search(pattern, message.content)

    if result == None:
      myGuildMate = "Unknown"
      myMessage = "Blank Message"
    else:
      myGuildMate = result.group(1)
      myMessage = result.group(2)
    
    #myReturn = {"GuildMate" : myGuildMate, "Message" : myMessage}
    
    return {"GuildMate" : myGuildMate, "Message" : myMessage}