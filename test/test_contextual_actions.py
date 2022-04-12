import pytest

from platform_api.use_case_executor import UseCaseExecutor


@pytest.fixture(autouse=True)
def before_each():
    UseCaseExecutor()._redis.get_client().flushdb()


def test_can_error_when_no_context_registered():
    response = UseCaseExecutor()('get_contextual_actions', 'dit:datahub:company')
    assert not response['success']
    assert ['NO_ACTION_CONTEXT_DEFINED'] == response['errors']


def test_can_get_no_contextual_actions():
    UseCaseExecutor()('register_action_context', 'dit:datahub:company')
    response = UseCaseExecutor()('get_contextual_actions', 'dit:datahub:company')
    contextual_action = response['actions']
    assert response['success']
    assert [] == contextual_action
