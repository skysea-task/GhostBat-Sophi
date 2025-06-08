from RAUSHAN import HANDLER
from RAUSHAN.__main__ import RAUSHAN
from RAUSHAN import *
from config import OWNER_ID as OWN
from pyrogram import filters
import asyncio
import logging
import aiohttp

@RAUSHAN.on_message(filters.command("xlyrics", prefixes=HANDLER) & filters.user(OWN))
async def lyrics(_, message):
  try:
    if len(message.text.split()) < 2:
      return await message.reply("Please enter song name to get lyrics.")
    m = await message.reply('Searching...')
    name = " ".join(message.command[1:])
    surl = f"https://api.lyrics.ovh/suggest/{name.replace(' ', '%20')}"
    async with aiohttp.ClientSession() as session:
      async with session.get(surl) as info:
        if info.status == 200:
          data = await info.json()
          artist_name = data['data'][0]['artist']['name']
          song_title = data['data'][0]['title']
          url = f"https://api.lyrics.ovh/v1/{artist_name}/{song_title}"
          async with session.get(url) as lyric:
            if lyric.status == 200:
              lyric_data = await lyric.json()
              lyric_text = lyric_data['lyrics']
              lyric_text = lyric_text.replace('\n\n', '\n')
              lyric_text = lyric_text.replace('\n\n\n', '\n\n')
              await message.reply(f"**Lyrics of: {artist_name} - {song_title}**\n\n{lyric_text}")
            else:
              await message.reply("Couldn't find the song ❌")
        else:
          await message.reply("Couldn't find the song ❌")
  except Exception as e:
    await message.reply("Couldn't find the song ❌")
    logging.error(e)
  await m.delete()
  

MOD_NAME = 'Lyrics'
MOD_HELP = ".lyrics <song name> - To get lyrics of that song from lyrics.ovh"
# Thanks lyrics.ovh for api 
