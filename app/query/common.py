
from typing import Optional
from enum import Enum
from datetime import datetime

from pydantic import BaseModel, Field


class OrderEnum(str, Enum):
    CREATED_DATE = 'created_date'
    CANCELED_DATE = 'canceled_date'

class SortEnum(str, Enum):
    DESC = 'desc'
    ASC = 'asc'

class SubscriptionInterval(str, Enum):
    MONTH = 'MONTH'
    YEAR = 'YEAR'
    # 필요한 다른 interval을 추가할 수 있어

class PaginationQuery(BaseModel):
    limit: Optional[int] = Field(10, description='가져올 갯수', ge=0)
    offset: Optional[int] = Field(0, description='페이지 넘버(0 이상)', ge=0)

class CursorBasedQuery(BaseModel):
    id: Optional[str] = Field(None, description='몽고 id(null 일 경우 처음부터, 리스트로 응답받은 마지막데이터의 몽고 id를 넣으면 됩니다.)')
    count: Optional[int] = Field(10, description='가져올 갯수', ge=0)

class OrderQuery(BaseModel):
    order: Optional[OrderEnum] = Field(OrderEnum.CREATED_DATE, description='정렬 기준')
    sort: Optional[SortEnum] = Field(SortEnum.DESC, description='정렬 방향')

class SearchQuery(BaseModel):
    customerId: Optional[str] = Field(None, description='검색하고자 하는 고객 id')
    startDate: Optional[datetime] = Field(None, description='구독 시작한 날짜 범위 검색 시작(UTC)')
    endDate: Optional[datetime] = Field(None, description='구독 시작한 날짜 범위 검색 끝(UTC)')
    subscriptionInterval: Optional[SubscriptionInterval] = Field(None, description='구독 인터벌 검색')