from os import environ

def debug(msg):
    if 'DEBUG' in environ and environ['DEBUG']:
        print msg

def neighbors((min_i, min_j), (max_i, max_j), (i, j)):
    """return all valid neighbors for (i, j) on board defined by given extremities.

    XXX for optimization, the output of this function can be memoized.

    order: (i, j + 1), (i, j - 1), (i + 1, j) and (i - 1, j)

    >>> [n for n in neighbors((0, 0), (0, 0), (0, 0))]
    []
    >>> [n for n in neighbors((0, 0), (1, 1), (0, 0))]
    [(0, 1), (1, 0)]
    >>> [n for n in neighbors((0, 0), (3, 3), (1, 2))]
    [(1, 3), (1, 1), (2, 2), (0, 2)]
    """
    if j + 1 <= max_j:
        yield (i, j + 1)
    if j - 1 >= min_j:
        yield (i, j - 1)
    if i + 1 <= max_i:
        yield (i + 1, j)
    if i - 1 >= min_i:
        yield (i - 1, j)

def mkpath(path, pos):
    path = list(path)
    path.append(pos)
    return set(path)

def count_paths((min_i, min_j), (max_i, max_j)):
    """how many paths from top left to bottom right on specified board?

    >>> count_paths((0, 0), (0, 0))
    0
    >>> count_paths((0, 0), (0, 2))
    1
    >>> count_paths((0, 0), (0, 5))
    1
    >>> count_paths((0, 0), (1, 1))
    2
    >>> count_paths((0, 0), (1, 2))
    4
    >>> count_paths((0, 0), (2, 2))
    12
    >>> count_paths((0, 0), (3, 3))
    184
    """

    def explore((i, j), path):
        found = 0
        for (x, y) in neighbors((min_i, min_j), (max_i, max_j), (i, j)):
            if (x, y) == (max_i, max_j):
                found += 1
                debug("neighbor %r of node %r on path %r is a goal node: +1" % ((x, y), (i, j), path))
            elif (x, y) in path: 
                debug("neighbor %r of node %r already on path %r; ignoring..." % ((x, y), (i, j), path))
                continue
            else:
                debug("neighbor %r of node %r not already on path %r; exploring ..." % ((x, y), (i, j), path))
                found += explore((x, y), mkpath(path, (x, y)))
        return found
    return explore((0, 0), set([(0, 0)]))

if __name__ == '__main__':
    print count_paths((0, 0), (3, 3))
