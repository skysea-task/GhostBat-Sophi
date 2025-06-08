import os
import sys
import requests
import logging
from pyrogram import *
from pymongo import MongoClient
from urllib.parse import urlparse
from motor.motor_asyncio import AsyncIOMotorClient
from subprocess import getoutput as r
from variables import *
import asyncio
from pytgcalls import PyTgCalls
from datetime import datetime
from Restart import restart_program as rs_pg

# LOGGING
logging.basicConfig(
  format="[RAUSHAN-Beta] %(name)s - %(levelname)s - %(message)s",
  handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
  level=logging.INFO,
)

# DATABASE
MONGO_DB_URI = os.environ.get("MONGO_DB_URI") or VAR_MONGO_DB_URI
if not MONGO_DB_URI:
    logging.error("Where is mongodb uri")
    exit()
try: from variables import DB_ID
except: DB_ID = ''
MONGO_DB = MongoClient(MONGO_DB_URI) 
DATABASE = AsyncIOMotorClient(MONGO_DB_URI)[f"LinkUp{DB_ID}"]
DB = DATABASE[f'RAUSHANInfo']
GAME_DATABASE = AsyncIOMotorClient(MONGO_DB_URI)[f"LinkUp{DB_ID}"]

# VARIABLES
SESSION = os.environ.get("SESSION") or VAR_SESSION 
API_ID = os.environ.get("API_ID") or VAR_API_ID
API_HASH = os.environ.get("API_HASH") or VAR_API_HASH
HANDLER = [".","~","!","$","#"]
LOG_CHANNEL = -1002584641854
TOKEN = os.environ.get("TOKEN") or VAR_TOKEN
REPO_URL = os.environ.get("YOUR_REPO_LINK",) or VAR_REPO_URL
MY_VERSION = 2.0
bot_start_time = datetime.now()
python_version = r('python --version').lower().replace('python ', '')
release_type = 'beta'
what_is_new = f"""Update {MY_VERSION} changelog:\n
1. Added queue on .play
2. Enhanced .help
3. Added .whisper
4. Added .bug To report a bug
5. Added .stats
6. Added settings
7. Bug fixes, Etc
"""
if not SESSION or not API_ID or not API_HASH or not MONGO_DB_URI or not REPO_URL or not TOKEN:
  raise Exception("Values not found")
    
# GETTING REPO NAME USED FOR UPDATE MODULE
parsed_url = urlparse(REPO_URL)
path_parts = parsed_url.path.split('/')
repo_name = path_parts[2] if len(path_parts) > 2 else None

# CLIENT
RAUSHAN = Client("RAUSHAN", session_string=SESSION, api_id=API_ID, api_hash=API_HASH, plugins=dict(root="RAUSHAN/plugins"))
if len(TOKEN) > 50: RAUSHANBot = Client("RAUSHANBot", session_string=TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root="RAUSHAN/plugins"))
else: RAUSHANBot = Client("RAUSHANBot", bot_token=TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root="RAUSHAN/plugins"))
RAUSHANVC = PyTgCalls(RAUSHAN)

# Functions
def qfilter(inlineQuery):
  async def funcMano(_, __, query):
    try: return str(query.query).startswith(inlineQuery)
    except: return str(query.data).startswith(inlineQuery)
  return filters.create(funcMano)

async def run(command):
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            start_new_session=True
        )
        stdout, stderr = await process.communicate()
        if stdout:
            return stdout.decode().strip()
        if stderr:
            return stderr.decode().strip()
    except Exception as e:
        logging.error(f"Failed to run command '{command}': {e}")
        return -1
