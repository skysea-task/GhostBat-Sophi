""" from RAUSHAN import HANDLER
from RAUSHAN.__main__ import RAUSHAN, RAUSHANBot
from config import OWNER_ID
from config import SUDO_USERS_ID
from pyrogram import filters
import asyncio
import os

@RAUSHAN.on_message(filters.command("help", prefixes=HANDLER) & filters.user(OWNER_ID))
async def help(_, message):
  results = await RAUSHAN.get_inline_bot_results(RAUSHANBot.me.username, 'help')
  await RAUSHAN.send_inline_bot_result(
    chat_id=message.chat.id,
    query_id=results.query_id,
    result_id=results.results[0].id
  )
    
