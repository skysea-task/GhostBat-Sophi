from pyrogram import filters
from RAUSHAN import HANDLER
from RAUSHAN.__main__ import RAUSHAN
from config import OWNER_ID as OWN
from config import BOTS_ALLOWED_TO_WORK_IN_BUSY_COMMANDS
from Restart import restart_program
import os
import re
from datetime import datetime
from RAUSHAN.database.afk import *

async def afk_remove(_, client, update):
    if await GET_AFK():
        Busy_time = await GET_AFK_TIME()
        formatted_elapsed_time = calculate_time(Busy_time, datetime.now())
        await UNSET_AFK()
        await update.reply_text(f"➲ **Hello**, Master Welcome Again ✨🥀.\n➲ **Your Offline Duration**: `{formatted_elapsed_time}`🥺")
        return False

def calculate_time(start_time, end_time):
    ping_time = (end_time - start_time).total_seconds() * 1000
    uptime = (end_time - start_time).total_seconds()
    hours, remainder = divmod(uptime, 3600)
    minutes, seconds = divmod(remainder, 60)
    END = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    return END

@RAUSHAN.on_message(filters.command(["busy", "offline", "afk"], prefixes=HANDLER) & filters.user(OWN))
async def set_afk(_, message):
    Busy_time = datetime.now()
    if len(message.command) < 2:
        await SET_AFK(Busy_time, None)
        await message.reply_text("➲ Successfuly set you in afk!")
    else:
        Reason_Of_Busy = " ".join(message.command[1:])
        await SET_AFK(Busy_time, Reason_Of_Busy)
        await message.reply_text(f"➲ Successfuly set you in afk!")
    
    
@RAUSHAN.on_message(filters.user(OWN) & filters.create(afk_remove))
async def remove_busy_mode(_, message):
    pass

MOD_NAME = 'Afk'
MOD_HELP = ".afk <reason (optional)> - To set you in afk, if anyone dm you they get alert!"
