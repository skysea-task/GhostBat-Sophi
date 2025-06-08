""" from RAUSHAN import HANDLER
from RAUSHAN.__main__ import RAUSHAN
from pyrogram import filters
import asyncio
import os
from pyrogram import enums

@RAUSHAN.on_message(filters.command("block", prefixes=HANDLER) & filters.me)
async def block_user(_, message):
    if message.chat.type == enums.ChatType.PRIVATE:
        try:
            await RAUSHAN.block_user(message.chat.id)
            await message.reply("➲ I successfully blocked the user ✅.")
        except Exception as e:
            await message.reply(f"**Error:** {e}")
    else:
        if message.chat.type == enums.ChatType.SUPERGROUP:
            if not message.reply_to_message:
                return await message.reply("➲ Reply a user to block.")
            user_id = message.reply_to_message.from_user.id
            try:
                await RAUSHAN.block_user(user_id)
                await message.reply("➲ I successfully blocked the user ✅.")
            except Exception as e:
                await message.reply(f"**Error:** {e}")


@RAUSHAN.on_message(filters.command("unblock", prefixes=HANDLER) & filters.me)
async def unblock_user(_, message):
    if not message.reply_to_message:
        return await message.reply("➲ Reply a user to unblock.")
    user_id = message.reply_to_message.from_user.id
    try:
        await RAUSHAN.unblock_user(user_id)
        await message.reply("➲ I successfully unblocked the user ✅.")
    except Exception as e:
        await message.reply(f"**Error:** {e}")
        
            
MOD_NAME = "Blocks"
MOD_HELP = ".block - Reply to a user or use in dm to block them.\n.unblock - Reply to a user or use in dm to unblock a user."
