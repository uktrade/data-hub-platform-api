import pytest

from platform_api.use_case_executor import UseCaseExecutor


@pytest.fixture()
def execute():
    executor = UseCaseExecutor()
    executor._redis.get_client().flushdb()
    yield executor


def test_can_error_when_no_context_registered(execute):
    response = execute('get_contextual_actions', 'dit:datahub:company')
    assert not response['success']
    assert ['NO_ACTION_CONTEXT_DEFINED'] == response['errors']


def test_can_get_no_contextual_actions(execute):
    execute('register_action_context', 'dit:datahub:company')
    response = execute('get_contextual_actions', 'dit:datahub:company')
    contextual_action = response['actions']
    assert response['success']
    assert [] == contextual_action


def test_can_describe_context(execute):
    execute('register_action_context', 'dit:datahub:company')
    response = execute('describe_action_context', 'dit:datahub:company')
    assert {'success': True, 'object': {'id': 'dit:datahub:company'}} == response
