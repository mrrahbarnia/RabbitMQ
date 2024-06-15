import logging
import time

from redis import Redis
from django.conf import settings

from producer import publish

logger = logging.getLogger('backend')

HOST = settings.REDIS_HOST
PORT = settings.REDIS_PORT

def connect_redis() -> None:
    r = Redis(host=HOST, port=PORT, decode_responses=True)
    return r

def insert_data(*, email: str, title: str, content: str) -> None:
    """
    Can be used for creating or updating.
    """
    r : Redis = connect_redis()
    r.getset(name=title, value=content)
    publish(method='sending_email', body=email)

def list_titles() -> None:
    r : Redis = connect_redis()
    return r.execute_command('KEYS *')

def send_email(*, email: str) -> None:
    # Simulating a long running task.(sending email)
    logger.info(f'Email is sending to {email}')
    time.sleep(3)
    raise ValueError('Something went wrong')
