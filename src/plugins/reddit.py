import os
import json
import re
import urllib.request
import praw
from discord import Embed
from ..utils import rchop
import random

trigger = re.compile("^!r(?:eddit)?[^emove]")
keywords = ["r", "reddit", "fun"]
base_url = "https://reddit.com"
INIT_UNINIT = 1
INIT_SUCCESS = 2
INIT_FAIL = 3
init_status = INIT_UNINIT
config = None
reddit = None

def init():
    global init_status, config, reddit
    try:
        config_file = open(os.path.abspath(os.path.dirname(__file__) + "/reddit.json"))
    except OSError as err:
        pass
    else:
        try:
            config = json.load(config_file)
        except json.decoder.JSONDecodeError as err:
            pass
        else:
            try:
                reddit = praw.Reddit(
                    client_id=config["client_id"],
                    client_secret=config["client_secret"],
                    user_agent=config["user_agent"],
                    check_for_async=False)
                init_status = INIT_SUCCESS
                return
            except (praw.exceptions.PRAWException, prawcore.exceptions.PrawcoreException) as err:
                pass
    print("Reddit plugin initialization failed: %s" % (err))
    init_status = INIT_FAIL

def hasattr_oftype(o, p, t):
    return hasattr(o, p) and isinstance(getattr(o, p), t)

def side_effect(arg):
    pass

def fetch_post(post):
    try:
        # this is the recommended way to fetch a lazy object in praw...
        side_effect(post.title)
    except Exception as err:
        print("Could not fetch Reddit post: %s" % (err))
        return None
    else:
        return post
def make_post_url(post):
    return base_url + post.permalink

def embed_reddit_video(post):
    embed = Embed()
    reddit_video = post.secure_media["reddit_video"]
    embed.title = post.title
    embed.url = rchop(reddit_video["fallback_url"], "?source=fallback")
    embed.set_author(name="Reddit", url=make_post_url(post))
    embed.set_thumbnail(url=post.thumbnail)
    return embed

def embed_oembed(post):
    embed = Embed()
    oembed = post.secure_media["oembed"]
    embed.title = post.title
    embed.url = oembed.get("url", post.url)
    if "provider_name" in oembed:
        embed.set_author(name=oembed["provider_name"])
    return embed

def embed_reddit_image(post):
    embed = Embed()
    embed.title = post.title
    embed.url = make_post_url(post)
    embed.set_author(name="Reddit", url=make_post_url(post))
    embed.set_image(url=post.url)
    return embed

def get_post_content(post):
    # some kind of embeddable link post
    if hasattr_oftype(post, "secure_media", dict):
        # reddit video
        if "reddit_video" in post.secure_media:
            return embed_reddit_video(post)
        # oembed
        elif "oembed" in post.secure_media and "url" in post.secure_media["oembed"]:
            return embed_oembed(post)
    # reddit hosted image
    if hasattr(post, "post_hint"):
        if post.post_hint == "image":
            return embed_reddit_image(post)
    # regular link post
    if hasattr(post, "url"):
        return post.url
    return make_post_url(post)

def alt_random_post(sr):
    num_retry = 2
    limit = 1000
    rand = random.randint(0, limit - 1)
    for i in range(0, num_retry):
        i = 0
        for post in sr.hot(limit=limit):
            if i == rand:
                return post
            i += 1
        rand = rand % i

def nsfw_check(post, msg):
    # filter nsfw posts on sfw channels
    # does the over_18 attribute exist?
    if hasattr(post, "over_18"):
        # is the reddit post sfw or discord channel nsfw?
        if post.over_18 == False or msg.channel.nsfw:
            return False
        else:
            return True
    return False

async def action(bot, msg):
    """**!r** _subreddit_
Show random post from a subreddit.
`!r bigfoot`"""
    if init_status == INIT_UNINIT:
        init()
        #await msg.channel.send(init_status)
    if init_status == INIT_FAIL:
        return
    args = msg.clean_content.split(" ")[1:]
    #sr = reddit.random_subreddit() if len(args) < 1 else reddit.subreddit(args[0])
    #try:
    #    post = sr.random()
    #except praw.exceptions.ClientException as err:
    #    print(err)
    #    post = alt_random_post(sr)
    #post = fetch_post(post)
    sr = reddit.random_subreddit() if len(args) < 1 else reddit.subreddit(args[0])
    post = alt_random_post(sr)
    post = fetch_post(post)
    if post:
        if nsfw_check(post, msg):
            try:
                await bot.send_message(msg.channel, "eyyy " + msg.author.display_name + ", get dat " + args[0] + " shid outta dis christian discord channel", escape_formatting=False)
            except Exception as e:
                print(e)
        else:
            result = get_post_content(post)
            if isinstance(result, Embed):
                #await msg.channel.send("sdfsdef")
                #await msg.channel.send(embed=get_post_content(post))
                await bot.send_message(msg.channel, embed=result, escape_formatting=False)
            else:
                #await msg.channel.send("no")
                #await msg.channel.send(get_post_content(post))
                await bot.send_message(msg.channel, result, escape_formatting=False)