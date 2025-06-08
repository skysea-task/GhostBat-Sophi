""" from RAUSHAN import HANDLER
from RAUSHAN.__main__ import RAUSHAN
from config import OWNER_ID, BOTS_ALLOWED_TO_WORK_IN_BUSY_COMMANDS
from pyrogram import filters
import asyncio
import os
from Restart import restart_program
from pyrogram import enums
from RAUSHAN.database.backup_msg import *
from RAUSHAN.database.pmguard import *
from RAUSHAN.plugins.message_handler import warning_count
        
@RAUSHAN.on_message(filters.command(["pmblock", "pmguard"], prefixes=HANDLER) & filters.user(OWNER_ID))
async def set_pm_guard(_, message):
    is_pm_block_enabled = await GET_PM_GUARD()
    if is_pm_block_enabled:
        await UNSET_PM_GUARD()
        await message.reply("**➲ I have Disabled PmGuard Successfully ✅**")
        return
    else:
        if len(message.command) < 2:
            RESULT = await GET_DEFAULT_MESSAGE_LIMIT()
            RESULT2 = str(RESULT)
            if RESULT2.isdigit():
                await SET_PM_GUARD(RESULT)
                return await message.reply('**➲ I have enabled PmGuard successfully with Default Warning limit 🥀 ✨**')
            else:
                return await message.reply_text("➲ Master, Please enter the maximum message warning limit.")
        count = " ".join(message.command[1:])
        intCount = int(count)
        if intCount == 1:
            await message.reply("➲ Master, Count must be atleast 2.")
            return
        if intCount <= 0:
            await message.reply("➲ Master, Count must be positive Integers.")
            return
        if intCount > 20:
            await message.reply("➲ Maximum Applable warning count is 20.")
            return
        await SET_PM_GUARD(intCount)
        await message.reply('**➲ I have enabled PmGuard successfully 🥀 ✨**')
    

@RAUSHAN.on_message(filters.command(['a', 'approve', 'allow'], prefixes=HANDLER) & filters.user(OWNER_ID))
async def approve_user(_, message):
    is_pm_block_enabled = await GET_PM_GUARD()
    approved_users = await GET_APPROVED_USERS()
    if is_pm_block_enabled:
        if message.chat.type == enums.ChatType.SUPERGROUP:
            await message.reply("➲ This Command Only Works On Private Chats ❌.")
            return
        user_id = message.chat.id
        try:
            if user_id in approved_users:
                await message.reply('**➲ This User is already approved ✨ 🥀**')
                return
            await ADD_APPROVED_USER(user_id)
            await message.reply("➲ Successfully Approved 🥀⚡")
        except Exception as e:
            await message.reply(f"Sorry, i got a error while approving this user\n\n{e}")
    else:
        if message.chat.type == enums.ChatType.SUPERGROUP:
            return
        await message.reply('**➲ PmGuard Not Enabled ❌.**')


@RAUSHAN.on_message(filters.command(['ua', 'unapprove', 'deny', 'd'], prefixes=HANDLER) & filters.user(OWNER_ID))
async def Unapprove_user(_, message):
    is_pm_block_enabled = await GET_PM_GUARD()
    approved_users = await GET_APPROVED_USERS()
    if is_pm_block_enabled:
        if message.chat.type == enums.ChatType.SUPERGROUP:
            await message.reply("➲ This Command Only Works On Private Chats ❌.")
            return
        user_id = message.chat.id
        if user_id not in approved_users:
            await message.reply("**➲ This user is Not Approved yet ❌.**")
            return
        try:
            await REMOVE_APPROVED_USER(user_id)
            await message.reply("➲ Successfully Unapproved ✨🗿.")
        except Exception as e:
            await message.reply(f"Sorry, i got a error while unapproving this user\n\n{e}")
    else:
        if message.chat.type == enums.ChatType.SUPERGROUP:
            return
        await message.reply('**➲ PmGuard Not Enabled ❌.**')
            

        
@RAUSHAN.on_message(filters.command(['cw', 'clearwarn'], prefixes=HANDLER) & filters.user(OWNER_ID))
async def clear_warn(_, message):
    global warning_count
    is_pm_block_enabled = await GET_PM_GUARD()
    if is_pm_block_enabled:
        if message.chat.type == enums.ChatType.SUPERGROUP:
            await message.reply("➲ This Command Only Works On Private Chats ❌.")
            return
        user_id = message.chat.id
        try:
            user_id = message.chat.id
            warning_count[user_id] = 0
            await message.reply("➲ Successfully Cleared All Warnings 🗿🔥.")
        except Exception as e:
            await message.reply(f"Sorry, i got a error while Clearing Warns for this user\n\n{e}")
    else:
        if message.chat.type == enums.ChatType.SUPERGROUP:
            return
        await message.reply('**➲ PmGuard Not Enabled ❌.**')
                
@RAUSHAN.on_message(filters.command(['setmsglimit', 'setpmlimit'], prefixes=HANDLER) & filters.user(OWNER_ID))
async def set_limit(_, message):
    if len(message.command) < 2:
        return await message.reply_text("➲ Please enter the maximum message warning limit.")
    count = " ".join(message.command[1:])
    intCount = int(count)
    if intCount == 1:
        await message.reply("➲ Count must be atleast 2.")
        return
    if intCount <= 0:
        await message.reply("➲ Count must be positive Integers.")
        return
    if intCount > 20:
        await message.reply("➲ Maximum Applable warning count is 20.")
        return
    await SET_DEFAULT_MESSAGE_LIMIT(intCount)
    await message.reply(f"**➲ Successfuly set default Warning limit! 🥀 ✨**")

@RAUSHAN.on_message(filters.command(["ausers", "achats"], prefixes=HANDLER) & filters.user(OWNER_ID))
async def get_approved_users(_, message):
    MSG = await message.reply("`Processing...`")
    NAMES = []
    FORMATTED_NAMES = ""
    async for dialog in RAUSHAN.get_dialogs():
        if dialog.chat.type == enums.ChatType.PRIVATE:
            if dialog.chat.id in await GET_APPROVED_USERS():
                GET_CHAT = await RAUSHAN.get_chat(dialog.chat.id)
                First_name = GET_CHAT.first_name
                NAMES.append(First_name)
    for name in NAMES:
        FORMATTED_NAMES += f"-» `{name}`\n"
    await MSG.edit(f"**Results:**\n{FORMATTED_NAMES}")
# END
