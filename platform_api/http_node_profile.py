import requests


class HttpNodeProfile:
    def __init__(self, mesh_nodes_gateway):
        self.mesh_nodes_gateway = mesh_nodes_gateway

    def to_profile(self, node):
        return requests.get(node.href).json()
