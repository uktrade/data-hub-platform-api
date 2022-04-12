import pytest

from platform_api.use_case_executor import UseCaseExecutor


@pytest.fixture()
def use_case_executor():
    executor = UseCaseExecutor()
    executor._redis.get_client().flushdb()
    yield executor


def test_can_error_when_no_context_registered(use_case_executor):
    response = use_case_executor('get_contextual_actions', 'dit:datahub:company')
    assert not response['success']
    assert ['NO_ACTION_CONTEXT_DEFINED'] == response['errors']


def test_can_get_no_contextual_actions(use_case_executor):
    use_case_executor('register_action_context', 'dit:datahub:company')
    response = use_case_executor('get_contextual_actions', 'dit:datahub:company')
    contextual_action = response['actions']
    assert response['success']
    assert [] == contextual_action
