import click
from ec import main
from collections import defaultdict, Counter
from itertools import pairwise

@click.option('--nails', type=int, default='32')
def p1(notes, nails):
    return sum(2*abs(b - a) == nails for a, b in pairs(notes))

@click.option('--nails', type=int, default='256')
def p2(notes, nails):
    art = Art(nails)
    knots = 0
    for a, b in pairs(notes):
        knots += art.crossings(a, b)
        art.add(a, b)
    return knots

@click.option('--nails', type=int, default='256')
def p3(notes, nails):
    art = Art(nails)
    for a, b in pairs(notes):
        art.add(a, b)
    return max(art.crossings(a, b) for a in range(1, nails + 1) for b in range(a + 1, nails + 1))

def pairs(notes):
    return pairwise(map(int, notes.split(',')))

class Art:
    def __init__(self, nails):
        self.nails = nails
        self.edges = defaultdict(Counter)

    def add(self, a, b):
        self.edges[a][b] += 1
        self.edges[b][a] += 1

    def crossings(self, a, b):
        count = 0
        if a in self.edges and b in self.edges[a]:
            count += self.edges[a][b]
        ends = set(self.between(b, a))
        for start in self.between(a, b):
            for end in self.edges[start]:
                if end in ends:
                    count += self.edges[start][end]
        return count

    def between(self, a, b):
        a = a % self.nails + 1
        while a != b:
            yield a
            a = a % self.nails + 1

if __name__ == '__main__':
    main()
