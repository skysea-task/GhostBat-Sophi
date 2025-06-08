from RAUSHAN import *
from pyrogram import *
from RAUSHAN.database.afk import *
from RAUSHAN.database.ignore_users import *
from RAUSHAN.database.backup_msg import *
from RAUSHAN.database.pmguard import *
from pyrogram.enums import *
from config import OWNER_ID
from datetime import datetime
import os
import re
import asyncio
import logging
import traceback

def calculate_time(start_time, end_time):
    ping_time = (end_time - start_time).total_seconds() * 1000
    uptime = (end_time - start_time).total_seconds()
    hours, remainder = divmod(uptime, 3600)
    minutes, seconds = divmod(remainder, 60)
    time = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    return time

warning_count = {}

async def filter_(_, client, update):
    message = update
    if message.chat.type == ChatType.PRIVATE and await GET_BACKUP() and update.chat.id not in await GET_STOP_BACKUP_CHATS() and update.chat.id != OWNER_ID:  # Backup section
        command = False
        if update.from_user.id == OWNER_ID and update.text and update.text.startswith(tuple(HANDLER)) and not len(update.text) < 2:
            command = True
        if not command:
            CHATS = await GET_BACKUP_CHATS()
            if update.chat.id in CHATS and await GET_BACKUP_CHANNEL_ID(update.chat.id) != 0:
                chat_id = await GET_BACKUP_CHANNEL_ID(update.chat.id)
                try:
                    if message.chat.type == ChatType.PRIVATE:
                        await RAUSHAN.forward_messages(chat_id, message.chat.id, message.id)
                except Exception as e:
                    if str(e).startswith(tuple([
                        "Telegram says: [400 CHAT_FORWARDS_RESTRICTED", 
                        "Telegram says: [400 MESSAGE_ID_INVALID]"
                    ])): pass
                    elif 'CHANNEL_INVALID' in str(e):
                        try:
                            c_name = f"{message.chat.first_name} BACKUP"
                            if message.chat.username:
                                chat = await RAUSHAN.create_channel(f"{c_name}", f"Username: @{message.chat.username}\n\n~ @Hyper_Speed0")
                                await RAUSHAN.archive_chats(chat.id)
                            else:
                                chat = await RAUSHAN.create_channel(f"{c_name}", "~ @Hyper_Speed0")
                                await RAUSHAN.archive_chats(chat.id)
                            await ADD_BACKUP_CHAT(message.chat.id)
                            await SET_BACKUP_CHANNEL_ID(message.chat.id, chat.id)
                            await RAUSHAN.forward_messages(chat.id, message.chat.id, message.id)
                        except:
                            t = traceback.format_exc()
                            logging.error(t)
                    else:
                        t = traceback.format_exc()
                        logging.error(f"Line 61 message_handler.py: {t}")
            else:
                try:
                    c_name = f"{message.chat.first_name} BACKUP"
                    if message.chat.username:
                        chat = await RAUSHAN.create_channel(f"{c_name}", f"Username: @{message.chat.username}\n\n~ @Hyper_Speed0")
                        await RAUSHAN.archive_chats(chat.id)
                    else:
                        chat = await RAUSHAN.create_channel(f"{c_name}", "~ @HeartBeat_Muzic")
                        await RAUSHAN.archive_chats(chat.id)
                    await ADD_BACKUP_CHAT(message.chat.id)
                    await SET_BACKUP_CHANNEL_ID(message.chat.id, chat.id)
                    await RAUSHAN.forward_messages(chat.id, message.chat.id, message.id)
                except:
                    t = traceback.format_exc()
                    logging.error(t)

    if await GET_PM_GUARD() and update.chat.id not in (await GET_APPROVED_USERS()) and message.chat.type == ChatType.PRIVATE and message.from_user.id != OWNER_ID:
        user_id = message.chat.id
        global warning_count
        maximum_message_count = await GET_WARNING_COUNT()
        if user_id not in warning_count:
            warning_count[user_id] = 0
        warning_count[user_id] += 1
        if warning_count[user_id] < maximum_message_count:
            await message.reply(f"**⚠️ WARNING**\n\nSorry, my master has enabled the PmGuard feature. You can't send messages until my master approves you or disables this feature. If you Spam Here or the warning exceeds the limits I will Block You.\n\n**➲ Warning Counts** `{warning_count[user_id]}/{maximum_message_count}`")
        elif warning_count[user_id] >= maximum_message_count:
            try:
                await message.reply("➲ You have exceeded your limits, so I have blocked you!")
                await RAUSHAN.block_user(user_id)
            except Exception as e:
                print(e)
                await RAUSHAN.send_message(OWNER_ID, f"Error in blocking user: {str(e)}")

    if await GET_AFK():
        if message.chat.type == ChatType.PRIVATE or message.reply_to_message.from_user.id == OWNER_ID:
            try:
                afk_time = await GET_AFK_TIME()
                formatted_time = calculate_time(afk_time, datetime.now())
                reason = await GET_AFK_REASON()
                if reason is None:
                    await message.reply_text(f"**⚠️ OFFLINE WARNING ⚠️**\n\nSorry, My master is Currently Offline, You can't chat with my master currently now. and don't spam here because he/she may be in a highly stressed situation, working, or facing a problem. Please do not disturb him/her now.\n\n**➲ Reason: NOT SET\n➲ Offline Duration:** {formatted_time}")
                else:
                    await message.reply_text(f"**⚠️ OFFLINE WARNING ⚠️**\n\nSorry, My master is Currently Offline, You can't chat with my master currently now. and don't spam here because he/she may be in a highly stressed situation, working, or facing a problem. Please do not disturb him/her now.\n\n**➲ Reason: `{reason}`\n➲ Offline Duration:** {formatted_time}")
                    await RAUSHAN.mark_chat_unread(message.chat.id)
            except Exception as e:
                print(e)
                await RAUSHAN.send_message(OWNER_ID, f"Error in AFK handling: {str(e)}")
    return False

@RAUSHAN.on_message(filters.create(filter_) & ~filters.bot & ~filters.service)
async def message_handle(_, message):
    # This function never triggered lol
    print("Join @HeartBeat_Muzic")
