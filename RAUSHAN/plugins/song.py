from RAUSHAN import HANDLER
from RAUSHAN.__main__ import RAUSHAN as bot
from config import OWNER_ID as OWN
from pyrogram import filters
import os
import requests
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL

@bot.on_message(filters.command("song", prefixes=HANDLER) & filters.user(OWN))
async def song(_, message):
    if len(message.text.split()) < 2:
        return await message.reply("Provide a song name or YouTube link.")

    query = " ".join(message.command[1:])
    if query.startswith(("www.youtube", "http://", "https://")):
        link = query
        with YoutubeDL({'quiet': True, 'cookiefile': 'cookies.txt'}) as ydl:
            info = ydl.extract_info(link, download=False)
            title = info.get("title", "Unknown Title")
            thumbnail = info.get("thumbnail")
            duration = info.get("duration")
    else:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"]
        thumbnail = results[0]["thumbnails"][0]
        duration = results[0]["duration"]

    thumb_name = f"{title}.jpg"
    if thumbnail:
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)

    msg = await message.reply("📥 Downloading...")
    ydl_opts = {"format": "bestaudio[ext=m4a]", "cookiefile": "cookies.txt"}
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            audio_file = ydl.prepare_filename(info_dict)
        secmul, dur, dur_arr = 1, 0, str(duration).split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        await msg.edit("📤 Uploading...")
        await message.reply_audio(
            audio_file,
            thumb=thumb_name,
            title=title,
            caption=f"{title}",
            duration=dur,
        )
        await msg.delete()
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        await msg.edit(f"Error: {e}")

@bot.on_message(filters.command("video", prefixes=HANDLER) & filters.user(OWN))
async def video(_, message):
    if len(message.text.split()) < 2:
        return await message.reply("Provide a video name or YouTube link.")

    query = " ".join(message.command[1:])
    if query.startswith(("www.youtube", "http://", "https://")):
        link = query
        with YoutubeDL({'quiet': True, 'cookiefile': 'cookies.txt'}) as ydl:
            info = ydl.extract_info(link, download=False)
            title = info.get("title", "Unknown Title")
            thumbnail = info.get("thumbnail")
            duration = info.get("duration")
    else:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"]
        thumbnail = results[0]["thumbnails"][0]
        duration = results[0]["duration"]

    thumb_name = f"{title}.jpg"
    if thumbnail:
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)

    msg = await message.reply("📥 Downloading...")
    ydl_opts = {"format": "best", "cookiefile": "cookies.txt"}
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            video_file = ydl.prepare_filename(info_dict)
        await msg.edit("📤 Uploading...")
        await message.reply_video(
            video_file,
            thumb=thumb_name,
            caption=f"**{title}**",
            duration=duration,
        )
        await msg.delete()
        os.remove(video_file)
        os.remove(thumb_name)
    except Exception as e:
        await msg.edit(f"Error: {e}")

MOD_NAME = "YouTube"
MOD_HELP = ".song <text/link> - To download the song from Youtube.\n.video <text/link> - To download the video from Youtube."
