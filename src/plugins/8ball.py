import re
import random

trigger = re.compile("^!8ball")
keywords = ["8ball", "8-ball"]

answers = [
    "It is certain",
    "It is decidedly so",
    "Without a doubt",
    "Yes, definitely",
    "You may rely on it",
    "As I see it, yes",
    "Most likely",
    "Outlook good",
    "Yes",
    "Signs point to yes",
    "Reply hazy try again",
    "Ask again later",
    "Better not tell you now",
    "Cannot predict now",
    "Concentrate and ask again",
    "Don't count on it",
    "My reply is no",
    "My sources say no",
    "Outlook not so good",
    "Very doubtful"
]

async def action(bot, msg):
    """**!8ball**
Responds to a yes-no question."""
    answer = random.choice(answers)
    await bot.send_message(msg.channel, answer)
