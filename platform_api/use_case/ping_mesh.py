from platform_api.domain.mesh_node import MeshNode


class PingMesh:
    def __init__(self, mesh_nodes_gateway):
        self.mesh_nodes_gateway = mesh_nodes_gateway

    def __call__(self, id_, href):
        self.mesh_nodes_gateway.add(MeshNode(id_, href))
