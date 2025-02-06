import re
import urllib.request
import json
from ..utils import querify
from dateutil import parser
from discord import Embed

trigger = re.compile("^!ud")
keywords = ["ud", "urban", "urban dictionary"]

match_pattern = re.compile(r"^!ud\s+(.+)")
base_url = "http://api.urbandictionary.com/v0/define"

def get_term(term):
    params = {"term": term}
    try:
        response = urllib.request.urlopen(base_url + querify(params)).read()
    except urllib.error.HTTPError as err:
        print("Urban Dictionary request failed: %s" % err)
    else:
        try:
            parsed = json.loads(response.decode("utf-8"))
        except json.JSONDecodeError as err:
            print("Failed to parse Urban Dictionary response: %s" % err)
        else:
            if isinstance(parsed, dict):
                terms = parsed.get("list")
                if terms and isinstance(terms, list) and len(terms) > 0:
                    best = terms[0]
                    for term in terms:
                        if term.get("thumbs_up") > best.get("thumbs_up"):
                            best = term
                    return best

max_embed_field_length = 1024
max_embed_footer_length = 2048

async def action(bot, msg):
    """**!ud** _term_
Prints the Urban Dictionary definition for _term_."""
    match = match_pattern.match(msg.clean_content)
    if match:
        term = get_term(match.groups()[0])
        if term:
            embed = Embed()
            embed.set_footer(text=term["example"][:max_embed_footer_length])
            embed.timestamp = parser.parse(term["written_on"])
            await msg.channel.send(term["definition"], embed=embed)
            #bot.send_message(msg.channel, content=term["definition"], embed=embed)
        else:
            await bot.send_message(msg.channel, "¯\\_(ツ)_/¯")
