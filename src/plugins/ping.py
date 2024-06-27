import re

trigger = re.compile("^!ping")
keywords = ["ping"]

async def action(bot, msg):
    """**!ping**
Responds with 'pong'."""
    await bot.send_message(msg.channel, "pong")
