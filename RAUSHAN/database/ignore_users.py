from RAUSHAN import DATABASE
import asyncio
import random

db = DATABASE["IGNORED USERS"]

class IGNORED_USERS:
    async def ADD(self, user_id):
        try:
            await db.update_one({"_id": 1}, {"$addToSet": {"IGNORED_USERS": user_id}}, upsert=True)
            return "SUCCESS"
        except Exception as e:
            print("Error while adding user in ignored list", e)
            return e
    async def GET(self):
        Find = await db.find_one({"_id": 1})
        if not Find:
            return []
        else:
            value = Find.get("IGNORED_USERS", [])
            return value
    async def REMOVE(self, user_id):
        try:
            await db.update_one({"_id": 1}, {"$pull": {"IGNORED_USERS": user_id}})
            return "SUCCESS"
        except Exception as e:
            return e
