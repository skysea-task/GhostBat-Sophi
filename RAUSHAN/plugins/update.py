""" from pyrogram import filters
from RAUSHAN.__main__ import RAUSHAN
from RAUSHAN import REPO_URL, repo_name, HANDLER
from config import OWNER_ID
import subprocess

OWN = OWNER_ID

@RAUSHAN.on_message(filters.command("update", prefixes=HANDLER) & filters.user(OWN))
async def update_repo(_, message):
    await message.reply_text("`Updating...`")
    try:
        command = f"cd && rm -rf {repo_name} && git clone {REPO_URL} && cd {repo_name} && ls && python3 -m RAUSHAN"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        exit()
    except Exception as e:
        await message.reply_text("Update Failed ", e)
        print("Error on Updating", e)
