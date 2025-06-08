import io
import json
import sys
import traceback
from RAUSHAN import *
from config import SUDO_USERS_ID
from RAUSHAN.__main__ import RAUSHAN
from config import OWNER_ID
from pyrogram import filters
import asyncio
from datetime import datetime
import os
from pyrogram import enums
from subprocess import getoutput as run
from pytgcalls import *
from pytgcalls.types import *
import logging
from variables import DEVELOPER_MODE
from RAUSHAN.helpers.ask import *

app = RAUSHAN
Client = RAUSHAN
bot = RAUSHAN
r = run
ldb = DATABASE['manokvp143']
mdb = DATABASE['messages']

def p(text):
    print(text)

@RAUSHAN.on_message(filters.command(["eval", "e", "python"], prefixes=HANDLER) & filters.user("me"))
async def eval(client, message):
    if not DEVELOPER_MODE:
        return await message.reply("Developer mode isn't enabled turn and try!")
    m = message
    chat_id = m.chat.id
    m_reply = m.reply_to_message
    if len(message.command) < 2:
        return await message.reply_text("Master, Please Enter code to run it!. ✨ 🥀")
    status_message = await message.reply_text("`Processing...`")
    cmd = message.text.split(None, 1)[1]
    reply_to_ = message
    if message.reply_to_message:
        reply_to_ = message.reply_to_message

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = "INPUT: "
    final_output += f"{cmd}\n\n"
    final_output += "OUTPUT:\n"
    final_output += f"{evaluation.strip()} \n"
    output_code = f"""```python\n{evaluation.strip()}```"""

    if len(output_code) > 3500:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.txt"
            await reply_to_.reply_document(
                document=out_file, disable_notification=True
            )
    else:
        await reply_to_.reply_text(output_code)
    await status_message.delete()


async def aexec(code, client, message):
    m, ctx, r, from_user = message, message, message.reply_to_message, message.from_user
    exec(
        "async def __run_code_otazuki_RAUSHAN(client, message, m, ctx, r, from_user): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__run_code_otazuki_RAUSHAN"](client, message, m, ctx, r, from_user)
