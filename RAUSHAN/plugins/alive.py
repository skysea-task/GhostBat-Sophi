from RAUSHAN import *
from RAUSHAN import MY_VERSION as Root_version
from RAUSHAN.__main__ import RAUSHAN
from config import OWNER_ID as OWN
from pyrogram import filters
from pyrogram import __version__ as ver_pyro
import asyncio
from datetime import datetime
import os
from subprocess import getoutput as run

@RAUSHAN.on_message(filters.command("alive", prefixes=HANDLER) & filters.user(OWN))
async def RAUSHAN_Alive(_, message):
    await message.edit("`◖⁠⚆⁠ᴥ⁠⚆⁠◗ Loading...`")
    await asyncio.sleep(0.8)
    bot_inf = await RAUSHAN.get_me()
    Name_of_ubot1 = bot_inf.first_name
    Name_of_ubot2 = bot_inf.last_name
    start_time = bot_start_time
    end_time = datetime.now()
    ping_time = (end_time - start_time).total_seconds() * 1000
    uptime = (end_time - bot_start_time).total_seconds()
    hours, remainder = divmod(uptime, 3600)
    minutes, seconds = divmod(remainder, 60)
    if Name_of_ubot2 == None:
        Name_of_ubot = Name_of_ubot1
    else:
        Name_of_ubot = f"{Name_of_ubot1} {Name_of_ubot2}"
    try: py_ver = str(run('python --version').lower().split('python ')[1])
    except Exception as e:
        print(e)
        py_ver = "Error"
    TEXT = f""" **𝅗ـﮩ٨ـ𝅽𝅾𓆩𝐇𖽞𖽖֯֟፝͢͡𖽸𖾓𝂬𓏲ࣹ᷼𝄢𝂬𝐁𖽞֟֠֯፝͢͡𖽖𖾓𓆪ﮩ٨ـ𝅽𝅾‐𝅘**
━━━━━━━━━━━━━━━━━━━━━━━━━

❥ **Owner**: {Name_of_ubot}
❥ **My Version**: `{Root_version}`
❥ **Python Version**: `{py_ver}`
❥ **Pyrogram Version:** `{ver_pyro}`
❥ **Uptime:** `{int(hours)}h {int(minutes)}m {int(seconds)}s`

━━━━━━━━━━━━━━━━━━━
**Join @HeartBeat_Muzic ✨🥀**
"""
    await message.delete()
    await RAUSHAN.send_photo(message.chat.id, photo="https://graph.org/file/9ee37cccd7bf55c3ec953.png", caption=TEXT)
