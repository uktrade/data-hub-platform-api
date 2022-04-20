import requests


class GetTaggedDescriptors:
    def __init__(self, redis_mesh_nodes):
        self.redis_mesh_nodes = redis_mesh_nodes

    def _to_profile(self, node):
        return requests.get(node.href).json()

    def __call__(self, tag):
        nodes = self.redis_mesh_nodes.get_all()

        target_document = {
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
            return target_document

        source_document = self._to_profile(nodes[0])
        for descriptor in source_document['semantics']['alps']['descriptor']:
            if descriptor['tag'] == tag:
                target_document['semantics']['alps']['descriptor'].append(descriptor)
                target_document['hypermedia']['_links'][descriptor['name']] = source_document['hypermedia']['_links'][
                    descriptor['name']]

        return target_document
