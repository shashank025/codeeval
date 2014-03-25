"""calculate the size of the social network of each word."""

import sys, doctest, Queue, fileinput
from os import environ

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

def debug(msg):
    if 'DEBUG' in environ and environ['DEBUG']:
        print msg

class network(object):
    def __init__(self, words):
        self.wordpos      = dict((word, i) for i, word in enumerate(words))
        self.wordstr      = dict((i, word) for i, word in enumerate(words))
        self.friendcache  = {}    # position -> [set of positions]
        self.closurecache = {}    # position -> [set of positions]

    def friends(self, word):
        member   = lambda w: w in self.wordpos
        splits   = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes  = filter(member, (a + b[1:] for a, b in splits if b))
        replaces = filter(member, (a + c + b[1:] for a, b in splits for c in ALPHABET if b))
        inserts  = filter(member, (a + c + b     for a, b in splits for c in ALPHABET))
        return set(deletes + inserts + replaces)

    def pfriends(self, pos):
        """wrapper around friends that deals with positions instead"""

        if pos not in self.friendcache:
            self.friendcache[pos] = set(self.wordpos[w] for w in self.friends(self.wordstr[pos]))
        return self.friendcache[pos]

    def _closure(self, pos):
        q, output = Queue.Queue(), set([pos])
        q.put(pos)
        while not q.empty():
            for fpos in self.pfriends(q.get()):
                if fpos not in output:
                    output.add(fpos)
                    q.put(fpos)
        output.discard(pos)
        return output

    def closure(self, word):
        """all nodes reachable from word, excluding the word itself.

        >>> input = ['the', 'cat', 'hat', 'then', 'them', 'kilted', 'gilted', 'gifted', 'they', 'their']
        >>> n = network(input)
        >>> sorted(n.wordstr[p] for p in n.closure('the'))
        ['them', 'then', 'they']
        >>> sorted(n.wordstr[p] for p in n.closure('they'))
        ['the', 'them', 'then']
        >>> sorted(n.wordstr[p] for p in n.closure('kilted'))
        ['gifted', 'gilted']
        >>> sorted(n.wordstr[p] for p in n.closure('their'))
        []
        """
        pos = self.wordpos[word]
        return self._closure(pos)

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
    main()
