import redis
import json
from message_queue.utils import redis_config, LogWrapper, _logger
import requests

logger = LogWrapper(_logger)

r = redis.Redis(**redis_config)


def run():
    while True:
        json_data = r.brpop('notification')
        ok_data = json_data[1].decode('utf-8')
        data = json.loads(ok_data)

        logger.info("data: {}".format(ok_data))

        req = requests.post('http://localhost:8000/social/save/notif/', json=data)

        logger.info("data: {}, status: {}".format(ok_data, req.status_code))


if __name__ == '__main__':
    run()
