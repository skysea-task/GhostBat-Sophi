""" from RAUSHAN import DATABASE
import asyncio

db = DATABASE["PM_GUARD"]

async def SET_PM_GUARD(maximum_warn_count):
    doc = {"_id": 1, "status": True, "warn_count": maximum_warn_count}
    try:
        await db.insert_one(doc)
    except Exception:
        await db.update_one({"_id": 1}, {"$set": {"status": True, "warn_count": maximum_warn_count}})

async def GET_PM_GUARD():
    Find = await db.find_one({"_id": 1})
    if not Find:
        return False
    else:
        value = Find["status"]
        return value

async def GET_WARNING_COUNT():
    Find = await db.find_one({"_id": 1})
    if not Find:
        return None
    else:
        value = Find["warn_count"]
        return value
    
async def UNSET_PM_GUARD():
    await db.update_one({"_id": 1}, {"$set": {"status": False, "warn_count": None}})

async def GET_APPROVED_USERS():
    Find = await db.find_one({"_id": 2})
    if not Find:
        return []  # Return an empty list if no approved users are found
    else:
        value = Find.get("approved_users", [])  # Ensure default value is an empty list
        return value
        
async def ADD_APPROVED_USER(user_id):
    await db.update_one({"_id": 2}, {"$addToSet": {"approved_users": user_id}}, upsert=True)

async def REMOVE_APPROVED_USER(user_id):
    await db.update_one({"_id": 2}, {"$pull": {"approved_users": user_id}})

async def SET_DEFAULT_MESSAGE_LIMIT(count):
    doc = {"_id": 3, "MESSAGE_LIMIT": count}
    try:
        await db.insert_one(doc)
    except Exception:
        await db.update_one({"_id": 3}, {"$set": {"MESSAGE_LIMIT": count}})

async def GET_DEFAULT_MESSAGE_LIMIT():
    Find = await db.find_one({"_id": 3})
    if not Find:
        return None
    else:
        value = Find["MESSAGE_LIMIT"]
        return value
