import json

import redis


class RedisMeshNodes:
    def __init__(self, redis_client: redis.Redis):
        self._redis_client = redis_client

    def add(self, node):
        self._redis_client.hset('1', '2', '3')

    def get_all(self):
        return self._redis_client.hgetall('1').items()
