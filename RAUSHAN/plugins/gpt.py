import aiohttp
from pyrogram import filters, Client
from pyrogram.types import Message
from RAUSHAN.__main__ import RAUSHAN as app
from config import OWNER_ID
from RAUSHAN import HANDLER, MY_VERSION
from datetime import datetime
import json

async def fetch_data(query: str, message: Message) -> str:
    try:
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json"
        }
        url = "https://api.binjie.fun/api/generateStream"
        data = {
            "prompt": query,
            "userId": f"#/chat/{message.from_user.id}",
            "network": True,
            "stream": False,
            "system": {
                "userId": "#/chat/1722576084617",
                "withoutContext": False
            }
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                return await response.text()
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.on_message(filters.command(["chat", "gpt"], prefixes=HANDLER) & filters.user(OWNER_ID))
async def chatgpt(_: Client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("Please provide a query.")
    query = " ".join(message.command[1:]) or '?'
    mquery = False
    if message.reply_to_message:
        rname = message.reply_to_message.from_user.first_name
        is_bot = message.reply_to_message.from_user.is_bot
        urname = message.from_user.first_name
        urid = message.from_user.id
        rid = message.reply_to_message.from_user.id
        if message.reply_to_message.text:
            mquery = f"The replied message you see is the user replied msg he asking something about that thing so you should act like he asking about that reply to you if he doesn't ask about that reply you shouldnt talk about that\n\n\nuser replied msg: {message.reply_to_message.text}\n\nUser message: {query}"
            if message.reply_to_message.reply_to_message and message.reply_to_message.reply_to_message.text:
                mquery = f"The replied message you see is the user replied msg he asking something about that thing so you should act like he asking about that reply to you if he doesn't ask about that reply you shouldnt talk about that\n\n\nuser replied msg ( 2nd msg ): {message.reply_to_message.text}\n\n User replied message replied msg ( 1st msg ): {message.reply_to_message.reply_to_message.text}\n\n User message ( 3rd latest msg ): {query}"
            mquery += f"\n\nADDITIONAL INFORMATION:\n Reply user name: {rname}\n is replied user is bot: {is_bot} ( if he asked replied user is bot or not you should answer by this if its false its not bot its true it is bot )\n Replied user telegram id {rid} \n Sender name: {urname}\nSender tg userid: {urid}\n if sender telegram userid is 5965055071 he is your owner you should respect him his name Otazuki\n\n This user using userbot to use you in telegram\n\n\n YOU SHOULD NOT USE FONTS IT DOESN'T WORK ON TELEGRAM.\n\n The userbot you are bot you are in name is RAUSHAN if they asked you should tell if they asked how to use this userbot you should give this link http://graph.org/RAUSHAN-Commands-01-30 this have all RAUSHAN bot commands and RAUSHAN was created by t.me/Hyper_speed0 and t.me/Otazuki\n Your version is 1 your version 1 release date is dec 12 2024, YOU ARE NOT BOT YOU ARE USERBOT, Time: ( {datetime.now()} ) if user asked time convert this into ist Time UTC +5:30 and tell them what time is now and don't say 'converted to IST ' like that just convert and just say what the asked like if i asked time say 1am 2pm 1:12am jan 12 2024 if asked, Repo of RAUSHAN: https://Github.com/Otazuki004/RAUSHANUB"
    else:
        urname = message.from_user.first_name
        urid = message.from_user.id
        query += f"\n\n\nThis message from code not from user: EXTRA INFO ABOUT USER: \n his name {urname} \n his telegram user id: {urid} \n  if sender telegram userid is 5965055071 he is your owner you should respect him his name Otazuki\n\n This user using userbot to use you in telegram\n\n\n YOU SHOULD NOT USE FONTS IT DOESN'T WORK ON TELEGRAM.\n\n The userbot you are bot you are in name is RAUSHAN if they asked you should tell if they asked how to use this userbot you should give this link http://graph.org/RAUSHAN-Commands-01-30 this have all RAUSHAN bot commands and RAUSHAN was created by t.me/Hyper_speed0 and t.me/Otazuki\n Your version is {MY_VERSION} YOU ARE NOT BOT YOU ARE USERBOT, Time: ( {datetime.now()} ) if user asked time convert this into ist Time UTC +5:30 and tell them what time is now and don't say 'converted to IST ' like that just convert and just say what the asked like if i asked time say 1am 2pm 1:12am jan 12 2024 if asked, Repo of RAUSHAN: https://Github.com/Otazuki004/RAUSHANUB"
    txt = await message.reply_text("`Processing...`")
    if mquery:
        api_response = await fetch_data(mquery, message)
    else:
        api_response = await fetch_data(query, message)
    await txt.edit(api_response)

MOD_NAME = 'Gpt'
MOD_HELP = ".gpt <query> - To ask the query to gpt"
