import json
from src.bot import Bot
import os

config = json.load(open(os.path.abspath("./config.json")))
bot = Bot(config)
bot.run()
