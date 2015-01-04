# https://www.codeeval.com/open_challenges/140/
import fileinput

for line in fileinput.input():
    line = line.strip()
    contents, key = line.split(';')
    contents = contents.split()
    key = [int(k) for k in key.split()]
    n = len(key) + 1
    total = (n * (n + 1)) / 2
    missing = total - sum(key)
    key.append(missing)
    print ' '.join(part for _, part in sorted(zip(key, contents)))
