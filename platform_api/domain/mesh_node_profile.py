class MeshNodeProfile:
    def __init__(self, profile):
        self._profile = profile

    def __getitem__(self, item):
        return self._profile[item]

    def get_semantic_descriptors(self):
        return self._profile['semantics']['alps']['descriptor']

    def get_hypermedia_links(self):
        return self._profile['hypermedia']['_links']
