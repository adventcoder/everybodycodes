from ec import main
from collections import Counter
import click

@click.option('--nails', type=int, default='32')
def p1(notes, nails):
    return sum(2*(b-a) == nails for a, b in parse(notes))

@click.option('--nails', type=int, default='256')
def p2(notes, nails):
    edges = Counter()
    knots = 0
    for a, b in parse(notes):
        knots += crossings(edges, a, b, nails)
        edges[(a, b)] += 1
    return knots

@click.option('--nails', type=int, default='256')
def p3(notes, nails):
    edges = Counter(parse(notes))
    most_cuts = 0
    for a in range(1, nails + 1):
        for b in range(a + 1, nails + 1):
            cuts = edges[(a, b)] + crossings(edges, a, b, nails)
            most_cuts = max(cuts, most_cuts)
    return most_cuts

def parse(notes):
    nums = [int(s) for s in notes.split(',')]
    for i in range(len(nums) - 1):
        a, b = nums[i : i + 2]
        yield min(a, b), max(a, b)

def crossings(edges, a, b, nails):
    count = 0
    for (c, d), n in edges.items():
        if (a < c < b < d) or (c < a < d < b):
            count += n
    return count

if __name__ == '__main__':
    main()
