import re
import asyncio

trigger = re.compile("^!send\s(?!.})(\w+\s+\w+ ?)$")
keywords = ["send"]

async def action(bot, msg):
    """**!send** _something_ to _location_
Send something to a location
`!send Neek Hell`"""
    #subjectlocation = trigger.sub("",msg.content)
    subject = msg.content.split()[1]
    location = msg.content.split()[2]
    

    await msg.channel.send("Sending "+subject+" to "+location+"...")
    #print(subject)
    #print(location)
    #await msg.channel.send(msg.content)
    


