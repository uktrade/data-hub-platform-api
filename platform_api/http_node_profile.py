import requests


class HttpNodeProfile:
    def to_profile(self, node):
        return requests.get(node.href).json()
