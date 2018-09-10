from enum import Enum

redis_config = {
    'host': 'localhost',
    'port': 6379
}


class NotifType(Enum):
    LIKE = 1
    FOLLOW = 2
    FOLLOW_REQUEST = 3
    COMMENT = 4
