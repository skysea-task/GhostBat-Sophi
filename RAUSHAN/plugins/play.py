from RAUSHAN import *
from RAUSHAN.__main__ import RAUSHAN as bot
from RAUSHAN import RAUSHANVC
from config import OWNER_ID as OWN
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
import asyncio
import os
import re
import requests
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL
from pytgcalls.types import MediaStream
from RAUSHAN.database.play import *
from pyrogram.types import *

oh = play()
RAUSHAN = bot
async def publicFilter(_, client, message):
    if not message.text.startswith(tuple(HANDLER)): return False
    if message.from_user.id == OWN: return True
    if message.chat.id in await oh.get() and message.text.startswith(("/", ".", "$")): return True
    return False

@bot.on_message(filters.command(["addplay", 'aplay'], prefixes=HANDLER) & filters.user(OWN) & ~filters.private & ~filters.bot)
async def addPlayGroups(_, message):
    chat_id = message.chat.id
    info = await oh.addRemove(chat_id)
    if info == "SUCCESS": await message.reply('Successfully allowed play commands in this chat ✅')
    elif info == 'ALREADY': await message.reply("❌ This chat already have permission to use play commands!")

@bot.on_message(filters.command("rplay", prefixes=HANDLER) & filters.user(OWN) & ~filters.private & ~filters.bot)
async def removePlayGroups(_, message):
    chat_id = message.chat.id
    info = await oh.addRemove(chat_id, addOrRemove='remove')
    if info == "SUCCESS": await message.reply('Successfully removed play commands access in this chat ✅')
    elif info == 'ALREADY': await message.reply("❌ This chat already don't have permission to use play commands!")

@bot.on_message(filters.command("getplay", prefixes=HANDLER) & filters.user(OWN) & ~filters.private & ~filters.bot)
async def getPlayGroups(_, message):
    info = await oh.get()
    a = await message.reply("Searching...")
    txt = ""
    for x in info:
        try:
            d = await RAUSHAN.get_chat(x)
            txt += f"{d.title}{'' if not d.username else f' | @{d.username}'}\n"
        except Exception as e: logging.error(e)
    await a.delete()
    if info and txt: return await message.reply(f"**⚕️ Here are the chats you allowed permission for play:**\n\n{txt}")
    await message.reply('No chats have play commands permission ❌')

is_playing = {}
queue_id = {}

async def make_queue(chat_id):
    global queue_id
    if chat_id in queue_id:
        last_key = queue_id[chat_id][-1] if queue_id[chat_id] else 0
        new_key = last_key + 1
        queue_id[chat_id].append(new_key)
        return new_key
    else:
        queue_id[chat_id] = [1]
        return 1

async def play_filter(_, client, message):
    if len(message.text.split()) < 2:
        if not message.reply_to_message: return True
        if message.reply_to_message.audio or message.reply_to_message.video: pass
        else: return True
    if is_playing.get(message.chat.id) or (queue_id.get(message.chat.id) and len(queue_id[message.chat.id]) != 0):
        msg = await message.reply("Successfully added your query in queue! ✅")
        id = await make_queue(message.chat.id)
        while queue_id[message.chat.id][0] != id:
            if id not in queue_id[message.chat.id]:
                return False
            await asyncio.sleep(0.3)
        try: await msg.delete()
        except: pass
        return True
    else:
        id = await make_queue(message.chat.id)
        if id == 1: return True
            
