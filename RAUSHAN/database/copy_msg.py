from RAUSHAN import DATABASE
import asyncio
import random

db = DATABASE["Copy_message"]

async def SAVE_MSG(msg_id: int, msg_chat: int, album=False):
        try:
            document = await db.find_one({"_id": 1})
            if document:
                await db.update_one({"_id": 1}, {"$set": {"COPIED": True, "CHAT": msg_chat, "ALBUM": album, "ID": msg_id}})
            else:
                await db.insert_one({"_id": 1, "COPIED": True, "CHAT": msg_chat, "ALBUM": album, "ID": msg_id})
            return "SUCCESS"
        except Exception as e:
            return str(e)
        
async def COPIED():
    try:
        Find = await db.find_one({"_id": 1})
        if Find:
            return Find.get("COPIED", False)
        else:
            return False
    except Exception as e:
        print(f"Error in COPIED: {e}")
        return False
        
async def UNSAVE_MSG():
    COPIED_MSG = await COPIED()
    if not COPIED_MSG:
        return "ALREADY_EMPTY"
    try:
        await db.update_one({"_id": 1}, {"$set": {"COPIED": False, "CHAT": 0, "ALBUM": None, "ID": 0}})
        return "SUCCESS"
    except Exception as e:
        return str(e)
        
async def CHAT_ID():
    Find = await db.find_one({"_id": 1})
    if not Find:
        return False
    else:
        value = Find["CHAT"]
        return value

async def MSG_ID():
    Find = await db.find_one({"_id": 1})
    if not Find:
        return False
    else:
        value = Find["ID"]
        return value

async def IS_ALBUM():
    Find = await db.find_one({"_id": 1})
    if not Find:
        return False
    else:
        value = Find["ALBUM"]
        return bool(value)
        
