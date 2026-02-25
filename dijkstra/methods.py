from typing import Dict, List


class Node:
    def __init__(self, data=None):
        self.data = data


class Edge:
    def __init__(self, node1, node2, cost=1.0, data=None):
        self.data = data
        self.node1: Node = node1
        self.node2: Node = node2
        self.cost: float = cost


class Path:
    def __init__(self, nodes, edges, cost):
        self.nodes: List[Node] = nodes
        self.edges: List[Edge] = edges
        self.cost: float = cost


def extend_path(old_path, edge, node):
    return Path(nodes=old_path.nodes + [node],
                edges=old_path.edges+[edge],
                cost=old_path.cost+edge.cost)


def dijkstra(nodes, edges, start_node, end_node=None, bidirectional=True):

    edges_of_node = dict((n, []) for n in nodes)
    for edge in edges:
        edges_of_node[edge.node1].append((edge, edge.node2))
        if (bidirectional):
            edges_of_node[edge.node2].append((edge, edge.node1))

    reached_nodes: Dict[Node, Path] = {}
    unresolved_reached_nodes: List[Node] = []

    reached_nodes[start_node] = Path(nodes=[start_node], edges=[], cost=0)
    unresolved_reached_nodes.append(start_node)

    def reach_node(node, new_path):
        if node in reached_nodes:
            old_path = reached_nodes[node]
            if (new_path.cost < old_path.cost):
                reached_nodes[node] = new_path
        else:
            reached_nodes[node] = new_path
            unresolved_reached_nodes.append(node)

    def resolve_node(node):
        old_path = reached_nodes[node]
        for edge, next_node in edges_of_node[node]:
            new_path = extend_path(old_path, edge, next_node)
            reach_node(next_node, new_path)

    while len(unresolved_reached_nodes) > 0:
        unresolved_reached_nodes.sort(
            key=lambda node: reached_nodes[node].cost)
        node = unresolved_reached_nodes[0]
        if (node is end_node):
            break
        resolve_node(node)
        unresolved_reached_nodes.remove(node)

    return reached_nodes
