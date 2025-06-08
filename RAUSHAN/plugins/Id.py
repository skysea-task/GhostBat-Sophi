from pyrogram import filters
from config import OWNER_ID
from RAUSHAN import HANDLER 
from RAUSHAN.__main__ import RAUSHAN


@RAUSHAN.on_message(filters.command("id", prefixes=HANDLER) & filters.user(OWNER_ID))
async def id(_, m):
    reply = m.reply_to_message
    _reply = ""
    if not reply:
        no_reply = f"**Your ID**: `{m.from_user.id}`\n"
        no_reply += f"**Chat ID**: `{m.chat.id}`\n"
        no_reply += f"**Message ID**: `{m.id}`"
        await m.reply_text(text=(no_reply))
    if reply.from_user:
        _reply += f"**Your ID**: `{m.from_user.id}`\n"
        _reply += f"**Replied User ID**: `{reply.from_user.id}`\n"
        _reply += f"**Chat ID**: `{m.chat.id}`\n"
        _reply += f"**Replied Message ID**: `{reply.id}`\n"
    if reply.sender_chat:
        _reply += f"\n**Channel ID**: `{reply.sender_chat.id}`\n"
    if reply.sticker:
        _reply += f"**Sticker ID**: `{reply.sticker.file_id}`"
    elif reply.animation:
        _reply += f"**Animation ID**: `{reply.animation.file_id}`"
    elif reply.document:
        _reply += f"**Document ID**: `{reply.document.file_id}`"
    elif reply.audio:
        _reply += f"**Audio ID**: `{reply.audio.file_id}`"
    elif reply.video:
        _reply += f"**Video ID**: `{reply.video.file_id}`"
    elif reply.photo:
        _reply += f"**Photo ID**: `{reply.photo.file_id}`"
    await reply.reply_text(_reply)
    await m.delete()

MOD_NAME = "ID"
MOD_HELP = ".id - Reply to a user to get their id and Get your id and chat id."
