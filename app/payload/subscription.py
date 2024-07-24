from enum import Enum

from pydantic import BaseModel, Field

class SubscriptionInterval(str, Enum):
    MONTH = 'month'
    YEAR = 'year'

class CreateSubscriptionPayload(BaseModel):
    customerId: str = Field(..., description='고객 id(숫자로 이루어진 문자열)', example='1321321312')
    subscriptionCost: float = Field(..., description='구독 비용', example=39)
    subscriptionInterval: SubscriptionInterval = Field(..., description='구독 interval', example=SubscriptionInterval.MONTH)

class DeleteSubscriptionPayload(BaseModel):
    customerId : str = Field(..., description='고객 id(숫자로 이루어진 문자열)', examples='1321321312')

