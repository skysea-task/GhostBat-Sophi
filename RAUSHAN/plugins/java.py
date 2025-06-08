""" from RAUSHAN import HANDLER
from RAUSHAN import RAUSHAN
from pyrogram import filters
from subprocess import getoutput as run
import asyncio
import os
import io

@RAUSHAN.on_message(filters.command(["java", "je"], prefixes=HANDLER) & filters.user('me'))
async def run_java(_, message):
    if len(message.command) < 2:
        return await message.edit("Please enter a Java command to run! 🥀 ✨")
    
    java_code = message.text.split(None, 1)[1]
    await message.edit(f"```java\n{java_code}```")
    message_text = await message.reply_text("Processing...")
    with open("MyProgram.java", "w") as java_file:
        java_file.write(java_code)
    compile_output = run("javac MyProgram.java")
    if compile_output:
        if len(compile_output) > 3900:
            with io.BytesIO(str.encode(compile_output)) as out_file:
                out_file.name = "error_output.txt"
                await message.reply_document(
                    document=out_file, disable_notification=True
                )
                await message_text.delete()
                return
        else:
            return await message_text.edit(f"```Error\n{compile_output}```")
    output = run("java MyProgram")
    os.remove("MyProgram.java")
    os.remove("MyProgram.class")
    if len(output) > 3900:
        with io.BytesIO(str.encode(output)) as out_file:
            out_file.name = "java_output.txt"
            await message.reply_document(
                document=out_file, disable_notification=True
            )
            await message_text.delete()
    else:
        await message_text.edit(f"```Output\n{output}```")
