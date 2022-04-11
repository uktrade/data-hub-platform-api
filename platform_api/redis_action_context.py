import json


class RedisActionContext:
    def __init__(self, redis_client):
        self._redis_client = redis_client

    def register_context(self, id_):
        root_schema = {
            'version': 1,
            'id': id_,
            'actions': []
        }
        self._redis_client.set(f"dit:actionContext:#{id_}", json.dumps(root_schema), nx=True)

    def get_context(self, id_):
        context_json = self._redis_client.get(f"dit:actionContext:#{id_}")
        if context_json is None:
            return None

        return json.loads(context_json)