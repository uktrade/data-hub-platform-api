import requests


class GetTaggedDescriptors:
    def __init__(self, redis_mesh_nodes):
        self.redis_mesh_nodes = redis_mesh_nodes

    def _to_profile(self, node):
        return requests.get(node.href).json()

    def __call__(self, tag):
        nodes = self.redis_mesh_nodes.get_all()

        document = {
            'success': True,
            'hypermedia': {
                '_links': {}
            },
            'semantics': {
                'alps': {
                    'version': '1.0',
                    'descriptor': []
                }
            }
        }

        if len(nodes) < 1:
            return document

        full_profile = self._to_profile(nodes[0])

        if full_profile['semantics']['alps']['descriptor'][0]['tag'] != tag:
            return document

        document['hypermedia']['_links'] = full_profile['hypermedia']['_links']
        document['semantics']['alps']['descriptor'] = full_profile['semantics']['alps']['descriptor']

        return document
