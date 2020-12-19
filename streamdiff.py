"""Compute the diff of two streams.

Usage:
    python3 diff.py <stream_a> <stream_b>

For example, if stream_a has the contents:
a
b
c
d

and stream_b has the contents:
a
a
c
e
f

then, the output will be:
 a
-b
+a
 c
-d
+e
+f
"""

import argparse
import doctest

from itertools import chain


def diff(stream_a, stream_b):
    """Compute the diff between two streams.

    A Naive Algorithm:

    A: If stream_a is empty, go to Step E.

    B: Iterate through stream_b (saving elements into a temporary list), until
    either it ends, or a match is found for the current head of stream_a.

    C: If a match is found, yield the saved elements of stream_b as additions,
    then yield the current cursor position from stream_a (having advanced
    through both streams). Go to Step B.

    D: If no match was found, yield the current cursor
    position in stream_a as a deletion (thereby also advancing through
    stream_a). Use the temporary list to rewind stream_b. Go to Step B.

    E: Yield the elements of stream_b as additions.


    >>> ''.join(list(diff(iter('abc'), iter(''))))
    '-a-b-c'
    >>> ''.join(list(diff(iter(''), iter('abc'))))
    '+a+b+c'
    >>> ''.join(list(diff(iter('abc'), iter('xyzacbuvw'))))
    '+x+y+z a+c b-c+u+v+w'
    >>> ''.join(list(diff(iter('abcd'), iter('aace'))))
    ' a-b+a c-d+e'
    >>> ''.join(list(diff(iter('abcdef'), iter('fghxbyzd'))))
    '-a+f+g+h+x b-c+y+z d-e-f'
    """
    for head_a in stream_a:
        toothpaste = []
        found_match = False
        while True:
            try:
                head_b = next(stream_b)
            except StopIteration:
                break
            if head_b == head_a:
                found_match = True
                break
            else:
                toothpaste.append(head_b)
        if found_match:
            for e in toothpaste:
                yield f"+{e}"
            yield f" {head_a}"
        else:
            yield f"-{head_a}"
            stream_b = chain(toothpaste, stream_b)
    for e in stream_b:
        yield f"+{e}"


def main():
    parser = argparse.ArgumentParser(description="Print a Unix style diff")
    parser.add_argument('-t', '--tests',
                        help="Run doc tests",
                        action="store_true")
    parser.add_argument('file_a',
                        nargs='?',
                        help="Old file")
    parser.add_argument('file_b',
                        nargs='?',
                        help="New file")
    args = parser.parse_args()
    if args.tests:
        doctest.testmod(verbose=True)
        return
    if not (args.file_a and args.file_b):
        parser.error("Either specify the --tests flag, or specify both positional args")
    for line in diff(fstream(args.file_a), fstream(args.file_b)):
        print(line)


def fstream(fname):
    for line in open(fname, 'r'):
        yield line.rstrip('\r\n')


if __name__ == '__main__':
    main()
