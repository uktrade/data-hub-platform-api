import requests


class HttpNodeProfile:
    def __init__(self, mesh_nodes_gateway):
        self.mesh_nodes_gateway = mesh_nodes_gateway

    def get_all(self):
        profiles = []
        for node in self.mesh_nodes_gateway.get_all():
            profiles.append(self.to_profile(node))
        return profiles

    def to_profile(self, node):
        return requests.get(node.href).json()
