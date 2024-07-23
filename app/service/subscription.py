from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

class SubscriptionService:
    def __init__(self, db: AsyncIOMotorClient):
        self.db : AsyncIOMotorClient = db

    async def create_subscription(self, data: dict) -> None:
        await self.db['subscriptions'].insert_one(data)

    async def get_all_subscriptions(self, filter : dict, order : dict, limit : int = 10, offset : int = 0):
        cursor = self.db['subscriptions'].find().limit(limit=limit).skip(offset)
        if order and order != {}:
            cursor.sort(order)
        
        result = await cursor.to_list(length=limit)
        result = convert_objectid(result)  
        return result    
    
    async def update_subscriptions(self, filter):
        self.db['video']['subscriptions'].find_one_and_update(filter=filter)
    
    async def get_long_term_subscribers(self, match_stage: dict, count=10):
        current_date = datetime.utcnow()
        pipeline = [
            {
                "$match": match_stage
            },
            {
                "$addFields": {
                    "dateDifference": {
                        "$abs": {
                            "$subtract": [current_date, "$created_date"]
                        }
                    }
                }
            },
            {
                "$sort": { "dateDifference": -1 }
            },
            {
                "$limit": count
            },
            {
                "$project": {
                    "dateDifference": 0
                }
            }
        ]
        cursor = self.db['video']['subscriptions'].aggregate(pipeline)
        result = await cursor.to_list(length=count)
        result = convert_objectid(result)
        return result

def convert_objectid(data):
    if isinstance(data, list):
        return [convert_objectid(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_objectid(value) for key, value in data.items()}
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data 

        
        
