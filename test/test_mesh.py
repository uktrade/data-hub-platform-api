import pytest

from platform_api.use_case_executor import UseCaseExecutor


@pytest.fixture()
def execute():
    execute = UseCaseExecutor()
    execute('flush_redis_database')
    yield execute


def test_can_get_no_mesh_nodes(execute):
    response = execute('get_mesh_nodes')
    assert response['success']
    assert response['nodes'] == []
