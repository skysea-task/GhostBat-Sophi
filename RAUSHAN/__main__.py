import threading
from RAUSHAN import *
from pyrogram import Client, filters
import os
from pyrogram import idle
from subprocess import getoutput as r
from Restart import restart_program
import asyncio 

PWD = f"{os.getcwd()}/"
my_id = None

async def fk():
  await RAUSHAN.start()
  await RAUSHANBot.start()
  try:
    await RAUSHANBot.send_photo(
      RAUSHAN.me.id,
      photo="https://i.imgur.com/DuoscLX.jpeg",
      caption=(
        f"**✅ 𝐇𝐞𝐚𝐫𝐭𝐁𝐞𝐚𝐭-✗-𝐁𝐨𝐭 ⚡**\n\n"
        f"**👾 Version:** {MY_VERSION}\n"
        f"**🥀 Python:** {r('python --version').lower().split('python ')[1]}\n"
        f"**🐬 Owner:** {RAUSHAN.me.first_name if not RAUSHAN.me.last_name else f'{RAUSHAN.me.first_name} {RAUSHAN.me.last_name}'}\n"
        f"**🦋 Join:**@HeartBeat_Muzic"
      )
    )
  except: pass
  await idle()
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(fk())
    
    
