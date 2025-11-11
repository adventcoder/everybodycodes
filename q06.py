from ec import main
from math import ceil
from collections import Counter
import click

def p1(notes):
    mentors = 0
    count = 0
    for c in notes.strip():
        if c == 'a':
            count += mentors
        elif c == 'A':
            mentors += 1
    return count

def p2(notes):
    mentors = Counter()
    count = 0
    for c in notes.strip():
        if c.islower():
            count += mentors[c.upper()]
        elif c.isupper():
            mentors[c] += 1
    return count

@click.option('--repeat', type=int, default='1000')
@click.option('--distance', type=int, default='1000')
def p3(notes, repeat, distance):
    segment = notes.strip()
    n = ceil(distance / len(segment))

    def get(i):
        return segment[i % len(segment)]

    # initialize the window
    wnd = Counter()
    for i in range(distance):
        wnd[get(i)] += 1

    # left
    lc = 0
    for k in range(n):
        for i, c in enumerate(segment):
            wnd[get(i + distance)] += 1
            if c.islower():
                lc += wnd[c.upper()]
            if i - distance >= -k*len(segment):
                wnd[get(i - distance)] -= 1

    # middle
    mc = 0
    for i, c in enumerate(segment):
        wnd[get(i + distance)] += 1
        if c.islower():
            mc += wnd[c.upper()]
        wnd[get(i - distance)] -= 1

    # right
    rc = 0
    for k in range(n):
        for i, c in enumerate(segment):
            if i + distance < (n-k)*len(segment):
                wnd[get(i + distance)] += 1
            if c.islower():
                rc += wnd[c.upper()]
            wnd[get(i - distance)] -= 1

    return lc + mc*(repeat-2*n) + rc

if __name__ == '__main__':
    main()
