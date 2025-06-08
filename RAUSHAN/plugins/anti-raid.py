from RAUSHAN import *
from pyrogram import *
from pyrogram.types import *
from datetime import *

raids = {}

async def raid(_, __, m):
  if raids and m.chat.id in raids:
    await m.chat.ban_member(m.from_user.id, datetime.utcnow() + timedelta(hours=1))

@RAUSHAN.on_message(filters.command('antiraid', prefixes=HANDLER) & filters.me & filters.group)
async def raid_setting(_, m):
  global raids
  if m.chat.id in raids:
    del raids[m.chat.id]
    return await m.reply(f"Anti-raid disabled in {m.chat.title}.")
  raids[m.chat.id] = True
  return await m.reply(f"Anti-raid enabled in {m.chat.title}.")

@RAUSHAN.on_message(filters.new_chat_members & filters.create(raid))
async def BanMfs(_, m):
  pass  
MOD_NAME = "Antiraid"
MOD_HELP = "soonn"