from typing import Any, Union
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient

from app.database.conn import get_db
from app.payload.subscription import CreateSubscriptionPayload, DeleteSubscriptionPayload
from app.query.common import SortEnum
from app.query.subscription import SubscriptionLongTermUsersQuery, SubscriptionsQuery
from app.service.subscription import SubscriptionService


from datetime import datetime

router = APIRouter()

def get_video_service(db: AsyncIOMotorClient = Depends(get_db)):
    return SubscriptionService(db)

@router.get("health")
def health():
    return {"msg":"hello"}

@router.post("")
async def create(
    payload : CreateSubscriptionPayload,
    service: SubscriptionService = Depends(get_video_service),
):
    filter = {
            'customer_id': payload.customerId,
            'canceled_date': None,
            'was_subscription_paid': True
    }
    sort = [('created_date', -1)]

    is_exist = await service.get_all_subscriptions(
        filter,
        sort,
        limit=1,
        offset=0,
    )
    
    if is_empty(is_exist):
        raise HTTPException(status_code=400, detail="already exist")
    
    subscription = {
            'customer_id': payload.customerId,
            'subscription_cost': payload.subscriptionCost,
            'subscription_interval': payload.subscriptionInterval.value,
            'canceled_date': None,
            'was_subscription_paid': True,
            'created_date': datetime.utcnow()
        }
    
    inserted_id = await service.create_subscription(subscription)
    subscription['_id'] = inserted_id
    

    try:
        process_payment()
    except Exception as err:
        subscription['was_subscription_paid'] = False
        raise err
    finally:
        await service.update_one(
                {'_id': subscription['_id']},
                {'$set': {'was_subscription_paid': subscription['was_subscription_paid']}}
            )

    return JSONResponse(status_code=201, content={"message":"ok"})


@router.get("")
async def getAll(
    query : SubscriptionsQuery= Depends(),
    service: SubscriptionService = Depends(get_video_service),
):
    filter_query = {"canceled_date": None}

    if query.startDate and query.endDate:
        filter_query["created_date"] = {
            "$gte": query.startDate,
            "$lte": query.endDate
        }

    if query.customerId:
        filter_query["customer_id"] = query.customerId

    if query.subscriptionInterval:
        filter_query["subscription_interval"] = query.subscriptionInterval

    order_field = query.order
    sort_order = -1 if query.sort == SortEnum.DESC else 1
    sort_query = {order_field: sort_order}

    result = await service.get_all_subscriptions(filter_query,sort_query,query.limit, query.offset)
    return JSONResponse(status_code=200, content={"data":jsonable_encoder(result)})

@router.get("/long-term-subscribers")
async def getLongTermSubscribers(
    query : SubscriptionLongTermUsersQuery = Depends(),
    service: SubscriptionService = Depends(get_video_service),
):
    match_stage = {}

    if query.id:
        match_stage["_id"] = { "$gt": ObjectId(query.id) }

    result = await service.get_long_term_subscribers(match_stage)
    return JSONResponse(status_code=200, content={"data":jsonable_encoder(result)})

@router.delete("/{customerId}")
async def cancel_subscription(
    customerId: str,
    service: SubscriptionService = Depends(get_video_service),
):
    filter = {
            'customer_id': customerId,
            'canceled_date': None,
            'was_subscription_paid': True
        }
    sort = [('created_date', -1)]
    is_exist = await service.get_all_subscriptions(filter, sort)
    print(is_exist)
    if len(is_exist) == 0:
            raise HTTPException(status_code=400, detail="no data to remove")

    if len(is_exist) > 1:
        raise HTTPException(status_code=500, detail="internal server error")

    await service.update_one(
        {'_id': ObjectId(is_exist[0]['_id'])},
        {'$set': {'canceled_date': datetime.utcnow()}}
    )
    return JSONResponse(status_code=201, content={"message":"ok"})

def process_payment() -> None:
    print("do payment....")

def is_empty(value: Union[list, dict, str, Any]) -> bool:
    if value is None:
        return True
    if isinstance(value, (list, dict, str)) and len(value) == 0:
        return True
    if isinstance(value, (list, dict)) and not value:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    return False

