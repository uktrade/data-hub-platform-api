import pytest
from httpretty import httpretty, HTTPretty

from platform_api.use_case_executor import UseCaseExecutor


@pytest.fixture()
def execute():
    execute = UseCaseExecutor()
    execute('flush_redis_database')
    yield execute


@pytest.fixture()
def service_simulator():
    httpretty.enable(allow_net_connect=False, verbose=True)
    yield None
    httpretty.disable()


def test_can_get_no_tagged_descriptors(execute):
    response = execute('get_tagged_descriptors', 'dit:datahub:company')

    assert response['success']
    assert response['hypermedia']['_links'] == {}
    assert response['semantics']['alps'] == {
        'version': '1.0',
        'descriptor': [],
    }


def test_can_get_one_tagged_descriptor(execute, service_simulator):
    execute('ping_mesh', id_='my-service', href='https://my-service.local/mesh')

    my_service_response = {
        'hypermedia': {
            '_links': {
                'dit:my-service:ReferForHelp': {
                    'href': 'https://my-service.local/refer/~{companyId}',
                    'method': 'get'
                }
            }
        },
        'semantics': {
            "alps": {
                "version": "1.0",
                "id": "dit:my-service",
                "descriptor": [
                    {
                        "name": "dit:my-service:ReferForHelp",
                        "type": "safe",
                        "doc": "Refer for Help",
                        "tag": "dit:datahub:company",
                        "descriptor": [
                            {
                                "id": "companyId",
                                "name": "dit:datahub:company:id",
                                "type": "semantic",
                            }
                        ]
                    }
                ]
            }
        },
    }

    httpretty.register_uri(
        HTTPretty.GET,
        'https://my-service.local/mesh',
        body=my_service_response
    )

    response = execute('get_tagged_descriptors', 'dit:datahub:company')
    assert response['hypermedia']['_links']['dit:my-service:ReferForHelp'] == {
        'href': 'https://my-service.local/refer/~{companyId}',
        'method': 'get'
    }
    assert response['semantics']['alps']['descriptor'] == [
        {
            "name": "dit:my-service:ReferForHelp",
            "type": "safe",
            "doc": "Refer for Help",
            "tag": "dit:datahub:company",
            "descriptor": [
                {
                    "id": "companyId",
                    "name": "dit:datahub:company:id",
                    "type": "semantic",
                }
            ]
        }
    ]
