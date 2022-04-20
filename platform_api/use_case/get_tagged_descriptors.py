import requests


class DocumentBuilder:
    def __init__(self):
        self._descriptors = []
        self._target_links = {}
        self.target_document = {
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

    def add_descriptor(self, descriptor):
        self._descriptors.append(descriptor)
        self.target_document['semantics']['alps']['descriptor'].append(descriptor)
        self.add_link(descriptor['name'])

    def register_links(self, links):
        self._links = links

    def add_link(self, name):
        self._target_links[name] = self._links[name]
        self.target_document['hypermedia']['_links'][name] = self._links[name]

    def to_document(self):
        return {
            'success': True,
            'hypermedia': {
                '_links': self.target_document['hypermedia']['_links']
            },
            'semantics': {
                'alps': {
                    'version': '1.0',
                    'descriptor': self._descriptors
                }
            }
        }


class GetTaggedDescriptors:
    def __init__(self, redis_mesh_nodes):
        self.redis_mesh_nodes = redis_mesh_nodes

    def _to_profile(self, node):
        return requests.get(node.href).json()

    def __call__(self, tag):
        nodes = self.redis_mesh_nodes.get_all()

        builder = DocumentBuilder()

        if len(nodes) < 1:
            return builder.to_document()

        source_document = self._to_profile(nodes[0])
        for descriptor in source_document['semantics']['alps']['descriptor']:
            if descriptor['tag'] == tag:
                builder.register_links(source_document['hypermedia']['_links'])
                builder.add_descriptor(descriptor)

        return builder.to_document()
