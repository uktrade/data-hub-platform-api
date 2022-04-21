from platform_api.http_node_profile import HttpNodeProfile
from platform_api.redis_connection import RedisConnection
from platform_api.redis_mesh_nodes import RedisMeshNodes
from platform_api.use_case.get_tagged_descriptors import GetTaggedDescriptors
from platform_api.use_case.get_mesh_nodes import GetMeshNodes
from platform_api.use_case.ping_mesh import PingMesh


class UseCaseNotFoundError(Exception):
    pass


class UseCaseMissingCallDunderMethodError(Exception):
    pass


class UseCaseExecutor:
    def __init__(self):
        self._redis = RedisConnection()
        mesh_nodes_gateway = RedisMeshNodes(self._redis.get_client())
        self.use_cases = {
            'flush_redis_database': lambda: self._redis.get_client().flushdb(),
            'get_tagged_descriptors': GetTaggedDescriptors(HttpNodeProfile(mesh_nodes_gateway)),
            'get_mesh_nodes': GetMeshNodes(mesh_nodes_gateway),
            'ping_mesh': PingMesh(mesh_nodes_gateway),
        }

    def __call__(self, use_case, *args, **kwargs):
        if use_case not in self.use_cases:
            raise UseCaseNotFoundError(f"Use Case {use_case} not found. Check UseCaseExecutor")

        use_case_instance = self.use_cases[use_case]

        if not callable(use_case_instance):
            raise UseCaseMissingCallDunderMethodError(f"Use Case {use_case} missing __call__ method?")

        return use_case_instance(*args, **kwargs)
