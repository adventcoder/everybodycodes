from ec import main
from collections import Counter

def p1(notes):
    nums = parse(notes)
    return sum(set(nums))

def p2(notes):
    nums = parse(notes)
    return sum(sorted(set(nums))[:20])

def p3(notes):
    nums = parse(notes)
    return max(Counter(nums).values())

def parse(notes):
    return [int(s) for s in notes.split(',')]

if __name__ == '__main__':
    main()
