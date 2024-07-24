from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from app.database.conn import get_db
from app.payload.subscription import CreateSubscriptionPayload
from app.query.subscription import SubscriptionLongTermUsersQuery, SubscriptionsQuery
from app.service.subscription import SubscriptionService

router = APIRouter()

def get_video_service(db: AsyncIOMotorClient = Depends(get_db)):
    return SubscriptionService(db)

@router.post("")
async def create(payload : CreateSubscriptionPayload,service: SubscriptionService = Depends(get_video_service)):
    await service.create_subscription(payload.model_dump())
    return JSONResponse(status_code=201, content={"message":"ok"})


@router.get("")
async def getAll(
    query : SubscriptionsQuery= Depends(),
    service: SubscriptionService = Depends(get_video_service),
):
    result = await service.get_all_subscriptions({},{})
    return JSONResponse(status_code=200, content={"data":result})

@router.get("/long-term-subscribers")
async def getLongTermSubscribers(
    query : SubscriptionLongTermUsersQuery = Depends(),
    service: SubscriptionService = Depends(get_video_service),
):
    result = await service.get_long_term_subscribers({})
    return JSONResponse(status_code=200, content={"data":result})

@router.delete("")
async def cancel_subscription(service: SubscriptionService = Depends(get_video_service)):
    await service.update_canceled_date({})
    return JSONResponse(status_code=201, content={"message":"ok"})