@bot.on_message(filters.command(["play", "ply"], prefixes=HANDLER) & filters.create(publicFilter) & filters.create(play_filter) & ~filters.private & ~filters.bot)
async def play(_, message):
    global is_playing, queue_id
    try: await RAUSHANVC.start()
    except: pass
    if len(message.text.split()) < 2:
        if message.reply_to_message and message.reply_to_message.audio:
            try:
                m = await message.reply("📥 Downloading...")
                file = message.reply_to_message.audio
                path = await message.reply_to_message.download()
                title = file.title or file.file_name or "Unknown Title"
                dur = file.duration or 0
                await m.delete()
                await message.reply_photo(
                    photo="https://i.imgur.com/9KKPfOA.jpeg",
                    caption=(
                        f"**✅ Started Streaming On VC.**\n\n"
                        f"**🥀 Title:** {title[:20] if len(title) > 20 else title}\n"
                        f"**🐬 Duration:** {dur // 60}:{dur % 60:02d} Mins\n"
                        f"**🦋 Stream Type:** Telegram audio\n"
                        f"**👾 Requested By:** {message.from_user.first_name if not message.from_user.last_name else f'{message.from_user.first_name} {message.from_user.last_name}'}\n"
                        f"**⚕️ Join:** __@HeartBeat_Muzic"
                    )
                )
                is_playing[message.chat.id] = True
                await RAUSHANVC.play(message.chat.id, MediaStream(path))
                await asyncio.sleep(dur + 5)
                os.remove(path)
                await manage_playback(message.chat.id, f'{title} {message.id}', dur)
            except Exception as e:
                if "CHAT_ADMIN_REQUIRED" in str(e):
                    await message.reply('**Cannot play song admin rights required ❌**')
                else:
                    logging.error(e)
                    await message.reply(f"Error: {e}")
                chat_id = message.chat.id
                queue_id[chat_id].remove(queue_id.get(chat_id)[0])
                del is_playing[chat_id]
                if not queue_id.get(chat_id):
                    await RAUSHANVC.leave_call(chat_id)
            return
        else: return await message.reply("Provide a song name or link.")
    query = " ".join(message.command[1:])
    m = await message.reply("🔄 Searching....")
    if query.startswith(("www.youtu", "http://youtu", "https://youtu")):
        link = query
        with YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(link, download=False)
            title = info.get("title", "Unknown Title")
            thumbnail = info.get("thumbnail")
            duration = info.get("duration")
    else:
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            link = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]
        except: return await m.edit("⚠️ No results were found.")
    s_title = re.sub(r'[<>:"/\\|?*]', '_', title)
    thumb_name = f"{s_title}.jpg"
    if thumbnail:
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
    await m.edit("📥 Downloading...")
    try:
        ydl_opts = {"format": "bestaudio[ext=m4a]", "cookiefile": "cookies.txt"}
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            audio_file = ydl.prepare_filename(info_dict)
        secmul, dur, dur_arr = 1, 0, str(duration).split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(dur_arr[i]) * secmul
            secmul *= 60
        await m.delete()
        await message.reply_photo(
            photo=thumb_name,
            caption=(
                f"**✅ Started Streaming On VC.**\n\n"
                f"**🥀 Title:** {title[:20] if len(title) > 20 else title}\n"
                f"**🐬 Duration:** {dur // 60}:{dur % 60:02d} Mins\n"
                f"**🦋 Stream Type:** Audio\n"
                f"**👾 Requested By:** {message.from_user.first_name if not message.from_user.last_name else f'{message.from_user.first_name} {message.from_user.last_name}'}\n"
                f"**⚕️ Join:** __@HeartBeat_Muzic"
            )
        )
        is_playing[message.chat.id] = True
        await RAUSHANVC.play(message.chat.id, MediaStream(audio_file))
        await asyncio.sleep(dur + 5)
        await manage_playback(message.chat.id, f'{title} {message.id}', dur)
    except Exception as e:
        if "CHAT_ADMIN_REQUIRED" in str(e):
            await message.reply('**Cannot play song admin rights required ❌**')
        else:
            logging.error(e)
            await message.reply(f"Error: {e}")
        chat_id = message.chat.id
        queue_id[chat_id].remove(queue_id.get(chat_id)[0])
        del is_playing[chat_id]
        if not queue_id.get(chat_id):
            await RAUSHANVC.leave_call(chat_id)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e: logging.error(e)

