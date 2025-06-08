from pyrogram import *
from RAUSHAN import *
import asyncio
from ..database.silent import Silent
import logging

silent, info = Silent(), logging.info

async def SilentFilter(_, __, m):
  if await silent.get() and m.chat.id not in await silent.get_exceptions():
    try:
      await RAUSHAN.read_chat_history(m.chat.id)
      await RAUSHAN.read_mentions(m.chat.id)
      await RAUSHAN.read_reactions(m.chat.id)
    except: pass
  return False

@RAUSHAN.on_message(filters.command('silent', prefixes=HANDLER) & filters.me)
async def SetSilent(_, m):
  x = await silent.get()
  if x:
    await silent.off()
    return await m.reply("Successfully, disabled silent mode.")
  await silent.on()
  await m.reply("Success! all your new messages will be marked as read.")
  
@RAUSHAN.on_message(filters.command('psilent', prefixes=HANDLER) & filters.me)
async def PauseSilent(_, m):
  await silent.add_exception(m.chat.id)
  await m.reply("Chat notifications are paused.")

@RAUSHAN.on_message(filters.command(['rsilent', 'upsilent'], prefixes=HANDLER) & filters.me)
async def ResumeSilent(_, m):
  await silent.remove_exception(m.chat.id)
  await m.reply("Chat notifications are unpaused.")
    
@RAUSHAN.on_message(~filters.me & filters.create(SilentFilter))
@RAUSHAN.on_message_reaction(~filters.me & filters.create(SilentFilter))
async def do_ntg(_, __):
  pass
  
MOD_NAME = "Silent"
MOD_HELP = "sooon..."