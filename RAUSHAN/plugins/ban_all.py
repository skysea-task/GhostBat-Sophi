""" from RAUSHAN import *
import logging
from config import OWNER_ID as OWN
from pyrogram import *
from pyrogram.types import *
import asyncio
from pyrogram import enums

info = logging.info
async def is_admin(chat_id: int, user_id: int):
  member = await RAUSHAN.get_chat_member(chat_id, user_id)
  return member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]

@RAUSHAN.on_message(filters.command("unbanall", prefixes=HANDLER) & filters.user(OWN))
async def unbanall(_, message):
  user_id, chat_id = message.from_user.id, message.chat.id
  if not await is_admin(chat_id, user_id):
    return
  elif message.chat.type == enums.ChatType.PRIVATE:
    return await message.reply("Sorry, This Command Only works in Groups!")
  else:
    try:
      msg = await message.reply("Processing...")
      BANNED, unban = [], 0
      async for m in RAUSHAN.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BANNED):
        BANNED.append(m.user.id)
        try:
          await RAUSHAN.unban_chat_member(chat_id, m.user.id)
          unban += 1
        except: pass
        await asyncio.sleep(1.2)
      m, f = await message.reply("Found Banned Members: {}\nUnbanned Successfully: {}".format(len(BANNED), unban)), await msg.delete()
    except Exception as e:
      if "CHAT_ADMIN_REQUIRED" in str(e):
        return await message.reply_text("**Sorry**, `I don't have Admin rights to do this!. ❌`")
      await message.reply(f"**Error:** {e}")
      info(e)

@RAUSHAN.on_message(filters.command("banall", prefixes=HANDLER) & filters.user(OWN))
async def banall(_, message):
  user_id, chat_id = message.from_user.id, message.chat.id  
  if not await is_admin(chat_id, user_id):
    return
  elif message.chat.type == enums.ChatType.PRIVATE:
    return await message.reply("This Command Only works in Groups!")
  else:
    try:
      msg = await message.reply("Processing...")
      Members, Admins = [], []
      async for x in RAUSHAN.get_chat_members(chat_id):
        if not x.privileges: Members.append(x.user.id)
        else: Admins.append(x.user.id)
      for user_id in Members:
        try:
          await RAUSHAN.ban_chat_member(chat_id, user_id)
          await RAUSHAN.unban_chat_member(chat_id, user_id)
          await asyncio.sleep(1.2)
        except Exception: info(Exception)
      m, f = await message.reply("Successfully Banned: {}\nRemaining Admins: {}".format(len(Members), len(Admins))), await msg.delete()
    except Exception as e:
      await message.reply_text(f"**Error:** {e}")
      info(e)

@RAUSHAN.on_message(filters.command("kickall", prefixes=HANDLER) & filters.user(OWN))
async def kickall(_, message):
  user_id, chat_id = message.from_user.id, message.chat.id
  if not await is_admin(chat_id, user_id):
    return
  elif message.chat.type == enums.ChatType.PRIVATE:
    return await message.reply("This Command Only works in Groups!")
  else:
    msg = await message.reply("Processing...")
    try:
      Admins, Members = [], []
      async for x in RAUSHAN.get_chat_members(chat_id):
        if not x.privileges: Members.append(x.user.id)
        else: Admins.append(x.user.id)
      for user_id in Members:
        try:
          await RAUSHAN.ban_chat_member(chat_id, user_id)
          await RAUSHAN.unban_chat_member(chat_id, user_id)
          await asyncio.sleep(1.2)
        except Exception: info(Exception)
      m, f = await message.reply_text("Successfully Kicked: {}\nRemaining Admins: {}".format(len(Members), len(Admins))), await msg.delete()
    except Exception as e:
      if "CHAT_ADMIN_REQUIRED" in str(e):
        return await message.reply_text("You don't have enough admin rights to do this 🚫")
      await message.reply_text(f"**Error:** {e}")
      info(e)

MOD_NAME = 'Bans'
MOD_HELP = """

""" **⚕️ Banall**
.banall - To ban all members from a group.
.unbanall - To unban all members from a group.
.kickall - To kick all members from a group.

**🥀 Normal-Ban**
.ban <Reply/id> - To ban them.
.kick <Reply/id> - To kick them.
.unban <Reply/id> - To unban them.
**💡 LMAO:** Don't try to test this and destroy your group!
"""