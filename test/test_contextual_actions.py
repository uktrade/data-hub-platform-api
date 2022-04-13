import pytest

from platform_api.use_case_executor import UseCaseExecutor


@pytest.fixture()
def execute():
    execute = UseCaseExecutor()
    execute('flush_redis_database')
    yield execute


def test_can_get_no_contextual_actions(execute):
    response = execute('get_contextual_actions', 'dit:datahub:company')
    contextual_action = response['actions']
    assert response['success']
    assert [] == contextual_action
