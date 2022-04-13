class GetMeshNodes:
    def __init__(self, mesh_nodes_gateway):
        self.mesh_nodes_gateway = mesh_nodes_gateway

    def __call__(self):
        nodes = [{
            'href': 'https://my-service.local/mesh',
            'id': 'my-service'
        } for _ in self._get_nodes()]

        return {
            'success': True,
            'nodes': nodes,
        }

    def _get_nodes(self):
        return self.mesh_nodes_gateway.get_all().items()
