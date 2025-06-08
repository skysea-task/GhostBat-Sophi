""" from RAUSHAN import *
from pyrogram import *

keypad = {'A': 2, 'B': 22, 'C': 222, 'D': 3, 'E': 33, 'F': 333, 'G': 4, 'H': 44, 'I': 444, 'J': 5, 'K': 55, 'L': 555, 'M': 6, 'N': 66, 'O': 666, 'P': 7, 'Q': 77, 'R': 777, 'S': 7777, 'T': 8, 'U': 88, 'V': 888, 'W': 9, 'X': 99, 'Y': 999, 'Z': 9999, ' ': 0}
reverse_keypad = {v: k for k, v in keypad.items()}

@RAUSHAN.on_message(filters.command("kencode", prefixes=HANDLER) & filters.user("me"))
async def keypad_encode(_, message):
  if len(message.command) < 2: return await message.reply("Please give a text to encode")
  text = message.text.split(None, 1)[1]
  encoded = ','.join(str(keypad[c]) for c in text.upper() if c in keypad)
  await message.reply(f"**Encoded text:** {encoded}")
  
@RAUSHAN.on_message(filters.command("kdecode", prefixes=HANDLER) & filters.user("me"))
async def keypad_decode(_, message):
  if len(message.command) < 2: return await message.reply("Please give a encoded text to decode")
  sequence = message.text.split(None, 1)[1]
  decoded = ''.join(reverse_keypad.get(int(num), '') for num in sequence.split(','))
  await message.reply(f"**Decoded text:** {decoded}")

MOD_NAME = "encode"
MOD_HELP = ".kencode <text> - To get keypad style encoded text\n.kdecode <text> - To decode encode text"
