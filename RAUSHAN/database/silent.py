from RAUSHAN import DATABASE
import logging

db = DATABASE["silent"]

class Silent:
  async def on(self):
    await db.update_one({"_id": 143}, {"$set": {"status": True}}, upsert=True)
  async def off(self):
    await db.update_one({"_id": 143}, {"$set": {"status": False}}, upsert=True)
  async def get(self):
    x = await db.find_one({"_id": 143})
    return x.get('status') if x else False
  async def add_exception(self, chat_id):
    await db.update_one({"_id": 'mano'}, {"$addToSet": {"exceptions": chat_id}}, upsert=True)
  async def get_exceptions(self):
    x = await db.find_one({"_id": 'mano'})
    return x.get("exceptions", []) if x else []
  async def remove_exception(self, chat_id):
    await db.update_one({"_id": 'mano'}, {"$pull": {"exceptions": chat_id}}, upsert=True)