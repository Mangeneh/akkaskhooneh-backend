import redis
import json
from message_queue.utils import redis_config
import os, django
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")
django.setup()

from social.models import Notification
from message_queue.utils import NotifType

r = redis.Redis(**redis_config)


def run():
    while True:
        json_data = r.brpop('notification')
        ok_data = json_data[1].decode('utf-8')
        data = json.loads(ok_data)

        requests.post('http://localhost:8000', data=data)


if __name__ == '__main__':
    run()
