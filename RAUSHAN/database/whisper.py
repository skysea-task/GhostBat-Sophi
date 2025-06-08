from RAUSHAN import DATABASE
import logging

db = DATABASE["whisper"]

class whisper:
    async def get(self, id):
        try:
            info = await db.find_one({"_id": id})
            if info and 'message' in info and 'user_id' in info:
                return {'message': info['message'], 'id': info['user_id']}
            return {}
        except Exception as e:
            logging.error(e)
            return {}

    async def add(self, message, user_id):
        try:
            counter = await db.find_one({"_id": 1})
            wid = counter['wid'] + 1 if counter else 1
            await db.update_one({"_id": 1}, {"$set": {"wid": wid}}, upsert=True)
            await db.update_one({"_id": wid}, {"$set": {"message": message, "user_id": user_id}}, upsert=True)
            return wid
        except Exception as e:
            logging.error(e)
