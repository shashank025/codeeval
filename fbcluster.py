import re
import fileinput

pattern = re.compile('\s+')

edges = set()

def is_tight_with(cluster, node):
    return all((v, node) in edges and (node, v) in edges for v in cluster)

for line in fileinput.input():
    from_u, to_u = pattern.split(line.strip())[-2:]
    edge = (from_u, to_u)
    edges.add(edge)

# print edges

clusters = []
for i, (a, b) in enumerate(edges):
    rev_edge = (b, a)
    if not rev_edge in edges:  # relationship is one way, so move on...
        continue
    # a->b and b->a are both valid,
    # so a and b are eligible to be clustered.

    # initialize clusters when you see the first edge
    new_cluster = False
    if not clusters:
        new_cluster = True

    for cluster in clusters:
        if a in cluster and b in cluster:
            continue
        if a in cluster and b not in cluster:
            if is_tight_with(cluster, b):
                cluster.add(b)
            else:
                new_cluster = True
        elif b in cluster and a not in cluster:
            if is_tight_with(cluster, a):
                cluster.add(a)
            else:
                new_cluster = True
        else: # neither a nor b in any existing clusters
            new_cluster = True
    if new_cluster:
        cluster = set([a, b])
        if not any(cluster.issubset(existing_cluster) for existing_cluster in clusters):
            clusters.append(cluster)
    # print "%(i)s [%(a)s -> %(b)s] %(clusters)s" % locals()

clusters = sorted(', '.join(sorted(cluster)) for cluster in clusters if len(cluster) > 2)
for cluster in clusters:
    print cluster
