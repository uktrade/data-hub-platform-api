class MeshNodeProfile:
    def __init__(self, profile):
        self._profile = profile

    def __getitem__(self, item):
        return self._profile[item]