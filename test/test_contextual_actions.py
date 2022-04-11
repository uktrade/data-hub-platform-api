import pytest

from platform_api.redis_action_context import RedisActionContext
from platform_api.use_case.get_contextual_actions import GetContextualActions
from platform_api.use_case.register_action_context import RegisterActionContext


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
