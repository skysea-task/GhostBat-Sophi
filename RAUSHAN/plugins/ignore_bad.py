from RAUSHAN import HANDLER
from RAUSHAN.__main__ import RAUSHAN
from config import OWNER_ID
from RAUSHAN.database.ignore_bad import *
from pyrogram import filters
import asyncio
import re

async def bad_word_remover_stats(_, client, update):
    ignore_bad = IGNORE_BAD()
    is_enabled = await ignore_bad.GET()
    if is_enabled:
        return True
    else:
        return False

bad_words = [
    'punda', 'fuck', 'ommala',
    'kena', 'mairu', 'savu',
    'otha', 'oththa', 'rape',
    'pussy', 'dick', 'kunji',
    'kunju', 'thevidiya', 'peins',
    'bitch', 'motherfucker', 'fucker',
    'omala', 'pota', 'kenapunda',
    'mairupunda', 'sex', 'sexchat'
]

pattern = r"\b(?:{})\b".format('|'.join(['{}(?:{})?'.format(re.escape(word), '[a-zA-Z]*' * (len(word)-1)) for word in bad_words]))

@RAUSHAN.on_message(filters.text & filters.regex(pattern, re.IGNORECASE) & filters.create(bad_word_remover_stats))
async def remove_message(_, message):
    try:
        await message.delete()
    except Exception as e:
        if str(e) == """Telegram says: [403 MESSAGE_DELETE_FORBIDDEN] - You don't have rights to delete messages in this chat, most likely because you are not the author of them (caused by "channels.DeleteMessages")""":
            print(str(e))
            return
        print(e)
        await RAUSHAN.send_message(message.chat.id, f"Error: {e}")

@RAUSHAN.on_message(filters.command(["ignorebad", "stopbad"], prefixes=HANDLER) & filters.me)
async def set_ignore_bad(_, message):
    try:
        ignore_bad = IGNORE_BAD()
        log = await ignore_bad.ENABLE()
        if log == "SUCCESS":
            await message.reply("Let's ignore bad things!")
        else:
            await message.reply(f"Error: {log}")
            print(log)
    except Exception as e:
        await message.reply(f"Error: {e}")
        print(e)
        
@RAUSHAN.on_message(filters.command(["unignorebad", "unstopbad"], prefixes=HANDLER) & filters.me)
async def unset_ignore_bad(_, message):
    try:
        ignore_bad = IGNORE_BAD()
        log = await ignore_bad.DISABLE()
        if log == "SUCCESS":
            await message.reply("Okay, I stoped ignoring bad things!")
        else:
            await message.reply(f"Error: {log}")
            print(log)
    except Exception as e:
        await message.reply(f"Error: {e}")
        print(e)
        
