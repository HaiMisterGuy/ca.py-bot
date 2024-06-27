from datetime import datetime, timedelta
from random import randint
import urllib.parse
import re

def discord_snowflake_to_datetime(snowflake):
    return datetime.fromtimestamp(((int(snowflake) / 4194304) + 1420070400000) / 1000)

def random_date_between(a, b):
    maxval = int((b - a).total_seconds())
    d = timedelta(seconds=randint(0, maxval))
    return a + d

def querify(params, allow_duplicates=False):
    return "?" + urllib.parse.urlencode(params, doseq=allow_duplicates)

discord_escape_match_pattern = re.compile(r"([*_~`\[\]\(\)\\])")
discord_escape_replace_pattern = r"\\\g<1>"
def discord_escape(text):
    return discord_escape_match_pattern.sub(discord_escape_replace_pattern, text)

# from https://en.wikibooks.org/w/index.php?title=Algorithm_Implementation/Strings/Levenshtein_distance&oldid=3381735#Python
def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def rchop(my_str, suffix):
    if my_str.endswith(suffix):
        return my_str[:-len(suffix)]
    return my_str
