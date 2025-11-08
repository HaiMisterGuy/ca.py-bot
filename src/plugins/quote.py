import re
from ..utils import discord_snowflake_to_datetime, random_date_between
from datetime import datetime, timedelta
from random import randint

trigger = re.compile("^!quote")
keywords = ["quote"]

def format_quote(msg):
    return str(msg.author.name) + ": " + str(msg.clean_content)

max_log_length = 100

async def action(bot, msg):
    """**!quote**
Prints a random message from the channel."""
    now = datetime.utcnow()
    channelBeg = msg.channel.created_at.replace(tzinfo=None)
    query_date = random_date_between(channelBeg, now)
    log_limit = randint(1, max_log_length)

    # for some reason the discord api returns the messages in reverse chronological order
    logs = msg.channel.history(after=query_date, limit=log_limit)

    async for log_msg in logs:
        if log_msg.author != bot.user and not bot.is_message_triggering(log_msg):
            break

    await bot.send_message(msg.channel, format_quote(log_msg))
