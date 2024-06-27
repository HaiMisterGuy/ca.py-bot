import re
import json
import os
import urllib.request
from discord import Embed
from ..utils import querify

trigger = re.compile("^!g(?:oogle)?")
keywords = ["g", "google"]

match_pattern = re.compile(r"^!g(?:oogle)?\s+(.+)")
base_url = "https://www.googleapis.com/customsearch/v1"
timeout_ms = 10 * 1000
default_params = json.load(open(os.path.abspath(os.path.dirname(__file__) + "/google.json")))
default_params["prettyPrint"] = "false"
default_params["fields"] = "items(title,link)"
default_params["num"] = 3

max_title_length = 80

def format_response(response):
    items = response.get("items")
    if items:
        embed = Embed()
        for item in items:
            embed.add_field(name=item["title"][:max_title_length], value=item["link"])
        return embed

async def action(bot, msg):
    """**!g** _search\_term_
Does a Google search for _search\_term_."""
    match = match_pattern.match(msg.clean_content)
    if match:
        params = dict(default_params)
        params["q"] = match.groups()[0]

        try:
            response = urllib.request.urlopen(base_url + querify(params)).read()
        except urllib.error.HTTPError as err:
            print("Google search request failed: %s" % err)
        else:
            try:
                parsed = json.loads(response.decode("utf-8"))
            except json.JSONDecodeError as err:
                print("Failed to parse Google search response: %s" % err)
            else:
                formatted = format_response(parsed)
                if formatted:
                    await msg.channel.send(embed=format_response(parsed))
                    #bot.send_message(msg.channel, embed=format_response(parsed))
