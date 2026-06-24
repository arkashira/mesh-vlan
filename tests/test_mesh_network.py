from mesh_network import MeshNetwork, Node, create_mesh_network, load_mesh_network

def test_create_mesh_network():
    mesh_network = create_mesh_network()
    assert isinstance(mesh_network, MeshNetwork)
    assert mesh_network.nodes == []

def test_add_node():
    mesh_network = create_mesh_network()
    node = Node(1, "Node 1")
    mesh_network.add_node(node)
    assert len(mesh_network.nodes) == 1
    assert mesh_network.nodes[0].id == 1
    assert mesh_network.nodes[0].name == "Node 1"

def test_remove_node():
    mesh_network = create_mesh_network()
    node1 = Node(1, "Node 1")
    node2 = Node(2, "Node 2")
    mesh_network.add_node(node1)
    mesh_network.add_node(node2)
    mesh_network.remove_node(1)
    assert len(mesh_network.nodes) == 1
    assert mesh_network.nodes[0].id == 2
    assert mesh_network.nodes[0].name == "Node 2"

def test_get_node():
    mesh_network = create_mesh_network()
    node = Node(1, "Node 1")
    mesh_network.add_node(node)
    retrieved_node = mesh_network.get_node(1)
    assert retrieved_node is not None
    assert retrieved_node.id == 1
    assert retrieved_node.name == "Node 1"

def test_monitor_performance():
    mesh_network = create_mesh_network()
    node = Node(1, "Node 1")
    mesh_network.add_node(node)
    performance = mesh_network.monitor_performance()
    assert performance == {"nodes": 1, "performance": "optimal"}

def test_secure_network():
    mesh_network = create_mesh_network()
    security_status = mesh_network.secure_network()
    assert security_status == "Network secured"

def test_load_mesh_network():
    data = '[{"id": 1, "name": "Node 1"}, {"id": 2, "name": "Node 2"}]'
    mesh_network = load_mesh_network(data)
    assert len(mesh_network.nodes) == 2
    assert mesh_network.nodes[0].id == 1
    assert mesh_network.nodes[0].name == "Node 1"
    assert mesh_network.nodes[1].id == 2
    assert mesh_network.nodes[1].name == "Node 2"
