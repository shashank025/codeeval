"""how many of the possible sub expressions of a number are ugly?"""

import sys
from os import environ
import fileinput

def debug(msg):
    if 'DEBUG' in environ and environ['DEBUG']:
        print ">>>>", msg
        sys.stdout.flush()

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

# str -> int
@memoize
def xeval(sexpr):
    """
    >>> xeval('')
    0
    >>> xeval('1234567')
    1234567
    >>> xeval('+1234567')
    1234567
    >>> xeval('-1234567')
    -1234567
    >>> xeval('2+3')
    5
    >>> xeval('2-3')
    -1
    >>> xeval('2-23+4')
    -17
    >>> xeval('2-01+3-1')
    3
    >>> xeval('1-2-3-4-5')
    -13
    """
    if not sexpr:
        return 0
    size = len(sexpr)
    start = 0
    curr = 1 if sexpr[0] == '+' or sexpr[0] == '-' else 0
    while curr < size and sexpr[curr] != '+' and sexpr[curr] != '-':
        curr += 1
    this = int(sexpr[start:curr])
    if curr >= size - 1:
        return this
    return this + xeval(sexpr[curr:])

# str -> list of strs
@memoize
def subexprs(s):
    """return all sub expressions of this number.

    >>> subexprs('3')
    ['3']
    >>> subexprs('23')
    ['23', '2+3', '2-3']
    >>> subexprs('011')
    ['011', '0+11', '0-11', '01+1', '0+1+1', '0-1+1', '01-1', '0+1-1', '0-1-1']
    """
    if s and not s[1:]:
        return [s]
    return [s[0] + sep + p for p in subexprs(s[1:]) for sep in ('', '+', '-')]

@memoize
def ugly(n):
    """if number is 0, or number is divisible by one of 2, 3, 5 or 7.

    >>> ugly(0)     # by definition
    True
    >>> ugly(4)
    True
    >>> ugly(13)
    False
    >>> ugly(39)
    True
    >>> ugly(121)
    False
    >>> ugly(-14)
    True
    >>> ugly(-39)
    True
    """

    return not n or not(n % 2) or not(n % 3) or not(n % 5) or not(n % 7)

def ugly_count(n):
    """

    >>> ugly_count('0')
    1
    >>> ugly_count('1')
    0
    >>> ugly_count('9')
    1
    >>> ugly_count('011')
    6
    >>> ugly_count('12345')
    64
    """
    return sum(ugly(xeval(s)) for s in subexprs(n))

if __name__ == '__main__':
    for line in fileinput.input():
        print ugly_count(line.strip())
