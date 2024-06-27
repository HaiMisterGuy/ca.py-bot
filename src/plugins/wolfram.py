import os
import json
import re
import urllib.request
import xml.etree.cElementTree as etree
from ..utils import querify

trigger = re.compile("^!(?:wolfram|wa)")
keywords = ["wa", "wolfram", "wolfram alpha"]

match_pattern = re.compile(r"^!(?:wolfram|wa)\s+(.+)")
base_url = "http://api.wolframalpha.com/v2/query"

def get_params():
    try:
        params = json.load(open(os.path.abspath(os.path.dirname(__file__) + "/wolfram.json")))
        params["format"] = "plaintext"
        params["parsetimeout"] = 30
        params["podtimeout"] = 30
        params["scantimeout"] = 30
        return params
    except:
        return None

result_queries = [
    ".pod[@title='Result']/subpod/plaintext",
    ".pod[@title='Name']/subpod/plaintext",
    ".pod[@title='Basic Information']/subpod/plaintext",
    ".pod[@title='Weather forecast']/subpod/plaintext",
    ".pod/subpod/plaintext"
]

def format_response(response):
    root = etree.fromstring(response)
    for query in result_queries:
        for element in root.findall(query)[::-1]:
            if element.text:
                return element.text

async def action(bot, msg):
    """**!wa** _query_
Query Wolfram Alpha the computational knowledge engine.
`!wa what is the average air speed of an unladen swallow`"""
    params = get_params()
    if params == None:
        return
    params = dict(params)
    match = match_pattern.match(msg.clean_content)
    if match:
        params["input"] = match.groups()[0]
        try:
            response = urllib.request.urlopen(base_url + querify(params)).read()
        except urllib.error.HTTPError as err:
            print("Wolfram Alpha query request failed: %s" % err)
        else:
            formatted = format_response(response.decode("utf-8"))
            if formatted:
                await bot.send_message(msg.channel, formatted)
            else:
                await bot.send_message(msg.channel, "¯\\_(ツ)_/¯")
