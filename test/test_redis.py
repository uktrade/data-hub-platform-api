from platform_api.redis_connection import RedisConnection


def test_redis_connection_available():
    connection = RedisConnection()
    assert connection.get_client().ping()
