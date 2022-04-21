class DocumentBuilder:
    def __init__(self):
        self._target_descriptors = []
        self._target_links = {}
        self._source_links = {}

    def add_descriptor(self, descriptor):
        self._target_descriptors.append(descriptor)
        self.add_link(descriptor['name'])

    def register_links(self, links):
        self._source_links = links

    def add_link(self, name):
        self._target_links[name] = self._source_links[name]

    def to_document(self):
        return {
            'hypermedia': {
                '_links': self._target_links
            },
            'semantics': {
                'alps': {
                    'version': '1.0',
                    'descriptor': self._target_descriptors
                }
            }
        }


class GetTaggedDescriptors:
    def __init__(self, node_profile_gateway):
        self.node_profile_gateway = node_profile_gateway

    def __call__(self, tag):
        profiles = self.node_profile_gateway.get_all()

        builder = DocumentBuilder()

        if len(profiles) < 1:
            return self._successful(builder.to_document())

        profile = profiles[0]
        for descriptor in profile.get_semantic_descriptors():
            if descriptor['tag'] == tag:
                builder.register_links(profile.get_hypermedia_links())
                builder.add_descriptor(descriptor)

        return self._successful(builder.to_document())

    def _successful(self, document):
        return {'success': True, **document}
