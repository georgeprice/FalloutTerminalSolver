from fts.helpers.graph import Graph
from fts.helpers.string import matching_characters

x = Graph([1, 2, 3, 4], lambda a, b: 1 if a < 4 and b < 4 else 0)
print(x)
print(x.get_nodes())
for e in x.get_edges():
    print(e)
for n in x.get_connected_nodes():
    print(n)


y = Graph(['dog', 'lag', 'bag', 'con', 'cod'], matching_characters)
print(y)
y.prune_edges(lambda a, b, w: 0 if (a == 'dog' or b == 'dog' or w < 2) else 1)
print(y)
y.prune_edges(lambda a, b, w: matching_characters(a, b) if (w > 0) else 0)
print(y)
for d_n in y.get_disconnected_nodes():
    print(d_n)
y.minimise()
print(y)
