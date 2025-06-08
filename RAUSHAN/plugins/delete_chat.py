""" from pyrogram.enums import ChatType
from pyrogram import *
from RAUSHAN import *
from config import OWNER_ID

@RAUSHAN.on_message(filters.command("delchat", HANDLER) & filters.user('me'))
async def delete_chat(_, m):
  if not m.chat.type == ChatType.PRIVATE and not m.chat.type == ChatType.BOT:
    return await m.reply("Please use this command on private chat!")
  if m.chat.id == OWNER_ID:
    return await m.reply("Sorry you cannot use this here!")
  try:
    await RAUSHAN.delete_chat_history(m.chat.id, revoke=True)
  except Exception as e:
    print(f"Something went wrong while deleting chat on {m.chat.id}: {e}")
