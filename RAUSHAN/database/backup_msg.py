from RAUSHAN import DATABASE
import asyncio

db = DATABASE["BACKUP_MESSAGE_TM"]

async def ENABLE_BACKUP(group=False):
    doc = {"_id": 1, "stats": True}
    gdoc = {"_id": 1, "gstats": True}
    try:
        if group:
            return await db.insert_one(gdoc)
        await db.insert_one(doc)
    except Exception:
        if group:
           return await db.update_one({"_id": 1}, {"$set": {"gstats": True}})
        await db.update_one({"_id": 1}, {"$set": {"stats": True}})
        
async def DISABLE_BACKUP(group=False):
    if group:
        await db.update_one({"_id": 1}, {"$set": {"gstats": False}})
        return
    await db.update_one({"_id": 1}, {"$set": {"stats": False}})

async def GET_BACKUP(group=False):
    Find = await db.find_one({"_id": 1})
    if not Find:
        return False
    else:
        if group:
            try:
                stats = Find["gstats"]
                return stats
            except:
                return False
        try:
            stats = Find["stats"]
            return stats
        except:
            return False

async def ADD_BACKUP_CHAT(chat_id: int):
    await db.update_one({"_id": 1}, {"$addToSet": {"CHATS": chat_id}}, upsert=True)

async def REMOVE_BACKUP_CHAT(chat_id: int):
    await db.update_one({"_id": 1}, {"$pull": {"CHATS": chat_id}})

async def GET_BACKUP_CHATS():
    Find = await db.find_one({"_id": 1})
    if not Find:
        return []
    else:
        value = Find.get("CHATS", [])
        return value

async def ADD_STOP_BACKUP_CHAT(chat_id: int):
    await db.update_one({"_id": 1}, {"$addToSet": {"STOPED_CHATS": chat_id}}, upsert=True)
    
async def REMOVE_STOP_BACKUP_CHAT(chat_id: int):
    await db.update_one({"_id": 1}, {"$pull": {"STOPED_CHATS": chat_id}})

async def GET_STOP_BACKUP_CHATS():
    Find = await db.find_one({"_id": 1})
    if not Find:
        return []
    else:
        value = Find.get("STOPED_CHATS", [])
        return value

async def SET_BACKUP_CHANNEL_ID(user_id, channel_id):
    await db.update_one({"_id": 1}, {"$set": {f"{user_id}": channel_id}})

async def GET_BACKUP_CHANNEL_ID(chat_id):
    Find = await db.find_one({"_id": 1})
    if not Find:
        return False
    else:
        channel = Find[f"{chat_id}"]
        return channel
