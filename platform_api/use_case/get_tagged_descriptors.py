import requests


class GetTaggedDescriptors:
    def __init__(self, redis_mesh_nodes):
        self.redis_mesh_nodes = redis_mesh_nodes

    def _to_profile(self, node):
        return requests.get(node.href).json()

    def __call__(self, tag):
        nodes = self.redis_mesh_nodes.get_all()

        profiles = [self._to_profile(node) for node in nodes]

        return {
            'success': True,
            'hypermedia': {
                '_links': profiles[0]['hypermedia']['_links'] if len(profiles) > 0 else {}
            },
            'semantics': {
                'alps': {
                    'version': '1.0',
                    'descriptor': profiles[0]['semantics']['alps']['descriptor'] if len(profiles) > 0 else []
                }
            }
        }
