import re
import random
import sys

trigger = re.compile("^!dice")
keywords = ["dice", "golf"]

match_pattern = re.compile(r"^!dice\s+(\d+)d(\d+)(?:([+-])(\d+))?")

async def action(bot, msg):
    """**!dice** _dice_**d**_sides_[+|-_modifier_]
Simulate a dice roll. _Dice_ is the number of dice to roll and _sides_ is the number of sides each die has. Optionally you can specify _modifier_, prefixed with + or -.
`!dice 1d20+3`
    """
    match = match_pattern.match(msg.clean_content)

    if match:
        match_grps = match.groups()
        dice_count = int(match_grps[0])
        dice_sides = int(match_grps[1])

        if match_grps[2] and match_grps[3]:
            modifier_sign = match_grps[2]
            modifier = int(match_grps[3])
            if modifier_sign == "-":
                modifier = -modifier
        else:
            modifier = 0

        if dice_count < sys.maxsize and dice_sides < sys.maxsize and modifier < sys.maxsize:
            result = random.randint(dice_count, dice_count * dice_sides) + modifier
            await bot.send_message(msg.channel, str(result))
