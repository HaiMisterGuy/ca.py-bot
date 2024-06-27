import re
import urllib.request
from urllib.request import HTTPError, URLError
import discord
from PIL import Image
import io
import emoji as allmyniggashateemoji

trigger = re.compile("^!picmerge")
keywords = ["picmerge", "picture", "merge", "image"]
'<:stare:451126180750557196>'
custom_emoji_pattern = re.compile("<:(?P<name>.+):(?P<id>.+)>")
max_img_size = 20000000 # 20mb
allowed_img_types = ["image/png", "image/jpeg", "image/gif"]
twemoji_url_template = "https://twitter.github.io/twemoji/v/latest/72x72/{}.png"
zerow_joiner = "\u200d"
variant_selector = '\ufe0f'

def parse_int(str):
    try:
        return int(str)
    except (ValueError, TypeError):
        return None

def parse_custom_emoji(bot, text):
    emoji_match = custom_emoji_pattern.match(text)
    if emoji_match:
        emoji_id = parse_int(emoji_match.group("id"))
        if emoji_id:
            return bot.get_emoji(emoji_id)

# Based on https://github.com/twitter/twemoji/blob/42f8843cb3aa1f9403d5479d7e3f7e01176ad08e/scripts/build.js#L571
def get_twemoji_url(emoji):
    if zerow_joiner not in emoji:
        emoji = re.sub(variant_selector, "", emoji)
    if allmyniggashateemoji.emoji_count(emoji) > 0:
        surrogates = list(emoji)
        r = []
        c = 0
        p = 0
        i = 0
        while i < len(surrogates):
            c = ord(surrogates[i])
            i += 1
            if p:
                r.append(hex(0x10000 + ((p - 0xd800) << 10) + (c - 0xdc00))[2:])
                p = 0
            elif 0xd800 <= c and c <= 0xdbff:
                p = c
            else:
                r.append(hex(c)[2:])
        return twemoji_url_template.format("-".join(r))
    else:
        return None

def get_image(bot, arg):
    url = arg
    emoji = parse_custom_emoji(bot, arg)
    if emoji:
        url = emoji.url
    else:
        twemoji = get_twemoji_url(arg)
        if twemoji:
            url = twemoji
    try:
        req = urllib.request.Request(url, method = "HEAD", headers = {"User-Agent": "capy"})
    except (HTTPError, URLError, ValueError) as e:
        print(e)
        return None

    res = urllib.request.urlopen(req)
    length = parse_int(res.getheader("Content-Length"))

    if not length or length > max_img_size:
        return None

    content_type = res.getheader("Content-Type", default="").lower()

    if content_type not in allowed_img_types:
        return

    req.method = "GET"
    res = urllib.request.urlopen(req)

    try:
        return Image.open(res)
    except IOError:
        return None

async def action(bot, msg):
    """**!picmerge** _link1_ _link2_
Merges two images. Works with image links or emojis.
`!picmerge https://example.com/pic1.png https://example.com/pic2.png`"""
    cmd_args = [arg.strip() for arg in re.split(r"\s+", trigger.sub("", msg.clean_content).strip())]
    if len(cmd_args) < 2 or len(cmd_args) > 2:
        return
    img1 = get_image(bot, cmd_args[0])
    if not img1:
        return
    img2 = get_image(bot, cmd_args[1])
    if not img2:
        return
    img1 = img1.convert(mode = "RGBA")
    img2 = img2.convert(mode = "RGBA").resize(img1.size)
    img1.alpha_composite(img2)
    save_buffer = io.BufferedWriter(io.BytesIO())
    img1.save(save_buffer, format = "png")
    send_buffer = io.BytesIO(save_buffer.detach().getvalue())
    await msg.channel.send(file = discord.File(send_buffer, filename = "picmerge.png"))
            

        
