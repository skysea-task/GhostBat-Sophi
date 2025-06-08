from config import *
from RAUSHAN import *
from pyrogram import *
from pyrogram.types import *
import traceback 

@RAUSHANBot.on_inline_query(filters.regex('RAUSHANReportBug'))
async def send_reportBug(_, query):
  try:
    btn = InlineKeyboardMarkup([[InlineKeyboardButton("🪲 Report a bug", url="t.me/futurecity005")]])
    result = InlineQueryResultArticle(
      title="Report bug",
      input_message_content=InputTextMessageContent(
        f"Click the button below to report bug 🪲"
      ),
      reply_markup=btn
    )
    await query.answer([result])
  except:
    e = traceback.format_exc()
    logging.error(e)

@RAUSHAN.on_message(filters.command("bug", prefixes=HANDLER) & filters.user(OWNER_ID))
async def send_rbug(_, message):
    results = await RAUSHAN.get_inline_bot_results(RAUSHANBot.me.username, 'RAUSHANReportBug')
    await RAUSHAN.send_inline_bot_result(
        chat_id=message.chat.id,
        query_id=results.query_id,
        result_id=results.results[0].id
    )

MOD_NAME = 'Bug'
MOD_HELP = ".bug - To report a bug to creator."
