from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.database.conn import get_db

router = APIRouter()

@router.get("")
async def create(db: AsyncIOMotorClient = Depends(get_db)):
    db['video']['subscriptions'].insert_one({"test":"test"})


@router.get("/test")
async def getAll(db: AsyncIOMotorClient = Depends(get_db)):
    cursor = db['video']['subscriptions'].find({})
    for document in await cursor.to_list(length=100):
        print(document)
