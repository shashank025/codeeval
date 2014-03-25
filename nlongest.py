"""
return the n longest lines in the input
"""

import doctest
import fileinput
from heapq import heappush, heappop

def top_n(n, input, f):
    """
    n => how many lines from the input do we want?
    f => function that defines the priority/rank of any line in the input

    >>> f = lambda x: len(x)
    >>> top_n(3, ['foo', 'bars', 'spams', 'python', 'several'], f)
    ['spams', 'python', 'several']
    """

    h = []
    for i, line in enumerate(input):
        if not line.rstrip('\r\n'):
            continue
        heappush(h, (f(line), i, line))
        if i >= n:
            heappop(h)
    return (e for _, _, e in h[::-1]) # reverse the order

if __name__ == '__main__':
    # doctest.testmod()
    actual_input = fileinput.input()
    n = int(actual_input.next())
    f = lambda x: len(x)
    for line in top_n(n, actual_input, f):
        print line.strip()
