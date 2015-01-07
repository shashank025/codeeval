"""Match products to customers to maximize suitability.

https://www.codeeval.com/open_challenges/48/
"""

from itertools import permutations, product, izip
from fractions import gcd
from fileinput import input

ALPHABET  = 'abcdefghijklmnopqrstuvwxyz'
VOWELS     = 'aeiouy'                             # yes, 'y' is a vowel. see defn.
CONSONANTS = set(ALPHABET).difference(VOWELS)

class memoize(object):
    def __init__(self, f):
        self.f = f
        self.cache = {}
    def __call__(self, *args):
        if args not in self.cache:
            self.cache[args] = self.f(*args)
        return self.cache[args]

@memoize
def suit(customer, product):
    """how suited is this customer product pair?

    >>> suit('Ira', 'iPod')
    2
    >>> suit('Ira', 'iPhone')
    3.0
    >>> suit('Ira', 'Apple')
    1
    """

    num_p = len(product)
    num_c = len(customer)
    refer = CONSONANTS if num_p % 2 else VOWELS
    output = sum(1 for c in customer.lower() if c in refer)
    if gcd(num_c, num_p) > 1:
        output *= 1.5
    return output

# 

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    for line in input():
        line = line.strip()
        if not line:
            continue
        customers, products = line.split(';')
        customers = customers.split(',')
        products = products.split(',')
        # what is the suitability for a given p?
        keyfn = lambda e: sum(suit(c, p) for c, p in izip(*e))
        p = max(product(permutations(customers), permutations(products)), key=keyfn)
        print keyfn(p)
