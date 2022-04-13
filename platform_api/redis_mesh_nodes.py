import json

import redis

from platform_api.domain.mesh_node import MeshNode


class RedisMeshNodes:
    def __init__(self, redis_client: redis.Redis):
        self._redis_client = redis_client

    def add(self, node):
        serialised_node = {
            'id': node.id_,
            'href': node.href,
        }
        id_ = f'dit:datahub:mesh:{node.id_}'
        self._redis_client.set(id_, json.dumps(serialised_node))
        self._redis_client.hset('dit:datahub:mesh', node.id_, id_)

    def get_all(self):
        mesh_ids = self._redis_client.hgetall('dit:datahub:mesh').values()
        serialised_nodes = map(json.loads, self._redis_client.mget(mesh_ids))

        return [
            MeshNode(
                id_=serialised_node['id'],
                href=serialised_node['href']
            ) for serialised_node in serialised_nodes
        ]
