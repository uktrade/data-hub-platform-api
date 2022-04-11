import json
import redis


class RedisActionContext:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    def flush_database(self):
        self.redis.flushdb()

    def register_context(self, id_):
        root_schema = {
            'version': 1,
            'id': id_,
            'actions': []
        }
        self.redis.set(f"dit:actionContext:#{id_}", json.dumps(root_schema), nx=True)

    def get_context(self, id_):
        context_json = self.redis.get(f"dit:actionContext:#{id_}")
        if context_json is None:
            return None

        return json.loads(context_json)