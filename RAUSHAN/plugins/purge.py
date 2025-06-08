""" from pyrogram import filters
from RAUSHAN.__main__ import RAUSHAN
from RAUSHAN import HANDLER
import asyncio
from pyrogram.enums import ChatType
import logging

@RAUSHAN.on_message(filters.command("purge", prefixes=HANDLER) & filters.me & filters.group)
async def purge_messages(_, message):
  if not message.reply_to_message:
    return await message.reply("Reply to the message you want to delete from.")
  start = message.reply_to_message.id
  end = message.id
  for x in range(start, end + 1, 100):
    try:
      x = list(range(x, x+101))
      await RAUSHAN.delete_messages(message.chat.id, x)
      await asyncio.sleep(3)
    except Exception as e:
      logging.error(f"Error deleting message {x}: {str(e)}")
  await message.reply("Purge complete.")
  
MOD_NAME = "Purge"
MOD_HELP = ".purge <reply> - To delete all messages from you replied one."