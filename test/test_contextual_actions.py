import pytest

from platform_api.redis_action_context import RedisActionContext


class GetContextualActions:
    def __init__(self, action_context_gateway):
        self.action_context_gateway = action_context_gateway

    def __call__(self, context_id):
        context = self.action_context_gateway.get_context(context_id)
        if context is None:
            return {
                'success': False,
                'errors': ['NO_ACTION_CONTEXT_DEFINED']

            }

        return {
            'success': True,
            'actions': []
        }


class RegisterActionContext:
    def __init__(self, action_context_gateway):
        self.action_context_gateway = action_context_gateway

    def __call__(self, id_):
        self.action_context_gateway.register_context(id_)


@pytest.fixture(autouse=True)
def before_each():
    RedisActionContext().flush_database()


def test_can_error_when_no_context_registered():
    action_context_gateway = RedisActionContext()

    get_contextual_actions = GetContextualActions(action_context_gateway)
    response = get_contextual_actions('dit:datahub:company')
    assert not response['success']
    assert ['NO_ACTION_CONTEXT_DEFINED'] == response['errors']


def test_can_get_no_contextual_actions():
    action_context_gateway = RedisActionContext()

    register_action_context = RegisterActionContext(action_context_gateway)
    register_action_context('dit:datahub:company')

    get_contextual_actions = GetContextualActions(action_context_gateway)
    response = get_contextual_actions('dit:datahub:company')
    contextual_action = response['actions']
    assert response['success']
    assert [] == contextual_action

