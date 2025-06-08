""" from RAUSHAN import *
from config import OWNER_ID as OWN
from pyrogram import *
import asyncio
from pyrogram.enums import *

@RAUSHAN.on_message(filters.command(["pin", "unpin"], prefixes=HANDLER) & filters.user(OWN))
async def pin_unpin(_, message):
  if not message.reply_to_message:
    return await message.reply("ℹ️ Please reply to a message to pin/unpin")
  chat = message.chat
  if chat.type != ChatType.PRIVATE:
    member = await RAUSHAN.get_chat_member(chat.id, message.from_user.id)
    if member.status == ChatMemberStatus.MEMBER or not member.privileges.can_pin_messages:
      return await message.reply("**You don't have enough admin rights to use this command ❌**")
  action = RAUSHAN.pin_chat_message if message.command[0] == "pin" else RAUSHAN.unpin_chat_message
  try:
    await action(chat.id, message.reply_to_message.id, both_sides=True if message.command[0] == "pin" else None)
    await message.delete()
  except Exception as e:
    if "FLOOD_WAIT" in str(e):
      await asyncio.sleep(int(str(e).split()[8]))
      await action(chat.id, message.reply_to_message.id)
    else:
      await message.reply(f"**Error:** `{e}`")

MOD_NAME = 'Pin'
MOD_HELP = ".pin (reply) - To pin the replied message!\n.unpin (reply) - To unpin the replied message!"