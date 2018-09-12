import redis
import json
from message_queue.utils import redis_config, NotifType
import requests

r = redis.Redis(**redis_config)


def run():
    while True:
        json_data = r.brpop('notification')
        ok_data = json_data[1].decode('utf-8')
        data = json.loads(ok_data)


        req =requests.post('http://localhost:8000/social/save/notif/', json=data)

if __name__ == '__main__':
    run()
