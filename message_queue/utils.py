from enum import Enum
import os

os.environ.setdefault('REDIS_ADDRESS', 'localhost')


redis_config = {
    'host': os.environ.get('REDIS_ADDRESSS'),
    'port': 6379
}


class NotifType(Enum):
    LIKE = 1
    FOLLOW = 2
    FOLLOW_REQUEST = 3
    COMMENT = 4
