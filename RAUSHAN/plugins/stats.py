""" from RAUSHAN import HANDLER
from RAUSHAN import *
from config import OWNER_ID
from pyrogram import filters
import asyncio
import logging
from pyrogram import enums
import os
from datetime import datetime
from pyrogram import *
import asyncio
import traceback
from RAUSHAN.plugins.modules import a, help_names
from RAUSHAN.plugins.ping import ping_website
from pyrogram.types import *
from pyrogram import __version__
from RAUSHAN.plugins.play import is_playing
from RAUSHAN.database.afk import *
from RAUSHAN.database.backup_msg import *
from RAUSHAN.database.pmguard import *

@RAUSHANBot.on_inline_query(filters.regex('IRLYMANOFR'))
async def send_btns(_, query):
  try:
    btns = InlineKeyboardMarkup([
      [
        InlineKeyboardButton("🆕 What is new?", callback_data=f"RAUSHANNew"),
        InlineKeyboardButton("⚙️ Settings", callback_data=f"RAUSHANPageSettigns")
      ],
      [
        InlineKeyboardButton("🗂️ Chat", url=f"https://t.me/HeartBeat_Muzic"),
        InlineKeyboardButton("📖 Help", callback_data=f"helppage:1")
      ],
      [
        InlineKeyboardButton("⚕️ Stats ⚕️", callback_data=f"RAUSHANStats")
      ],
      [
        InlineKeyboardButton("👥 Deploy", url="https://t.me/Ghostt_Batt")
      ]
    ])
    result = InlineQueryResultPhoto(
      photo_url="https://graph.org/file/ffdb1be822436121cf5fd.png",
      caption="""

      """**𝅗ـﮩ٨ـ𝅽𝅾𓆩𝐇𖽞𖽖֯֟፝͢͡𖽸𖾓𝂬𓏲ࣹ᷼𝄢𝂬𝐁𖽞֟֠֯፝͢͡𖽖𖾓𓆪ﮩ٨ـ𝅽𝅾‐𝅘**\n
**__🍃 𝐇𝐞𝐚𝐫𝐭𝐁𝐞𝐚𝐭-✗-𝐁𝐨𝐭 designed 👾 to automate and simplify your Telegram experience 🦋. 🥀 ✨__**

**👇 Explore the Features Below ✅**
      """
      """ ,
      reply_markup=btns
    )
    await query.answer([result])
  except:
    e = traceback.format_exc()
    logging.error(e)

@RAUSHANBot.on_callback_query(filters.regex('RAUSHANStats'))
async def show_stats(_, query):
  start_time = bot_start_time
  end_time = datetime.now()
  ping_time = (end_time - start_time).total_seconds() * 1000
  uptime = (end_time - bot_start_time).total_seconds()
  hours, remainder = divmod(uptime, 3600)
  minutes, seconds = divmod(remainder, 60)
  stats_txt = f"""
  """𝗦𝗼𝗽𝗵𝗶𝗮 𝗦𝘆𝘀𝘁𝗲𝗺\n
Uᴘᴛɪᴍᴇ: {int(hours)}h {int(minutes)}m {int(seconds)}s
Pʏᴛʜᴏɴ: {python_version}
Pʏʀᴏɢʀᴀᴍ: {__version__}
Pɪɴɢ: {ping_website("https://google.com")}
Sᴏɴɢs ᴘʟᴀʏɪɴɢ: {len(is_playing) if is_playing else 0}
Hᴇʟᴘ ᴍᴏᴅᴜʟᴇs: {len(help_names)}/{len(a)}
Mʏ ᴠᴇʀsɪᴏɴ: {MY_VERSION}
Rᴇʟᴇᴀsᴇ ᴛʏᴘᴇ: {release_type}
Aғᴋ: {await GET_AFK()}
Pᴍɢᴜᴀʀᴅ: {await GET_PM_GUARD()}
  """
"""  await query.answer(stats_txt, show_alert=True)

@RAUSHANBot.on_callback_query(filters.regex('RAUSHANNew'))
async def show_newUpdates(_, query):
  await query.answer(what_is_new, show_alert=True)

@RAUSHANBot.on_callback_query(filters.regex('RAUSHANPageSettigns'))
async def show_settings(_, query):
  if query.from_user.id != OWNER_ID:
        return await query.answer('This is not for you!', show_alert=False)
  await query.answer("Coming soon", show_alert=False)

@RAUSHAN.on_message(filters.command(["hbs", "stats"], prefixes=HANDLER) & filters.user(OWNER_ID))
async def send_stats(_, message):
    results = await RAUSHAN.get_inline_bot_results(RAUSHANBot.me.username, 'IRLYMANOFR')
    await RAUSHAN.send_inline_bot_result(
        chat_id=message.chat.id,
        query_id=results.query_id,
        result_id=results.results[0].id
    )


MOD_NAME = 'HeartBeat'
MOD_HELP = ".hbs | .stats - To get info of userbot & change settings of userbot."
