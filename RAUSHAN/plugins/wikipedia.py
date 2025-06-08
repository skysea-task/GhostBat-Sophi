from RAUSHAN import HANDLER
from RAUSHAN.__main__ import RAUSHAN
from config import OWNER_ID
from pyrogram import filters
import asyncio
import os
import io
import wikipedia

@RAUSHAN.on_message(filters.command(["wiki", "wikipedia"], prefixes=HANDLER) & filters.user(OWNER_ID))
async def search_wikipedia(_, message):
    if len(message.text.split()) < 2:
        return await message.reply("Please enter a text to search it.")
    MSG = await message.reply("`Loading...`")
    query = " ".join(message.command[1:])
    try:
        results = wikipedia.search(query)
        if not results:
            return await MSG.edit("No results found.")
        summary = wikipedia.summary(results[0])
        if len(summary) > 3700:
            summary = f"Results from Wikipedia for {query}:\n\n{summary}"
            with io.BytesIO(str.encode(summary)) as output:
                output.name = "wikipedia.txt"
                await message.reply_document(
                    document=output
                )
                await MSG.delete()
        else:
            await MSG.edit(f"**Results from Wikipedia for '{query}':**\n\n{summary}")
    except wikipedia.exceptions.DisambiguationError as e:
        await MSG.edit(f"DisambiguationError: {e}")
    except wikipedia.exceptions.PageError as e:
        await MSG.edit(f"PageError: {e}")
    except Exception as e:
        await MSG.edit(f"An error occurred: {e}")

MOD_NAME = "Wikipedia"
MOD_HELP = ".wiki <query> - To search that query in wikipedia."
