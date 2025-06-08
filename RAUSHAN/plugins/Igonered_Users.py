from RAUSHAN import *
from RAUSHAN.__main__ import RAUSHAN
from config import OWNER_ID
from pyrogram import filters
from RAUSHAN.database.ignore_users import *

async def ignore_users(_, client, update):
    ignore_usr = IGNORED_USERS()
    if update.chat.id not in await ignore_usr.GET():
        return False
    else:
        if update.from_user.id == OWNER_ID:
            return False
        return True

warning_count = {}

@RAUSHAN.on_message(filters.private & filters.create(ignore_users))
async def ignored_private_chat(_, message):
    user_id = message.chat.id
    if user_id not in warning_count:
        warning_count[user_id] = 0
    warning_count[user_id] += 1
    if warning_count[user_id] == 1:
        await message.reply("Sorry, you are a ignored person of my master you can't chat with him!")
        await RAUSHAN.archive_chats([message.chat.id])
    elif warning_count[user_id] == 2:
        await message.reply("This is your second warning. If you send another message, you will be blocked.")
    elif warning_count[user_id] >= 3:
        try:
            await message.reply("Sorry, You have breaked your limits so i blocked you")
            await RAUSHAN.block_user(user_id)
            await RAUSHAN.send_message(LOG_CHANNEL, f"Master, i have blocked {message.from_user.first_name}\n\nHe/she spamed in your chat so i blocked if you want unblock you can find them in archived chats! use .unignore to unignore them!")
        except Exception as e:
            print(e)
            await RAUSHAN.send_message(LOG_CHANNEL, f"Sorry Master, I got an error when blocking Ignored User. Check Errors Below 💔\n {e}")

@RAUSHAN.on_message(filters.command("ignore", prefixes=HANDLER) & filters.private & filters.me)
async def add_ignored_person(_, message):
    if message.chat.id == OWNER_ID:
        return await message.reply("You can't ignore yourself!")
    USRS = IGNORED_USERS()
    if message.chat.id in await USRS.GET():
        return await message.reply("This person already in ignored list!")
    else:
        try:
            H = await USRS.ADD(message.chat.id)
            if H == "SUCCESS":
                await message.reply("I have started ignoring this person!")
            else:
                await message.reply(f'Error {H}')
        except Exception as e:
            await message.reply(f'Error {e}')

@RAUSHAN.on_message(filters.command("unignore", prefixes=HANDLER) & filters.private & filters.me)
async def remove_ignored_person(_, message):
    if message.chat.id == OWNER_ID:
        return await message.reply("You can't unignore yourself!")
    USRS = IGNORED_USERS()
    if message.chat.id not in await USRS.GET():
        return await message.reply("This person is not in ignored list!")
    else:
        try:
            H = await USRS.REMOVE(message.chat.id)
            if H == "SUCCESS":
                await message.reply("I have removed this person in ignored list!")
            else:
                await message.reply(f"Error, {H}")
        except Exception as e:
            await message.reply(f"Error {e}")
