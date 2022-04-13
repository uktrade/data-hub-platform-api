class GetMeshNodes:
    def __init__(self, mesh_nodes_gateway):
        self.mesh_nodes_gateway = mesh_nodes_gateway

    def __call__(self):
        mesh_nodes = self.mesh_nodes_gateway.get_all()
        nodes = []
        for _ in mesh_nodes.items():
            nodes.append(
                {
                    'href': 'https://my-service.local/mesh',
                    'id': 'my-service'
                }
            )
        return {
            'success': True,
            'nodes': nodes,
        }
