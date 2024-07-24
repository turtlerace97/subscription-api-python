from app.query.common import CursorBasedQuery, OrderQuery, PaginationQuery, SearchQuery


class SubscriptionsQuery(PaginationQuery, OrderQuery, SearchQuery):
    pass

class SubscriptionLongTermUsersQuery(CursorBasedQuery):
    pass