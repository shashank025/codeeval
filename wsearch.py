"""find if a word exists in a grid"""

def occurs(board, c):
    """find all occurrences of char c in 2-d array board"""

    for i, row in enumerate(board):
        for j, p in enumerate(row):
            if c == p:
                yield (i, j)

def neighbors(board, (i, j)):
    """return all valid neighboring positions

    try: (i, j + 1), (i, j - 1), (i + 1, j) and (i - 1, j)
    """
    max_i = len(board) - 1
    max_j = len(board[0]) - 1
    # try (i, j + 1)
    if j + 1 <= max_j:
        yield (i, j + 1)
    if j - 1 >= 0:
        yield (i, j - 1)
    if i + 1 <= max_i:
        yield (i + 1, j)
    if i - 1 >= 0:
        yield (i - 1, j)

def match(board, path, suffix, (i, j)):
    """match suffix by walking neighbor-tree starting at (i, j))"""

    if not suffix:
        return (True, path)
    for (n_i, n_j) in neighbors(board, (i, j)):
        if (n_i, n_j) in path:
            # dont walk back over current path
            # print ">>>> ignoring neighbor %s, since its already on current path" % ((n_i, n_j),)
            continue
        # print ">>>> checking if neighbor %s matches suffix %s ..." % ((n_i, n_j), suffix[0])
        if board[n_i][n_j] == suffix[0]:
            # print ">>>>    yes!"
            path = set(list(path) + [(n_i, n_j)])
            return match(board, path, suffix[1:], (n_i, n_j))
    return (False, path)

def word_in_grid(board, word):
    """
    >>> board = ['abce', 'sfcs', 'adee']
    >>> found, path = word_in_grid(board, 'ASADB')
    >>> found
    False
    >>> path
    []
    >>> found, path = word_in_grid(board, 'ABCCED')
    >>> found
    True
    >>> sorted(path)
    [(0, 0), (0, 1), (0, 2), (1, 2), (2, 1), (2, 2)]
    """
    word = word.lower()
    c = word[0]
    # print ">>>> board: %s" % (board,)
    for pos in occurs(board, c):
        # print ">>>> char %s occurs in position %s on board; matching suffix ..." % (c, pos)
        found, path = match(board, set([pos]), word[1:], pos)
        if found:
            return (True, path)
    return (False, [])

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import fileinput
    board = ['abce', 'sfcs', 'adee']
    for line in fileinput.input():
        found, path = word_in_grid(board, line.strip())
        print found
