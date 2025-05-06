import asyncio
import random
import time
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, name):
        self.name = name
        self.connections = []

    def connect(self, node):
        self.connections.append(node)
        node.connections.append(self)

class Router(Node):
    pass

class Packet:
    def __init__(self, sender, receiver, size=1):
        self.sender = sender
        self.receiver = receiver
        self.size = size

class TCPProtocol:
    async def send(self, packet):
        delay = random.uniform(0.01, 0.1)
        await asyncio.sleep(delay)
        return random.random() > 0.1

class UDPProtocol:
    async def send(self, packet):
        delay = random.uniform(0.01, 0.1)
        await asyncio.sleep(delay)
        return random.random() > 0.2

async def send_packet(protocol, sender, receiver):
    packet = Packet(sender, receiver)
    print(f"Sending packet from {sender.name} to {receiver.name} using {protocol.__class__.__name__}.")
    start_time = time.time()
    success = await protocol.send(packet)
    end_time = time.time()
    return success, end_time - start_time

async def simulate_network(nodes, protocols, topology_name):
    total_packets = 0
    lost_packets = 0
    times = []

    for node in nodes:
        for connection in node.connections:
            for protocol in protocols:
                success, duration = await send_packet(protocol, node, connection)
                total_packets += 1
                if not success:
                    lost_packets += 1
                times.append(duration)

    avg_time = sum(times) / len(times) if times else 0
    print(f"\nPerformance Metrics for {topology_name} topology:")
    print({"total_packets": total_packets, "lost_packets": lost_packets, "average_time": avg_time})

def visualize_network(nodes, topology_name):
    G = nx.Graph()
    for node in nodes:
        G.add_node(node.name)
        for connection in node.connections:
            G.add_edge(node.name, connection.name)

    plt.figure(figsize=(6, 6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold')
    plt.title(f"{topology_name} Topology")
    plt.show()

def create_hybrid_topology():
    A, B, C, D, E, F, G = Node("A"), Node("B"), Node("C"), Node("D"), Node("E"), Node("F"), Node("G")
    R1, R2 = Router("Router1"), Router("Router2")

    A.connect(R1)
    B.connect(R1)
    R1.connect(R2)
    C.connect(R2)
    D.connect(R2)
    E.connect(R2)
    F.connect(R2)
    G.connect(R2)

    return [A, B, C, D, E, F, G, R1, R2]

def create_mesh_topology():
    nodes = [Node(f"D{i}") for i in range(1, 8)]
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            nodes[i].connect(nodes[j])
    return nodes

async def main():
    hybrid_nodes = create_hybrid_topology()
    mesh_nodes = create_mesh_topology()

    protocols = [TCPProtocol(), UDPProtocol()]
    await simulate_network(hybrid_nodes, protocols, "Hybrid")
    visualize_network(hybrid_nodes, "Hybrid")

    await simulate_network(mesh_nodes, protocols, "Mesh")
    visualize_network(mesh_nodes, "Mesh")

asyncio.run(main())
