from redis import Redis
from django.conf import settings

HOST = settings.REDIS_HOST
PORT = settings.REDIS_PORT

def connect_redis() -> None:
    r = Redis(host=HOST, port=PORT, decode_responses=True)
    return r

def insert_data(*, title: str, content: str) -> None:
    """
    Can be used for creating or updating.
    """
    r : Redis = connect_redis()
    r.getset(name=title, value=content)

def list_titles() -> None:
    r : Redis = connect_redis()
    return r.execute_command('KEYS *')
