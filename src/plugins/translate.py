import re
import json
import urllib.request
from ..utils import querify

trigger = re.compile("^!tr(?:anslate)?")
keywords = ["tr", "translate"]

match_pattern = re.compile(r"^!tr(?:anslate)?\s+(\S+)\s+(\S+)\s*(.*)", re.DOTALL)
newline = re.compile(r"\n")
base_url = "https://translate.google.com/translate_a/single"
default_params = {
    "client": "gtx",
    "ie": "UTF-8",
    "oe": "UTF-8",
    "dt": ("ld", "qca", "t")
}
languages = [
    "af",
    "sq",
    "ar",
    "hy",
    "az",
    "eu",
    "be",
    "bn",
    "bs",
    "bg",
    "ca",
    "ceb",
    "ny",
    "zh-CN",
    "zh-TW",
    "hr",
    "cs",
    "da",
    "nl",
    "en",
    "eo",
    "et",
    "tl",
    "fi",
    "fr",
    "gl",
    "ka",
    "de",
    "el",
    "gu",
    "ht",
    "ha",
    "iw",
    "hi",
    "hmn",
    "hu",
    "is",
    "ig",
    "id",
    "ga",
    "it",
    "ja",
    "jw",
    "kn",
    "kk",
    "km",
    "ko",
    "lo",
    "la",
    "lv",
    "lt",
    "mk",
    "mg",
    "ms",
    "ml",
    "mt",
    "mi",
    "mr",
    "mn",
    "my",
    "ne",
    "no",
    "fa",
    "pl",
    "pt",
    "ma",
    "ro",
    "ru",
    "sr",
    "st",
    "si",
    "sk",
    "sl",
    "so",
    "es",
    "su",
    "sw",
    "sv",
    "tg",
    "ta",
    "te",
    "th",
    "tr",
    "uk",
    "ur",
    "uz",
    "vi",
    "cy",
    "yi",
    "yo",
    "zu"
]

url_opener = urllib.request.build_opener()
url_opener.addheaders = [("User-Agent", "Mozilla/5.0")]

def get_url(msg_text):
    match = match_pattern.match(msg_text)
    if match:
        params = dict(default_params)
        (arg1, arg2, arg3) = match.groups()
        arg2_is_valid = arg2 in languages
        arg1_is_valid = arg1 in languages

        if arg2_is_valid and arg1_is_valid:
            params["sl"] = arg1
            params["tl"] = arg2
            params["q"] = newline.sub(" ", arg3)
            return base_url + querify(params, True)
        elif arg1_is_valid:
            params["tl"] = arg1
            params["q"] = newline.sub(" ", arg2)
            return base_url + querify(params, True)

def format_response(response):
    try:
        return response[0][0][0]
    except Exception:
        pass

doc = "**!tr** [_source\_lang_] _target\_lang_ _text_\n" \
"Translates _text_ from _source\_lang_ to _target\_lang_ using Google Translate. " \
"If _source\_lang_ is omitted then the language is automatically detected.\n_source\_lang_ and _target\_lang_ must be one of the following: " + languages[0]

for lang in languages[1:]:
    doc += ", " + lang
doc += "."

async def action(bot, msg):
    url = get_url(msg.clean_content)
    if url:
        try:
            response = url_opener.open(url).read()
        except urllib.error.HTTPError as err:
            print("Google Translate request failed: %s" % err)
        else:
            try:
                parsed = json.loads(response.decode("utf-8"))
            except json.JSONDecodeError as err:
                print("Failed to parse Google Translate response: %s" % err)
            else:
                formatted = format_response(parsed)
                if formatted:
                    await bot.send_message(msg.channel, formatted)

action.__doc__ = doc
