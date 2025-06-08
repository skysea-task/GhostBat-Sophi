from RAUSHAN import HANDLER
from RAUSHAN.__main__ import RAUSHAN
from config import OWNER_ID
from pyrogram import filters
from RAUSHAN.database.copy_msg import *
import asyncio
import os

@RAUSHAN.on_message(filters.command("copy", prefixes=HANDLER) & filters.user(OWNER_ID))
async def Copy_msg(_, message):
    await message.delete()
    if not message.reply_to_message:
        return await message.reply("Reply to a message to copy it.")
    else:
        try:
            if message.reply_to_message.media_group_id is None:
                COPIED_MSG = message.reply_to_message_id
                COPIED_MSG_CHAT = message.chat.id
                STORE = await SAVE_MSG(COPIED_MSG, COPIED_MSG_CHAT, album=False)
                if STORE == "SUCCESS":
                    await message.reply("Successfully copied!")
                else:
                    await message.reply(f"Error: {STORE}")
            else:
                COPIED_MSG = message.reply_to_message_id
                COPIED_MSG_CHAT = message.chat.id
                STORE = await SAVE_MSG(COPIED_MSG, COPIED_MSG_CHAT, album=True)
                if STORE == "SUCCESS":
                    await message.reply("Successfully copied!")
                else:
                    await message.reply(f"Error: {STORE}")
        except Exception as e:
            return await message.reply(f"Error: {e}")

@RAUSHAN.on_message(filters.command(["dcopy", "rcopy", "delcopy"], prefixes=HANDLER) & filters.user(OWNER_ID))
async def del_msg_copy(_, message):
    STATUS = await UNSAVE_MSG()
    if STATUS == "SUCCESS":
        await message.reply("Copy deleted!")
    else:
        await message.reply(f"Error: {STATUS}")
    
@RAUSHAN.on_message(filters.command("paste", prefixes=HANDLER) & filters.user(OWNER_ID))
async def paste_msg(_, message):
    await message.delete()
    COPIED_MSG = await COPIED()
    if not COPIED_MSG == True:
        return await message.reply("Clipboard is empty.")
    else:
        try:
            if message.reply_to_message:
                if await IS_ALBUM() == True:
                    return await RAUSHAN.copy_media_group(message.chat.id, await CHAT_ID(), await MSG_ID(), reply_to_message_id=message.reply_to_message_id)
                else:
                    return await RAUSHAN.copy_message(message.chat.id, await CHAT_ID(), await MSG_ID(), reply_to_message_id=message.reply_to_message_id)
            if await IS_ALBUM() == True:
                return await RAUSHAN.copy_media_group(message.chat.id, await CHAT_ID(), await MSG_ID())
            else:
                return await RAUSHAN.copy_message(message.chat.id, await CHAT_ID(), await MSG_ID())
        except Exception as e:
            if str(e).startswith("Telegram says: [400 CHAT_FORWARDS_RESTRICTED]"):
                return await message.reply("Master, Copying forwarding not allowed in that chat so we cannot paste it.")
            await message.reply(f"Error: {e}")

@RAUSHAN.on_message(filters.command("ncpaste", prefixes=HANDLER) & filters.user(OWNER_ID))
async def no_caption_paste_msg(_, message):
    await message.delete()
    COPIED_MSG = await COPIED()
    if not COPIED_MSG == True:
        return await message.reply("Clipboard is empty.")
    else:
        try:
            if message.reply_to_message:
                if await IS_ALBUM() == True:
                    return await RAUSHAN.copy_media_group(message.chat.id, await CHAT_ID(), await MSG_ID(), reply_to_message_id=message.reply_to_message_id, caption="")
                return await RAUSHAN.copy_message(message.chat.id, await CHAT_ID(), await MSG_ID(), reply_to_message_id=message.reply_to_message_id, caption="")
            if await IS_ALBUM() == True:
                return await RAUSHAN.copy_media_group(message.chat.id, await CHAT_ID(), await MSG_ID(), caption="")
            return await RAUSHAN.copy_message(message.chat.id, await CHAT_ID(), await MSG_ID(), caption="")
        except Exception as e:
            if str(e).startswith("Telegram says: [400 CHAT_FORWARDS_RESTRICTED]"):
                return await message.reply("Master, Copying forwarding not allowed in that chat so we cannot paste it.")
            await message.reply(f"Error: {e}")

MOD_HELP = "Copy"
MOD_HELP = ".copy (reply) - To copy that message and paste anywhere (must be that chat allow copy&forwarding)\n.paste - To paste the copied message"
