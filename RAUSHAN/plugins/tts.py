""" from gtts import gTTS
from RAUSHAN import HANDLER
from RAUSHAN.__main__ import RAUSHAN
from config import OWNER_ID
from pyrogram import filters
import asyncio
import os

@RAUSHAN.on_message(filters.command("tts", prefixes=HANDLER) & filters.user(OWNER_ID))
async def tts(_, message):
    m = message
    if len(message.command) < 2:
        return await m.reply(f"Please enter the language [code](https://graph.org/Language-codes-03-26)!", disable_web_page_preview=True)
    else:
        load = await m.reply('`Loading...`')
        try:
            if not message.reply_to_message or len(" ".join(message.command[1:])) > 2:
                text = message.text.split(None, 1)[1]
                language = 'en'
            else:
                text = message.reply_to_message.text
                if not text: text = message.reply_to_message.caption
                language = " ".join(message.command[1:])
            language = language.lower()
            tts = gTTS(text=text, lang=language, slow=True)
            tts.save("output.oga")
            await m.reply_voice("output.oga")
        except ValueError:
            await m.reply(f"Please enter a correct language [code](https://graph.org/Language-codes-03-26)!", disable_web_page_preview=True)
        except Exception as e:
            await m.reply(f"Error: {e}")
            raise Exception(f"Error in TTS: {e}")
        await load.delete()

MOD_NAME = 'TTS'
MOD_HELP = ".tts (text/reply) - To get that message text-to-speach."
