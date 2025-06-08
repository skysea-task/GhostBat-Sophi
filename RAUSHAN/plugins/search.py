""" from RAUSHAN import HANDLER
from RAUSHAN.__main__ import RAUSHAN
from config import OWNER_ID
from pyrogram import filters
import asyncio
import os
from googlesearch import search as g_search

@RAUSHAN.on_message(filters.command("search", prefixes=HANDLER) & filters.user(OWNER_ID))
async def search(_, message):
    if len(message.text.split()) < 2:
        return await message.reply("Master, enter a text to search it.")
    MSG = await message.reply("`Loading...`")
    query = " ".join(message.command[1:])
    links = ""
    numb = 0
    try:
        for j in g_search(query, num=10, stop=10, pause=2):
            numb += 1
            links += f"{numb}. {j}\n"
            await MSG.edit(f"**Results:**\n\n{links}", disable_web_page_preview=True)
    except Exception as e:
        await MSG.edit(f"Error: {e}")
