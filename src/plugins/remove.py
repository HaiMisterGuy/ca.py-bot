import re
import asyncio

trigger = re.compile("^!remove")
keywords = ["remove"]

async def action(bot, msg):
    """**!remove** _thing_
Removes something, not everything in life is necessary.
`!remove EDF`"""
    thing = trigger.sub("",msg.content).strip()
    
    if thing != "":
        await msg.channel.send("Removing "+thing)
        await asyncio.sleep(2)
        await msg.channel.send("██]]]]]]]] 25% complete...")
        await asyncio.sleep(2)
        await msg.channel.send("█████]]]]] 50% complete...")
        await asyncio.sleep(2)
        await msg.channel.send("█████████] 99% complete...")
        await asyncio.sleep(2)
        await msg.channel.send(thing+" removed!")
        await asyncio.sleep(2)

