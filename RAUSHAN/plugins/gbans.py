from RAUSHAN import HANDLER
from RAUSHAN.__main__ import RAUSHAN
from pyrogram import filters
import asyncio
import time
from pyrogram import enums, errors

async def ban_unban_user(message, action, user_id):
    me = message.from_user.id
    if user_id == message.from_user.id:
        return await message.reply("⚠️ You can't do this on yourself")
    success_chats = 0
    time_start = time.time()
    loading_msg = await message.reply(f"Processing...")
    async for dialog in RAUSHAN.get_dialogs():
        if dialog.chat.type in [enums.ChatType.SUPERGROUP, enums.ChatType.GROUP]:
            try:
                if action == 'ban':
                    await RAUSHAN.ban_chat_member(dialog.chat.id, user_id)
                else:
                    await RAUSHAN.unban_chat_member(dialog.chat.id, user_id)
                success_chats += 1
                await asyncio.sleep(2)
            except errors.ChatAdminRequired:
                print(f"Admin rights required in chat {dialog.chat.id}")
            except errors.FloodWait as e:
                print(f"Flood wait of {e.value} seconds")
                await asyncio.sleep(e.value)
            except Exception as e:
                print(f"Error in chat {dialog.chat.id}: {e}")

    await loading_msg.delete()
    await message.reply(f"""**✅ {'Gban' if action == 'ban' else 'Ungban'} Summary 🐬**

**🚫 Successfully baned:** __{success_chats}chats__
**👤 User:** __{user_id}__
**🕒 Taken Time:** __{int(time.time() - time_start)}s__

**» 🦋 Join:** @HeartBeat_Muzic
    """)


@RAUSHAN.on_message(filters.command("gban", prefixes=HANDLER) & filters.user("me"))
async def gban(_, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) >= 2:
        user_id = str(message.command[1])
        try: user_id = await RAUSHAN.get_users(user_id)
        except: return await message.reply("Please enter a valid id 🆔.")
        user_id = user_id.id
    else:
        return await message.reply("⚠️ Please reply to a user or enter their user-id.")
    await ban_unban_user(message, action="ban", user_id=user_id)


@RAUSHAN.on_message(filters.command("ungban", prefixes=HANDLER) & filters.user("me"))
async def ungban(_, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) >= 2:
        user_id = str(message.command[1])
        try: user_id = await RAUSHAN.get_users(user_id)
        except: return await message.reply("Please enter a valid id 🆔.")
        user_id = user_id.id
    else:
        return await message.reply("⚠️ Please reply to a user or enter their user-id.")
    await ban_unban_user(message, action="unban", user_id=user_id)
