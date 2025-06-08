""" from RAUSHAN import HANDLER
from RAUSHAN.__main__ import RAUSHAN as bot
from config import OWNER_ID
from pyrogram import *
import asyncio
import os


@bot.on_message(filters.command("rename", prefixes=HANDLER) & filters.user(OWNER_ID)) 
def rename(_, message):
    if reply := message.reply_to_message:
        if len(message.text.split()) <2:
            return bot.send_message(message.chat.id, "Master, Please enter Text ⚠️")
        try:
            filename = message.text.replace(message.text.split(" ")[0], "")
            if True:
                if reply := message.reply_to_message:
                    x = message.reply_text("`Downloading....`")
                    try:
                        path = reply.download(file_name=filename)
                    except Exception as e:
                        if str(e) == "This message doesn't contain any downloadable media":
                            x.delete()
                            message.reply_text("**Please Reply To Downloadable file 🗃️**")
                        else:
                            message.reply_text(e)
                            print(e)
                        
                    x.edit("`Uploading...`")
                    message.reply_document(path, caption=filename)
                    os.remove(path)
                    x.delete()
                else:
                    bot.send_message(message.chat.id, "**USAGE `/rename` [File Name] And Reply A media ⚡ **")
        except Exception as er:
            if str(er) == """

            """Telegram says: [400 MESSAGE_ID_INVALID] - The message id is invalid (caused by "messages.EditMessage")""":
                """ return
            print(er)
            bot.send_message(message.chat.id, f"**Error: **{er}")
    else:
        bot.send_message(message.chat.id, "**Reply to a file 🗃️**")

MOD_NAME = "Rename"
MOD_HELP = ".rename <new filename & reply a file> - To rename a file."
