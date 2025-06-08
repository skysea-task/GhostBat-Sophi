""" from RAUSHAN import DATABASE
import asyncio
import random

db = DATABASE["Update"]

class UPDATE:
    async def ADD(self, add: bool, chat: int):
        doc = {"_id": 1, "stats": add, "chat": chat}
        try:
            await db.insert_one(doc)
        except:
            await db.update_one(doc)
    async def GET(self):
        Find = await db.find_one({"_id": 1})
        if not Find:
            return False
        else:
            stats = bool(Find["stats"])
            if stats == True:
                return int(Find["chat"])
            return False
