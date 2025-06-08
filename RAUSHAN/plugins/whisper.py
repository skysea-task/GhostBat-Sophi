from RAUSHAN import HANDLER, RAUSHANBot, RAUSHAN, qfilter
from pyrogram import *
import logging
from pyrogram.types import *
from config import OWNER_ID
import traceback
from RAUSHAN.database.whisper import whisper

whs = whisper()

@RAUSHAN.on_message(filters.command("whisper", prefixes=HANDLER) & filters.user(OWNER_ID) & ~filters.private & ~filters.bot)
async def whisper(_, message):
  await message.delete()
  if len(message.text.split()) < 2:
    return await message.reply("Please enter a text to whisper!")
  if not message.reply_to_message:
    return await message.reply("Please reply to someone to whisper!")
  reply = message.reply_to_message
  name = f"{reply.from_user.first_name} {reply.from_user.last_name or ''}".strip()
  data = f"name: {name}\nid: {reply.from_user.id}\nmessage: {message.text.split(None, 1)[1]}\nusername: {reply.from_user.username or 'Nothing'}"
  results = await RAUSHAN.get_inline_bot_results(RAUSHANBot.me.username, f"whisper: {data}")
  if results.results:
    await RAUSHAN.send_inline_bot_result(
      chat_id=message.chat.id,
      query_id=results.query_id,
      result_id=results.results[0].id
    )
  else:
    await message.reply("Error: No result returned by the inline bot, Make sure you have turned on inline in your bot-settings.")

@RAUSHANBot.on_inline_query(qfilter("whisper: "))
async def send_whisper(_, query):
  try:
    data = query.query.replace("whisper: ", "")
    data_lines = data.split("\n")
    data_dict = {line.split(":", 1)[0].strip(): line.split(":", 1)[1].strip() for line in data_lines}
    wid = await whs.add(data_dict['message'], int(data_dict['id']))
    mention = f"tg://user?id={data_dict['id']}"
    to_user = f"**🦋 To:** @{data_dict['username']}" if data_dict['username'] != "Nothing" else ""
    result = InlineQueryResultArticle(
      title="Whisper message",
      input_message_content=InputTextMessageContent(
        f"🔒 A whisper message to [{data_dict['name']}]({mention}), only they can open it.\n\n{to_user}\n**👾 By:**𝐇𝐞𝐚𝐫𝐭𝐁𝐞𝐚𝐭-✗-𝐁𝐨𝐭",
        parse_mode=enums.ParseMode.MARKDOWN,
        disable_web_page_preview=True
      ),
      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("View 🔓", callback_data=f"wh: {wid}")]])
    )
    await query.answer([result])
  except:
    e = traceback.format_exc()
    logging.error(e)

@RAUSHANBot.on_callback_query(qfilter("wh: "))
async def show_whisper(_, query):
  try:
    wid = int(query.data.replace("wh: ", ""))
    data = await whs.get(wid)
    if data and (query.from_user.id == data['id'] or query.from_user.id == OWNER_ID):
      await query.answer(data['message'], show_alert=True)
    else:
      await query.answer("This message is not for you.", show_alert=False)
  except:
    e = traceback.format_exc()
    logging.error(e)

MOD_NAME = "Whisper"
MOD_HELP = ".whisper <text & reply> - To send a message privately!"
