# LOL MODULE, I don't know why i created this 😂

from RAUSHAN import HANDLER
from RAUSHAN.__main__ import RAUSHAN
from config import OWNER_ID
from pyrogram import filters

@RAUSHAN.on_message(filters.command(["echo", "recho"], prefixes=HANDLER) & filters.user(OWNER_ID))
async def echo(_, m):
  message=m
  try:
    if len(m.command) >= 2 or m.reply_to_message:
      await m.delete()
  except:
    pass 
  if m.reply_to_message and len(m.command) < 2:
    if m.text[1:].lower().startswith('r') or m.text.lower().startswith('r'):
      if not m.reply_to_message.media_group_id:
        return await RAUSHAN.copy_message(m.chat.id, m.chat.id, m.reply_to_message.id, reply_to_message_id=m.reply_to_message_id)
      return await RAUSHAN.copy_media_group(m.chat.id, m.chat.id, m.reply_to_message.id, reply_to_message_id=m.reply_to_message_id)
    else:
      if not m.reply_to_message.media_group_id:
        return await RAUSHAN.copy_message(m.chat.id, m.chat.id, m.reply_to_message.id)
      return await RAUSHAN.copy_media_group(m.chat.id, m.chat.id, m.reply_to_message.id)
  else:
    if len(m.command) >= 2:
      txt = m.text.split(None, 1)[1]
      if m.reply_to_message:
        return await m.reply_to_message.reply(txt)
      return await RAUSHAN.send_message(m.chat.id, txt)
MOD_NAME = "Echo"
MOD_HELP = ".echo (text or reply) - To send that message\n.recho (reply) - To send the message you replied with reply of original message"
