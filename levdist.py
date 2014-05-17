"""calculate the size of the social network of each word."""

import sys, doctest, Queue, fileinput
from os import environ

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

def debug(msg):
    if 'DEBUG' in environ and environ['DEBUG']:
        print msg

def friends(word, member):
    """
    >>> dictionary = frozenset(['the', 'cat', 'hat', 'then', 'them', 'kilted', 'gilted', 'gifted', 'they', 'their'])
    >>> member = lambda w: w in dictionary
    >>> sorted(friends('foo', member))
    []
    >>> sorted(friends('the', member))
    ['them', 'then', 'they']
    >>> sorted(friends('hat', member))
    ['cat']
    >>> sorted(friends('kilted', member))
    ['gilted']
    >>> sorted(friends('gilted', member))
    ['gifted', 'kilted']
    >>> sorted(friends('gifted', member))
    ['gilted']
    """
    splits   = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes  = filter(member, (a + b[1:]     for a, b in splits if b))
    replaces = filter(member, (a + c + b[1:] for a, b in splits for c in ALPHABET if b))
    inserts  = filter(member, (a + c + b     for a, b in splits for c in ALPHABET))
    output   = set(deletes + inserts + replaces)
    output.discard(word)
    return output

class network(object):
    """on-demand (lazy) evaluation of closure of each word in specified dictionary"""

    def __init__(self, words):
        self.pos_of_word  = dict((word, i) for i, word in enumerate(words))
        self.word_at_pos  = dict((i, word) for i, word in enumerate(words))
        self.friendcache  = {}    # position -> [set of positions]
        self.closurecache = {}    # position -> [set of positions]
        self.member       = lambda w: w in self.pos_of_word

    def pfriends(self, pos):
        """wrapper around friends that deals with positions instead"""

        if pos not in self.friendcache:
            self.friendcache[pos] = set(self.pos_of_word[w] for w in friends(self.word_at_pos[pos],
                                                                             self.member))
        return self.friendcache[pos]

    def _closure(self, pos):
        q, output = Queue.Queue(), set([pos])
        q.put(pos)
        while not q.empty():
            for fpos in self.pfriends(q.get()):
                if fpos not in output:
                    output.add(fpos)
                    q.put(fpos)
        return output

    def closure(self, word):
        """all nodes reachable from word, excluding the word itself.

        >>> input = ['the', 'cat', 'hat', 'then', 'them', 'kilted', 'gilted', 'gifted', 'they', 'their']
        >>> n = network(input)
        >>> sorted(n.word_at_pos[p] for p in n.closure('the'))
        ['the', 'them', 'then', 'they']
        >>> sorted(n.word_at_pos[p] for p in n.closure('they'))
        ['the', 'them', 'then', 'they']
        >>> sorted(n.word_at_pos[p] for p in n.closure('kilted'))
        ['gifted', 'gilted', 'kilted']
        >>> sorted(n.word_at_pos[p] for p in n.closure('their'))
        ['their']
        """
        pos = self.pos_of_word[word]
        if pos not in self.closurecache:
            computed_closure = self._closure(pos)
            # given a closure c, the closure for every member in c is again c.
            self.closurecache[pos] = computed_closure
            for member in computed_closure:
                self.closurecache[member] = computed_closure
        return self.closurecache[pos]

def main():
    testcases = []
    actual_input = fileinput.input()
    for line in actual_input:
        line = line.strip()
        if line == 'END OF INPUT':
            break
        testcases.append(line.lower())
    n = network([line.strip().lower() for line in actual_input])
    for t in testcases:
        print len(n.closure(t))

if __name__ == '__main__':
    if 'TEST' in environ and environ['TEST']:
        import doctest
        doctest.testmod()
    else:
        main()
