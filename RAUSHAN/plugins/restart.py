from Restart import restart_program
from RAUSHAN import *
from RAUSHAN.helpers import *
from config import OWNER_ID as OWN
from pyrogram import filters
import asyncio
import os
from datetime import datetime
import pytz

@RAUSHAN.on_message(filters.command(["xrestart", 'trestart'], prefixes=HANDLER) & filters.user(OWN))
async def restart(_, message):
  if message.command[0] == 'trestart':
    try:  
      txt, ist = " ".join(message.command[1:]), pytz.timezone('Asia/Kolkata')
      if int(txt[:-1]) <= 5 and txt.endswith('s'):
        return await message.reply("Time should be greater than 5 sec.")
      x = await GetTime(txt)
      fk, s, n, e = await message.edit(f"Done! userbot will be restarted in {txt}"), datetime.now(ist).strftime("%H:%M:%S"), await asyncio.sleep(x), datetime.now(ist).strftime("%H:%M:%S")
      await RAUSHANBot.send_message(message.from_user.id, f"**🔴 Restarting...**\n\n**🕐 Set on:** {s}\n**⌚ End on:** {e}\n\n**Powered by:** @HeartBeat_Muzic")
    except: return await message.edit("Nooo, this is not correct time format.\nUse: `.trestart 1h`")
  try: await message.edit("Restarting...")
  except: pass
  restart_program()
