"""
from each row, choose largest element in a position adjacent to element chosen in previous row.
"""

import doctest
import fileinput

def triangle(input):
    pos, sum = 0, 0
    for j, line in enumerate(input):
        if not j:
            pos, sum = 0, int(line)
            continue
        left, right = [int(e) for i, e in enumerate(line.split()) if i in (pos, pos + 1)]
        sum, pos = (sum + left, pos) if left > right else (sum + right, pos + 1)
    return sum

if __name__ == '__main__':
    # doctest.testmod()
    actual_input = fileinput.input()
    print triangle(actual_input)
