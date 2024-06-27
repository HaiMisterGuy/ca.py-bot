import re
import random

trigger = re.compile("^!decide")
keywords = ["decide"]

async def action(bot, msg):
    """**!decide** _a_ **or** _b_ [**or** _c_] ...
Helps you with decisions.
`!decide to be or not to be`"""
    cmd_args = [arg.strip() for arg in trigger.sub("", msg.clean_content).split(" or ")]
    if len(cmd_args) > 1:
        choice = random.choice(cmd_args)
        await bot.send_message(msg.channel, choice)
