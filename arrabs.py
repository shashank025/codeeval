import fileinput

def sigma(n):
    return (n * (n + 1))/2

for line in fileinput.input():
    n, arr = line.split(';')
    expected = sigma(int(n) - 2)
    actual = sum(int(e) for e in arr.split(','))
    print actual - expected
