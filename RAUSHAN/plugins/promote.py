""" from pyrogram.types import ChatPrivileges
from pyrogram import *
from RAUSHAN import RAUSHAN
from RAUSHAN import HANDLER
import asyncio
import logging
from config import OWNER_ID
from pyrogram.enums import ChatMemberStatus

@RAUSHAN.on_message(filters.command(["promote", "fpromote", "lpromote", "lowpromote", "fullpromote"], prefixes=HANDLER) & filters.user("me"))
async def promote(_, message):
    title = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        title = " ".join(message.command[1:]) or None
    else:
        if len(message.command) < 2:
            return await message.reply("Reply to a user or enter the user ID to promote.")
        txt = " ".join(message.command[1:])
        try:
            user_id = await RAUSHAN.get_chat_member(message.chat.id, txt)
            user_id = user_id.user.id
        except: return await message.reply("Reply to a user or enter the user ID to promote.")      
    if user_id == message.from_user.id:
        return await message.reply("You can't promote yourself!")
    target = await RAUSHAN.get_chat_member(message.chat.id, user_id)
    you = await RAUSHAN.get_chat_member(message.chat.id, message.from_user.id)
    if target.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return await message.reply("**ℹ️ The user is admin/owner already!**")
    if not you.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER] or not you.privileges.can_promote_members:
        return await message.reply("**ℹ️ You don't have enough admin rights to do this!**")
    if message.text[1:].startswith('f'):
        privileges = ChatPrivileges(
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True,
            can_manage_chat=True,
            can_manage_video_chats=True,
            can_promote_members=True,
            can_delete_messages=True,
            can_restrict_members=True,
            can_delete_stories=True,
            can_edit_stories=True,
            can_post_stories=True,
            is_anonymous=False
        )
        type = 'Full'
    elif message.text[1:].startswith('l'):
        privileges = ChatPrivileges(
            can_change_info=False,
            can_invite_users=True,
            can_pin_messages=False,
            can_manage_chat=False,
            can_manage_video_chats=True,
            can_post_stories=False,
            can_manage_topics=False,
            can_delete_messages=False,
            is_anonymous=False
        )
        type = 'Low'
    else:
        privileges = ChatPrivileges(
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True,
            can_manage_chat=True,
            can_manage_video_chats=True,
            can_delete_messages=True,
            can_delete_stories=True,
            can_edit_stories=True,
            can_post_stories=True,
            is_anonymous=False
        )
        type = ''
    try:
        await RAUSHAN.promote_chat_member(message.chat.id, user_id, privileges)
        if title: await RAUSHAN.set_administrator_title(message.chat.id, user_id, title[:15])
        await message.reply(f"Successfuly {type}promoted!")
    except Exception as e:
        logging.error(e)
        await message.reply(f"**Error:** {e}")

@RAUSHAN.on_message(filters.command("demote", prefixes=HANDLER) & filters.user("me"))
async def demote(_, message):
    if message.reply_to_message: user_id = str(message.reply_to_message.from_user.id)
    else:
        if len(message.command) < 2:
            return await message.reply("Reply to a user or enter the user ID to demote.")
        txt = " ".join(message.command[1:])
        try:
            user_id = await RAUSHAN.get_chat_member(message.chat.id, txt)
            user_id = user_id.user.id
        except: return await message.reply("Reply to a user or enter the user ID to demote.")
    if user_id == message.from_user.id:
        return await message.reply("You can't promote yourself!")
    target = await RAUSHAN.get_chat_member(message.chat.id, user_id)
    you = await RAUSHAN.get_chat_member(message.chat.id, message.from_user.id)
    if not target.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return await message.reply("**ℹ️ The user not a admin to demote!**")
    if not you.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER] or not you.privileges.can_promote_members:
        return await message.reply("**ℹ️ You don't have enough admin rights to do this!**")
    privileges = ChatPrivileges(
        can_change_info=False,
        can_invite_users=False,
        can_pin_messages=False,
        can_manage_chat=False,
        can_manage_video_chats=False,
        can_manage_topics=False,
        can_delete_messages=False,
        can_delete_stories=False,
        can_edit_stories=False,
        can_post_stories=False,
        is_anonymous=False
    )
    try:
        await RAUSHAN.promote_chat_member(message.chat.id, user_id, privileges)
        await message.reply("Successfuly demoted!")
    except Exception as e:
        logging.error(e)
        await message.reply(f"**Error:** {e}")

MOD_NAME = "Promote"
MOD_HELP = """

""".promote (reply or username) - To promote them with basic rights.
.lpromote (reply or username) - To promote them with low rights.
.fpromote (reply or username) - To promote them with all rights.
.demote (reply or username) - To demote them.
"""
