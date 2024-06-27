import re

trigger = re.compile("^!help")
keywords = ["help"]

match_pattern = re.compile(r"^!help\s*(.*)")

async def action(bot, msg):
    """**!help** _command_
Display help for _command_."""
    match = match_pattern.match(msg.clean_content)
    if match:
        query = match.groups()[0]
        if not query:
            query = "help"

        plugin = bot.find_plugin_by_keyword(query)
        if plugin and plugin.__file__ == __file__:
            doc = action.__doc__
            kws = bot.get_good_plugin_keywords()
            doc += "\nAvailable commands: " + kws[0]
            for kw in kws[1:]:
                doc += ", " + kw
            doc += "."
            await bot.send_message(msg.channel, doc, escape_formatting=False)
        elif hasattr(plugin, "action") and plugin.action.__doc__:
            await bot.send_message(msg.channel, plugin.action.__doc__, escape_formatting=False)
        else:
            await bot.send_message(msg.channel, "No help entry found for %s" % query)
