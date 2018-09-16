from typing import Callable, TypeVar

T = TypeVar('T')


class Graph:
    """
    Represents a generic undirected graph
    """

    def __init__(self, nodes: [T], func: Callable[[T, T], int]):
        """
        Generates the graph for a list of node Objects
        :param nodes: a list of nodes, of generic type T
        :param func: a callable function to get the weight between two nodes
        """
        self._adj_mat = {a: {b: func(a, b) for b in nodes[i+1:]} for i, a in enumerate(nodes)}

    def __str__(self) -> str:
        return str(self._adj_mat)

    def get_edges(self) -> [(T, T, int)]:
        """
        Yields the list of (start node, end node, weight) tuples
        :return: a list of tuples of type (T, T, int) representing edge pairs and their weights
        """

        # iterate through each row of the folded adjacency matrix, then through its columns to yield (x, y, val) tuples
        for node_a, adj in self._adj_mat.items():
            for node_b, weight in adj.items():
                yield (node_a, node_b, weight)

    def get_nodes(self) -> [T]:
        """
        Returns the list of nodes held in the graph
        :return: a list of T Object instances, containing adjacency information in this graph
        """
        return list(self._adj_mat.keys())

    def get_node_edges(self, node) -> {T: int}:
        """
        Returns the adjacency for a given node in the graph
        :param node: the T instance in the graph
        :return: adjacency row for this node, given in the form {T: int, ...}
        """

        # TODO: improve this method for getting the edges for a node, seems overkill

        out = {}

        for a, b, w in self.get_edges():

            if a == node:
                out[b] = w
            elif b == node:
                out[a] = w

        return out

    def get_connected_nodes(self) -> [T]:
        """
        Returns the nodes of the graph which have at least one (non-zero weighted) edge to a node
        :return: a list of T Object instances
        """
        return filter(lambda n: sum(self.get_node_edges(n).values()) > 0, self.get_nodes())

    def get_disconnected_nodes(self) -> [T]:
        """
        Returns the nodes of the graph which have no (or, all zero-weighted) edges to other nodes
        :return: a list of T Object instances
        """
        return filter(lambda n: sum(self.get_node_edges(n).values()) == 0, self.get_nodes())

    def minimise(self) -> None:
        """
        Removes disconnected nodes from the Graph
        :return: None, edits the Graph instance that calls the function
        """

        [self.delete_node(d_node) for d_node in self.get_disconnected_nodes()]

    def delete_node(self, d_node: T) -> None:
        """
        Removes a node from the graph, and its associated edges
        :param d_node: the T Object instance to remove from the graph
        :return: None, edits the Graph instance that calls the function
        """

        # TODO: tidy this up, seems like overkill
        if d_node in self.get_nodes():

            del self._adj_mat[d_node]

            for node in [n for n in self._adj_mat if d_node in self._adj_mat[n]]:
                del self._adj_mat[node][d_node]

    def prune_nodes(self, func: Callable[[T], bool]) -> None:
        """
        Edits the nodes present in the search tree according to some deletion function
        :param func: takes a node as a parameter, returning True if it is to be deleted, else False
        :return: None, edits the Graph instance that calls this function
        """

        for n in filter(func, self.get_nodes()):
            self.delete_node(n)

    def prune_edges(self, func: Callable[[T, T, int], int]) -> None:
        """
        Edits the edges in the search tree according to some edit function
        :param func: takes parameters (start node, end node, weight) and returns their new value
        :return: None, edits the Graph instance that calls this function
        """

        for a, b, w in self.get_edges():
            self._adj_mat[a][b] = func(a, b, w)
