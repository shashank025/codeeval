from itertools import chain, izip_longest
import fileinput

def doit(l):
    foo = filter(None, l)
    return foo if len(foo) < k else reversed(foo)

for line in fileinput.input():
    contents, k = line.split(';')
    contents = contents.split(',')
    k = int(k)
    print ','.join([str(e)
                    for e in chain.from_iterable([doit(e)
                                                  for e in izip_longest(*([iter(contents)] * k))])])
