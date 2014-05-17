from fileinput import input

# pattern of last digits for numbers obtained when each digit
# in {0, 1, ..., 9} is raised to successively higher powers.
sequence = {
    2: [2, 4, 8, 6],
    3: [3, 9, 7, 1],
    4: [4, 6],
    5: [5],
    6: [6],
    7: [7, 9, 3, 1],
    8: [8, 4, 2, 6],
    9: [9, 1]
    }

for line in input():
    a, n = [int(x) for x in line.split()]
    s = sequence[a]
    l = len(s)
    q, r = divmod(n, l)
    output = dict((i, 0) if i not in s else (i, q) for i in range(10))
    for i in range(r):
        output[s[i]] += 1
    print ', '.join("%s: %s" % (k, v) for k, v in sorted(output.items()))
