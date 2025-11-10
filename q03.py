import ec
from collections import Counter

def p1(notes):
    return sum(set(nums(notes)))

def p2(notes):
    return sum(sorted(set(nums(notes)))[:20])

def p3(notes):
    counts = Counter(nums(notes))
    return max(counts.values())

def nums(notes):
    return map(int, notes.split(','))

if __name__ == '__main__':
    ec.main()
