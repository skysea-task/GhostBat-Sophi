""" from RAUSHAN import *
from pyrogram import *

data, gmute = {}, {}

async def CmuteFilter(_, __, m):
  if m.chat.id in data:
    await m.delete()
  return False
    
@RAUSHAN.on_message(filters.command(['cmute', 'uncmute'], prefixes=HANDLER) & filters.me)
async def mute_chat(_, message):
  global data
  m = message
  if data.get(m.chat.id) and m.command[0] == 'cmute':
    return await message.reply("This chat has been muted already.")
  elif data.get(m.chat.id) and m.command[0] == 'uncmute':
    del data[m.chat.id]
    name = m.chat.title if hasattr(m.chat, 'title') else m.chat.first_name
    return await m.reply(f"Fine, {name} members can speak again.")
  elif m.from_user.id == m.chat.id:
    return await message.reply("You cannot mute yoyr chat.")
  data[m.chat.id] = True
  name = m.chat.title if hasattr(m.chat, 'title') else m.chat.first_name
  return await message.reply(f"Shhh, quiet now.\nMuted {name}")

@RAUSHAN.on_message(filters.create(CmuteFilter))
async def hander(_, m):
  pass
  