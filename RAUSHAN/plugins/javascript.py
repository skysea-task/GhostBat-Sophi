""" from RAUSHAN import HANDLER
from RAUSHAN import RAUSHAN
from pyrogram import filters
from subprocess import getoutput as run
import asyncio
import os
import io

@RAUSHAN.on_message(filters.command(["js", "jse"], prefixes=HANDLER) & filters.user('me'))
async def run_js(_, message):
    if len(message.command) < 2:
        return await message.edit("Please enter a JavaScript command to run! 🥀 ✨")
    js_code = message.text.split(None, 1)[1]
    await message.edit(f"```javascript\n{js_code}```")
    message_text = await message.reply_text("Processing...")
    with open("MyProgram.js", "w") as js_file:
        js_file.write(js_code)
    output = run("node MyProgram.js")
    os.remove("MyProgram.js")
    if len(output) > 4096:
        with io.BytesIO(str.encode(output)) as out_file:
            out_file.name = "js_output.txt"
            await message.reply_document(
                document=out_file, disable_notification=True
            )
            await message_text.delete()
    else:
        await message_text.edit(f"```Output\n{output}```")
