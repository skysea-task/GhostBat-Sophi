from requests import get
from RAUSHAN import HANDLER
from RAUSHAN.__main__ import RAUSHAN
from config import OWNER_ID
from pyrogram import filters
import asyncio
import os

@RAUSHAN.on_message(filters.command("git", prefixes=HANDLER) & filters.user(OWNER_ID))
async def git(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Master, give me GitHub username")
    user = message.text.split(None, 1)[1]
    res = get(f"https://api.github.com/users/{user}").json()
    data = f"""
**👤 Name:** {res['name']}
**🌐 Username:** `{res['login']}`
**🔗 Link:** [{res['login']}]({res['html_url']})
**⚕️ Bio:** `{res['bio']}`
**💻 Company:** {res['company']}
**🍃 Blog:** {res['blog']}
**🚩 Location:** {res['location']}
**🛠️ Repos:** `{res['public_repos']}`
**✨ Followers:** `{res['followers']}`
**🌟 Following:** `{res['following']}`
**🏦 Account created:** `{res['created_at']}`
"""
    with open(f"{user}.jpg", "wb") as f:
        kek = get(res["avatar_url"]).content
        f.write(kek)

    await message.reply_photo(f"{user}.jpg", caption=data)
    os.remove(f"{user}.jpg")

MOD_NAME = 'Git'
MOD_HELP = ".git <github username> - To get information of that github account"
