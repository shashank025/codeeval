"""how many grid positions are reachable given the following condition?

starting from (0, 0), how many planar grid positions (x, y) can be reached
in a nieghborly walk that satisfy:

sum(digits(abs(x)) + sum(digits(abs(y))) <= 19?
"""

from os import environ
import Queue

def debug(msg):
    if 'DEBUG' in environ and environ['DEBUG']:
        print msg

class memoize(object):
    def __init__(self, f):
        self.fn = f
        self.fn.__name__ = f.__name__
        self.fn.__doc__ = f.__doc__
        self.cache = {}

    def __call__(self, *args):
        if args not in self.cache:
            self.cache[args] = self.fn(*args)
        return self.cache[args]

@memoize
def neighbors((i, j)): return [(i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)]
@memoize
def csum(d): return sum(int(c) for c in str(abs(d)))

def accessible((x, y)):
    """is this position accessible?

    >>> accessible((0, 0))
    True
    >>> accessible((59, 79))
    False
    >>> accessible((-5, -7))
    True
    """

    xsum = csum(x)
    return xsum <= 19 and (xsum + csum(y)) <= 19

def gridwalk(initial):
    seen = set()       # all positions that have been accessed so far
    q = Queue.Queue()

    def process(node):
        seen.add(node)
        q.put(node)

    process(initial)

    while not q.empty():
        pos = q.get()
        debug("examining position %r; size(seen) = %r; size(q) = %r" % (pos, len(seen), q.qsize()))
        for n in neighbors(pos):
            if n not in seen and accessible(n):
                process(n)
    return len(seen)

if __name__ == '__main__':
    print gridwalk((0, 0))
