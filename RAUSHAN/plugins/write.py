""" from pyrogram import filters
from config import SUDO_USERS_ID
from config import OWNER_ID
from RAUSHAN import HANDLER
from RAUSHAN.__main__ import RAUSHAN


@RAUSHAN.on_message(filters.command("write", prefixes=HANDLER) & filters.user('me'))
async def write(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Pʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛᴇxᴛ. ✨")
    m = await message.reply_text("Wʀɪᴛɪɴɢ...")
    name = (
        message.text.split(None, 1)[1]
        if len(message.command) < 3
        else message.text.split(None, 1)[1].replace(" ", "%20")
    )
    hand = "https://apis.xditya.me/write?text=" + name
    await m.edit("Uᴘʟᴏᴀᴅɪɴɢ...")
    await message.reply_photo(hand, caption="**Cᴀɴ ʏᴏᴜ ᴊᴏɪɴ ʜᴇʀᴇ?:** @HeartBeat_Muzic")
    await m.delete()
  
MOD_NAME = 'Write'
MOD_HELP = ".write (text) - To get that text in notebook page."
