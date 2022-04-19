import pytest
from httpretty import httpretty, HTTPretty

from platform_api.use_case_executor import UseCaseExecutor


class ServiceSimulator:
    def __init__(self, ping_mesh):
        self.ping_mesh = ping_mesh
        self._endpoint = None
        self._id = None

    def simulate(self, id_, endpoint):
        self._endpoint = endpoint
        self._id = id_
        return self

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self._service = None
        self._id = None
        pass

    def register(self, response):
        self.ping_mesh(id_=self._id, href=self._endpoint)
        httpretty.register_uri(
            HTTPretty.GET,
            self._endpoint,
            body=response
        )


@pytest.fixture()
def execute():
    execute = UseCaseExecutor()
    execute('flush_redis_database')
    yield execute


@pytest.fixture()
def simulate(execute):
    httpretty.enable(allow_net_connect=False, verbose=True)
    yield ServiceSimulator(lambda **kwargs: execute('ping_mesh', **kwargs)).simulate
    httpretty.disable()


def test_can_get_no_tagged_descriptors(execute):
    response = execute('get_tagged_descriptors', 'dit:datahub:company')

    assert response['success']
    assert response['hypermedia']['_links'] == {}
    assert response['semantics']['alps'] == {
        'version': '1.0',
        'descriptor': [],
    }


def test_can_get_one_tagged_descriptor(execute, simulate):
    with simulate('my-service', 'https://my-service.local/mesh') as service:
        service.register({
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
        })

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
