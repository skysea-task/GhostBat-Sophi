import io
from pyrogram import *
from RAUSHAN.__main__ import RAUSHAN as bot
from RAUSHAN import HANDLER
from config import OWNER_ID
from config import SUDO_USERS_ID
import traceback
from subprocess import getoutput as run
from pyrogram.enums import ChatAction

@bot.on_message(filters.command(["logs", "log"], prefixes=HANDLER))
async def logs(_, message):
    if message.from_user.id == OWNER_ID or message.from_user.id in SUDO_USERS_ID:
        print("")
    else:
        return
    run_logs = run("tail log.txt")
    text = await message.reply_text("`Getting logs...`")
    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    await message.reply_text(f"```shell\n{run_logs}```")
    await text.delete()


@bot.on_message(filters.command(["flogs", "flog"], prefixes=HANDLER))
async def logs(_, message):
    if message.from_user.id == OWNER_ID or message.from_user.id in SUDO_USERS_ID:
        print("")
    else:
        return
    run_logs = run("cat log.txt")
    text = await message.reply_text("`Sending Full logs...`")
    await bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_DOCUMENT)
    with io.BytesIO(str.encode(run_logs)) as logs:
        logs.name = "log.txt"
        await message.reply_document(
            document=logs,
        )
    await text.delete()
