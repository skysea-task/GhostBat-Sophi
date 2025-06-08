""" from RAUSHAN import HANDLER
from RAUSHAN.__main__ import RAUSHAN
from pyrogram import filters
import asyncio
import io
from variables import DEVELOPER_MODE

@RAUSHAN.on_message(filters.command(["sh", "shell", "bash"], prefixes=HANDLER) & filters.user('me'))
async def shell(_, message):
    if not DEVELOPER_MODE:
        return await message.reply("Developer mode isn't enabled turn and try!")
    if len(message.command) < 2:
        return await message.edit("Please enter a command to run! 🥀 ✨")
    
    code = message.text.split(None, 1)[1]
    message_text = await message.reply_text("`Processing...`")
    
    try:
        process = await asyncio.create_subprocess_shell(
            code,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        output = (stdout.decode() + stderr.decode()).strip()
        if not output:
            output = "No output from command."
        if len(output) > 4096:
            with io.BytesIO(str.encode(output)) as out_file:
                out_file.name = "shell.txt"
                await message.reply_document(
                    document=out_file, disable_notification=True
                )
                await message_text.delete()
        else:
            await message_text.edit(f"**Output**:\n`{output}`")
    except Exception as e:
        await message_text.edit(f"**Error**:\n`{str(e)}`")
