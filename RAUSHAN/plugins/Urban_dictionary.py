from RAUSHAN import HANDLER
from RAUSHAN.__main__ import RAUSHAN as RAUSHAN
from config import OWNER_ID
from pyrogram import filters
import asyncio
import os
import requests

@RAUSHAN.on_message(filters.command("ud", prefixes=HANDLER) & filters.user(OWNER_ID))
async def urban_dictionary(_, message):
  if len(message.command) < 2:
    return await message.reply("Please give an input of a word.\nExample: `.ud asap`")         
  text = message.text.split(None, 1)[1]
  try:
    results = requests.get(
      f'https://api.urbandictionary.com/v0/define?term={text}').json()
    reply_text = f"""

    """
**Results for**: {text}

**Defination**:
{results["list"][0]["definition"]}\n
**Example:**
{results["list"][0]["example"]}
  
except Exception as e:
    if str(e) == "list index out of range":
      await message.reply("Cannot find your query on Urban dictionary.")
      return
    return await RAUSHAN.send_message(message.chat.id, f"Somthing wrong Happens:\n`{e}`")
  ud = await RAUSHAN.send_message(message.chat.id, "Exploring....")
  await ud.edit_text(reply_text)

MOD_NAME = "UD"
MOD_HELP = ".ud <word> - To get definition of that word!"
