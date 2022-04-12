from platform_api.redis_action_context import RedisActionContext
from platform_api.redis_connection import RedisConnection
from platform_api.use_case.get_contextual_actions import GetContextualActions
from platform_api.use_case.register_action_context import RegisterActionContext


class UseCaseExecutor:
    def __init__(self):
        self._redis = RedisConnection()
        action_context_gateway = RedisActionContext(self._redis.get_client())
        self.use_cases = {
            'get_contextual_actions': GetContextualActions(action_context_gateway),
            'register_action_context': RegisterActionContext(action_context_gateway)
        }

    def __call__(self, use_case, *args, **kwargs):
        return self.use_cases[use_case](*args, **kwargs)