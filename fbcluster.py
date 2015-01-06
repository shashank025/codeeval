from collections import defaultdict
import re
import fileinput

pattern = re.compile('\s+')

def find_cliques(g):
    cliques = []
    def bron_kerbosch1(r, p, x):
        """return all maximal cliques in graph g, such that each clique includes:

        all vertices in r,
        some of the vertices in p, and
        and none of the vertices in x.
        """
        if not p and not x and r:
            cliques.append(r)
        for v in p[:]:            # trick: making a copy here
            neighs = g[v]
            bron_kerbosch1(r.union([v]), list(set(p).intersection(neighs)), x.intersection(neighs))
            p.remove(v)
            x = x.union([v])
    bron_kerbosch1(set(), g.keys(), set())
    return cliques

# each edge is of the form (node1, node2)
edges = set()
for line in fileinput.input():
    from_u, to_u = pattern.split(line.strip())[-2:]
    edges.add((from_u, to_u))

# node -> set([neighbor1, neighbor2, ...])
graph = defaultdict(set)
# only strong edges
for a, b in edges:
    if (b, a) in edges:
        graph[a].add(b)
        graph[b].add(a)

scliques = sorted(', '.join(sorted(clique))
                  for clique in find_cliques(graph)
                  if len(clique) > 2)
for clique in scliques:
    print clique
