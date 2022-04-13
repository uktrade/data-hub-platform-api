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


def test_can_get_no_contextual_actions(execute):
    response = execute('get_contextual_actions', 'dit:datahub:company')

    assert response['success']
    assert response['alps'] == {
        'version': '1.0',
        'descriptor': []
    }


def test_can_get_one_contextual_action(execute, service_simulator):
    execute('ping_mesh', id_='my-service', href='https://my-service.local/mesh')

    my_service_response = {
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
                        "link": {"href": 'https://my-service.local/mesh'},
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

    response = execute('get_contextual_actions', 'dit:datahub:company')
    assert response['alps']['descriptor'] == [
        {
            "name": "dit:my-service:ReferForHelp",
            "type": "safe",
            "doc": "Refer for Help",
            "tag": "dit:datahub:company",
            "link": {"href": 'https://my-service.local/refer-for-help/#companyId'},
            "descriptor": [
                {
                    "id": "companyId",
                    "name": "dit:datahub:company:id",
                    "type": "semantic",
                }
            ]
        }
    ]
