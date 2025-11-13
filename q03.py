from ec import main
from itertools import groupby, islice

def p1(notes):
    sizes = parse(notes)
    return sum(size for size, _ in groupby(sizes))

def p2(notes):
    sizes = parse(notes)
    return sum(size for size, _ in islice(groupby(sizes), 20))

def p3(notes):
    sizes = parse(notes)
    return max(len(list(group)) for _, group in groupby(sizes))

def parse(notes):
    return sorted(map(int, notes.split(',')))

if __name__ == '__main__':
    main()
