from pyrogram import filters
from config import OWNER_ID, SUDO_USERS_ID
from RAUSHAN import HANDLER
from RAUSHAN.__main__ import RAUSHAN


@RAUSHAN.on_message(filters.command(["cinfo", "channelinfo"], prefixes=HANDLER) & filters.user(OWNER_ID))
async def cinfo(_, m):
    reply = m.reply_to_message
    if not reply:
        await m.reply_text("yoo! baka reply to channel")
        return
    if not reply.sender_chat:
        await m.reply_text("yoo! baka reply to channel")
        return
    if reply.sender_chat:
        message = await m.reply_text("information gathering!!!")
        id = reply.sender_chat.id
        reply.sender_chat.type
        name = reply.sender_chat.title
        username = reply.sender_chat.username
        pfp = reply.sender_chat.photo
    if not pfp:
        text = f"✪ **TYPE:** Channel\n\n"
        text += f"✪ **ID:** {id}\n\n"
        text += f"✪ **NAME:** {name}\n\n"
        text += f"✪ **USERNAME:** @{username}\n\n"
        text += f"✪ **MENTION:** [link](t.me/{username})"
        await m.reply_text(text)
        await message.delete()
        return
    image = reply.sender_chat.photo
    if image:
        photo = await RAUSHAN.download_media(image.big_file_id)
        text = f"✪ **TYPE:** Channel\n\n"
        text += f"✪ **ID:** {id}\n\n"
        text += f"✪ **NAME:** {name}\n\n"
        text += f"✪ **USERNAME:** @{username}\n\n"
        text += f"✪ **MENTION:** [link](t.me/{username})"
        await m.reply_photo(photo=photo, caption=(text))
        await message.delete()


no_reply_user = """╒═══「 Appraisal results:」

**ɪᴅ**: `{}`
**ᴅᴄ**: `{}`
**ғᴜʟʟ ɴᴀᴍᴇ**: {}
**ᴜsᴇʀɴᴀᴍᴇ**: @{}
**ᴘᴇʀᴍᴀʟɪɴᴋ**: {}
**ᴜsᴇʀʙɪᴏ**: `{}`
**sᴜᴅᴏ ᴜsᴇʀ**: `{}`

**Powered by: @HeartBeat_Muzic & @HeartBeat_Offi **
"""


@RAUSHAN.on_message(filters.command("info", prefixes=HANDLER) & filters.user(OWNER_ID))
async def info(_, m):
    message = m
    reply = m.reply_to_message
    if len(m.command) < 2 and not reply:
        return await m.reply_text("ℹ️ Please reply to a user or enter their id 🆔!")
    elif not len(m.command) < 2:
        id_user = " ".join(message.command[1:]).replace('https://t.me/', '').replace('http://t.me/', '').replace('t.me/', '').replace('https://telegram.dog', '').replace('http://telegram.dog', '').replace('telegram.dog/', '')
    else:
        id_user = m.reply_to_message.from_user.id
    msg = await m.reply_text("`Processing...`")
    try: info = await RAUSHAN.get_chat(id_user)
    except:
        await msg.delete()
        return await message.reply("🚫 Cannot find chat/user, make sure you entered correct id/username.")
    if info.photo:
        file_id = info.photo.big_file_id
        photo = await RAUSHAN.download_media(file_id)
        user_id = info.id
        if not info.last_name: User_Name = info.first_name or info.title
        else: User_Name = f"{info.first_name} {info.last_name}"
        if info.id in SUDO_USERS_ID: sudo_stats = True
        else: sudo_stats = False
        first_name = User_Name
        username = info.username
        user_bio = info.bio or info.description[:40]
        dc_id = info.dc_id
        user_link = f"[Link](tg://user?id={user_id})" if not str(user_id).startswith('-') else f"[Link](https://t.me/{username})"
        is_sudo = sudo_stats
        await m.reply_photo(
            photo=photo,
            caption=no_reply_user.format(
                user_id, dc_id, first_name, username, user_link, user_bio, is_sudo
            ),
        )
    elif not info.photo:
        user_id = info.id
        if info.last_name == None:
            User_Name = info.first_name or info.title
        else:
            User_Name = f"{info.first_name} {info.last_name}"
        if info.id in SUDO_USERS_ID:
            sudo_stats = True
        else:
            sudo_stats = False
        full_name = User_Name
        username = info.username
        user_bio = info.bio or info.description[:40]
        dc_id = info.dc_id
        user_link = f"[Link](tg://user?id={user_id})" if not str(user_id).startswith('-') else f"[Link](https://t.me/{username})"
        is_sudo = sudo_stats
        await m.reply_text(
            text=no_reply_user.format(
                user_id, dc_id, full_name, username, user_link, user_bio, is_sudo
            )
        )
    await msg.delete()
      
MOD_NAME = 'Info'
MOD_HELP = ".info (user_id or reply) - To get information of that user\n.cinfo (reply) - Reply to a channel to get it's info"