@bot.on_message(filters.command("vply", prefixes=HANDLER) & filters.create(publicFilter) & filters.create(play_filter) & filters.user(OWN) & ~filters.private & ~filters.bot)
async def vplay(_, message):
    global is_playing, queue_id
    try: await RAUSHANVC.start()
    except: pass
    if len(message.text.split()) < 2:
        if message.reply_to_message and message.reply_to_message.video:
            try:
                m = await message.reply("📥 Downloading...")
                file = message.reply_to_message.video
                path = await message.reply_to_message.download()
                file_name = file.file_name or "Unknown Title"
                title = file_name
                dur = int(file.duration or 0)
                await m.delete()
                await message.reply_photo(
                    photo="https://graph.org/file/ffdb1be822436121cf5fd.png",
                    caption=f"**✅ Started Streaming On VC.**\n\n**🥀 Title:** {title[:20] if len(title) > 20 else title}\n**🐬 Duration:** {dur // 60}:{dur % 60:02d} Mins\n**🦋 Stream Type:** Telegram video\n**👾 Requested By:** {message.from_user.first_name if not message.from_user.last_name else f'{message.from_user.first_name} {message.from_user.last_name}'}\n**⚕️ Join:** @HeartBeat_Muzic"
                )
                is_playing[message.chat.id] = True
                await RAUSHANVC.play(message.chat.id, MediaStream(path))
                await asyncio.sleep(dur + 5)
                os.remove(path)
                await manage_playback(message.chat.id, f'{title} {message.id}', dur)
            except Exception as e:
                if "CHAT_ADMIN_REQUIRED" in str(e):
                    await message.reply('**Cannot play song admin rights required ❌**')
                else:
                    logging.error(e)
                    await message.reply(f"Error: {e}")
                chat_id = message.chat.id
                queue_id[chat_id].remove(queue_id.get(chat_id)[0])
                del is_playing[chat_id]
                if not queue_id.get(chat_id):
                    await RAUSHANVC.leave_call(chat_id)
            return
        else: return await message.reply("Provide a video name or link.")
    query = " ".join(message.command[1:])
    m = await message.reply("🔄 Searching....")
    if query.startswith(("www.youtube", "http://", "https://")):
        link = query
        with YoutubeDL({'quiet': True, 'noplaylist': True}) as ydl:
            info = ydl.extract_info(link, download=False)
            title = info.get("title", "Unknown Title")
            thumbnail = info.get("thumbnail")
            duration = int(info.get("duration", 0))
            is_video = True 
    else:
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            link = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = int(results[0]["duration"].split(":")[0]) * 60 + int(results[0]["duration"].split(":")[1])
            is_video = True
        except: return await m.edit("⚠️ No results were found.")
    s_title = re.sub(r'[<>:"/\\|?*]', '_', title)
    thumb_name = f"{s_title}.jpg"
    if thumbnail:
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
    await m.edit("📥 Downloading...")
    try:
        ydl_opts = {
            "format": "worstvideo[ext=mp4]+bestaudio/best" if is_video else "bestaudio[ext=m4a]",
            "cookiefile": "cookies.txt"
        }
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            video_file = ydl.prepare_filename(info_dict)
        await m.delete()
        await message.reply_photo(
            photo=thumb_name,
            caption=f"**✅ Started Streaming On VC.**\n\n**🥀 Title:** {title[:20] if len(title) > 20 else title}\n**🐬 Duration:** {duration // 60}:{duration % 60:02d} Mins\n**🦋 Stream Type:** Video\n**👾 Requested By:** {message.from_user.first_name if not message.from_user.last_name else f'{message.from_user.first_name} {message.from_user.last_name}'}\n**⚕️ Join:** @HeartBeat_Muzic"
        )
        is_playing[message.chat.id] = True
        await RAUSHANVC.play(message.chat.id, MediaStream(video_file))
        await asyncio.sleep(duration + 5)
        await manage_playback(message.chat.id, f'{title} {message.id}', duration)
    except Exception as e:
        if "CHAT_ADMIN_REQUIRED" in str(e):
            await message.reply('**Cannot play video admin rights required ❌**')
        else:
            logging.error(e)
            await message.reply(f"Error: {e}")
        chat_id = message.chat.id
        queue_id[chat_id].remove(queue_id.get(chat_id)[0])
        del is_playing[chat_id]
        if not queue_id.get(chat_id):
            await RAUSHANVC.leave_call(chat_id)
    try:
        os.remove(video_file)
        os.remove(thumb_name)
    except Exception as e: logging.error(e)
        
async def manage_playback(chat_id, title, duration):
    global is_playing, queue_id
    try:
        queue_id[chat_id].remove(queue_id.get(chat_id)[0])
        del is_playing[chat_id]
        if not queue_id.get(chat_id):
            await RAUSHANVC.leave_call(chat_id)
    except Exception as e: logging.error(e)

@bot.on_message(filters.command("skp", prefixes=HANDLER) & filters.create(publicFilter) & ~filters.private & ~filters.bot)
async def skip(_, message):
    global queue_id, is_playing
    a = await RAUSHAN.get_chat_member(message.chat.id, message.from_user.id)
    if a.status == ChatMemberStatus.MEMBER or not a.privileges.can_manage_video_chats:
        return await message.reply("**You don't have enough admin rights to use this command ❌**")
    chat_id = message.chat.id
    if queue_id.get(message.chat.id):
        try:
            if len(queue_id.get(message.chat.id)) > 1:
                queue_id[chat_id].remove(queue_id.get(chat_id)[0])
            else:
                await message.reply("**ℹ️ No more queues in the chat leaving...**")
                await RAUSHANVC.leave_call(message.chat.id)
                try: queue_id[chat_id].remove(queue_id.get(chat_id)[0])
                except: pass
                del is_playing[chat_id]
        except Exception as w:
            logging.error(w)
            await message.reply('**ℹ️ No active voice chat to skip!**')
    else:
        await message.reply('**ℹ️ No active voice chat to skip.**')

MOD_NAME = "Play"
MOD_HELP = """**🥀 Your commands**:
.ply - To play a song in voice chat
.vply - To play a youtube video on voice chat
.skip - To skip a playing song/video
.addplay - To allow a chat to use GroupUsers commands
.rplay - To remove permission of a chat to use GroupUsers commands
.getplay - To get allowed permission chats of GroupUsers commands

**👤 GroupUsers commands**:
.ply - To play a song in voice chat
.vply - To play a youtube video on voice chat
.skip - To skip a playing song/video
"""
