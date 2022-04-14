class GetTaggedDescriptors:
    def __init__(self, redis_mesh_nodes):
        self.redis_mesh_nodes = redis_mesh_nodes

    def __call__(self, tag):
        nodes = self.redis_mesh_nodes.get_all()

        descriptors = [{
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
        } for _ in nodes]

        links = {'dit:my-service:ReferForHelp': ({
            'href': 'https://my-service.local/refer/~{companyId}',
            'method': 'get'
        }) for _ in nodes}

        return {
            'success': True,
            'hypermedia': {
                '_links': links
            },
            'semantics': {
                'alps': {
                    'version': '1.0',
                    'descriptor': descriptors
                }
            }
        }
