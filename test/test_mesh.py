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


def test_can_get_one_mesh_node(execute):
    execute(
        'ping_mesh',
        id_='my-service',
        href='https://my-service.local/mesh',
    )
    response = execute('get_mesh_nodes')
    assert response['success']
    assert response['nodes'] == [
        {
            'id': 'my-service',
            'href': 'https://my-service.local/mesh',
        }
    ]


def test_can_get_two_mesh_nodes(execute):
    execute(
        'ping_mesh',
        id_='my-service',
        href='https://my-service.local/mesh',
    )
    execute(
        'ping_mesh',
        id_='data-hub',
        href='https://data-hub.local/mesh',
    )
    response = execute('get_mesh_nodes')
    assert response['nodes'] == [
        {
            'id': 'my-service',
            'href': 'https://my-service.local/mesh',
        },
        {
            'id': 'data-hub',
            'href': 'https://data-hub.local/mesh',
        }
    ]
