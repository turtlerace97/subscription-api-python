from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from app.database.conn import get_db
from app.service.subscription import SubscriptionService

router = APIRouter()

def get_video_service(db: AsyncIOMotorClient = Depends(get_db)):
    return SubscriptionService(db)

@router.post("")
async def create(service: SubscriptionService = Depends(get_video_service)):
    await service.create_subscription({"test":"test"})
    return JSONResponse(status_code=201, content={"message":"created"})


@router.get("")
async def getAll(service: SubscriptionService = Depends(get_video_service)):
    result = await service.get_all_subscriptions({},{})
    return JSONResponse(status_code=200, content={"data":result})

@router.get("/long-term-subscribers")
async def getLongTermSubscribers(service: SubscriptionService = Depends(get_video_service)):
    result = await service.get_long_term_subscribers({})
    return JSONResponse(status_code=200, content={"data":result})

