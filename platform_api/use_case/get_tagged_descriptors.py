import requests


class GetTaggedDescriptors:
    def __init__(self, redis_mesh_nodes):
        self.redis_mesh_nodes = redis_mesh_nodes

    def _to_profile(self, node):
        return requests.get(node.href).json()

    def __call__(self, tag):
        nodes = self.redis_mesh_nodes.get_all()

        class DocumentBuilder:
            def __init__(self):
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
                self.target_document['semantics']['alps']['descriptor'].append(descriptor)

            def register_links(self, links):
                self._links = links

            def add_link(self, name, object):
                target_document['hypermedia']['_links'][name] = self._links[name]

            def to_document(self):
                return self.target_document

        builder = DocumentBuilder()
        target_document = builder.target_document

        if len(nodes) < 1:
            return builder.to_document()

        source_document = self._to_profile(nodes[0])
        for descriptor in source_document['semantics']['alps']['descriptor']:
            if descriptor['tag'] == tag:
                builder.register_links(source_document['hypermedia']['_links'])
                builder.add_descriptor(descriptor)
                builder.add_link(descriptor['name'], source_document['hypermedia']['_links'][
                    descriptor['name']]
                                 )

        return builder.to_document()
