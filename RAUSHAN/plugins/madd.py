from RAUSHAN import HANDLER
from RAUSHAN.__main__ import RAUSHAN
from config import OWNER_ID
from pyrogram import filters
import asyncio
import time
from pyrogram.enums import ChatType

@RAUSHAN.on_message(filters.command("madd", prefixes=HANDLER) & filters.user(OWNER_ID) & filters.group)
async def mass_add(_, message):
    if len(message.command) < 2:
        return await message.reply("Please enter group user name to mass add.")
    time_start = time.time()
    success = 0
    chat_username = str(message.text.split(None, 1)[1])
    chat_info = await RAUSHAN.get_chat(chat_username)
    if not chat_username.startswith(('@', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
        return await message.reply("Please enter a valid id.")
    if chat_info.type == ChatType.PRIVATE or chat_info.type == ChatType.CHANNEL:
        return await message.reply('Please enter a group id')
        
    loading_msg = await message.reply("Adding members...")
    async for member in RAUSHAN.get_chat_members(message.chat.id):
        try:
            if not member.user.is_bot == True:
                output = await RAUSHAN.add_chat_members(chat_username, member.user.id)
                if output == True:
                    success += 1
                await asyncio.sleep(2)
        except Exception as e:
            if not str(e) == """Telegram says: [400 CHAT_ADMIN_REQUIRED] - The method requires chat admin privileges (caused by "messages.UpdatePinnedMessage")""" and not str(e).startswith("Telegram says: [420 FLOOD_WAIT_X] - A wait"):
                print(e)
    await loading_msg.delete()
    if success <= 0:
        return await message.reply(f"Failed to add members ❌")
    await message.reply(f"Successfully added {success} members\nTaken time: {int(time.time() - time_start)}")
