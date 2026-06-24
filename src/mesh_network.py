import json
from dataclasses import dataclass
from typing import List

@dataclass
class Node:
    id: int
    name: str

@dataclass
class MeshNetwork:
    nodes: List[Node]

    def add_node(self, node: Node):
        self.nodes.append(node)

    def remove_node(self, node_id: int):
        self.nodes = [node for node in self.nodes if node.id != node_id]

    def get_node(self, node_id: int):
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None

    def monitor_performance(self):
        # Simulate monitoring performance
        return {"nodes": len(self.nodes), "performance": "optimal"}

    def secure_network(self):
        # Simulate securing the network
        return "Network secured"

def create_mesh_network():
    return MeshNetwork([])

def load_mesh_network(data: str):
    mesh_network = MeshNetwork([])
    nodes = json.loads(data)
    for node in nodes:
        mesh_network.add_node(Node(node["id"], node["name"]))
    return mesh_network
