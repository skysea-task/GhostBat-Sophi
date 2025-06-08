""" from RAUSHAN import HANDLER, RAUSHAN
from pyrogram import filters
from subprocess import getoutput as run
import os
import io

@RAUSHAN.on_message(filters.document & filters.user('me'))
async def translate_java(_, message):
    document = message.document
    if not document.file_name.endswith(".class"):
        return
    message_text = await message.reply_text("Processing...")
    class_file_path = await message.download()
    if not os.path.exists("cfr.jar"):
        download_output = run("wget https://www.benf.org/other/cfr/cfr-0.152.jar -O cfr.jar")
        if "error" in download_output.lower():
            return await message_text.edit(f"Error downloading cfr.jar: {download_output}")
    reverse_output = run(f"java -jar cfr.jar {class_file_path}")
    if "error" in reverse_output.lower():
        return await message_text.edit(f"Error during bytecode reversal: {reverse_output}")
    java_file_path = "MyProgram.java"
    with open(java_file_path, "w") as java_file:
        java_file.write(reverse_output)
    with open(java_file_path, "r") as java_file:
        java_code = java_file.read()
    os.remove(java_file_path)
    try:
        os.remove(class_file_path)
    except FileNotFoundError:
        pass
    java_code = java_code.replace("/*\n * Decompiled with CFR 0.152.\n */\n", f"// This code may not work properly!\n")
    if len(java_code) > 4096:
        with io.BytesIO(str.encode(java_code)) as out_file:
            out_file.name = "java_output.txt"
            await message.reply_document(document=out_file, disable_notification=True)
            await message_text.delete()
    else:
        await message_text.edit(f"```java\n{java_code}```")

MOD_NAME = "ClassConvert"
MOD_HELP = "Send a java .class file to decode it"
