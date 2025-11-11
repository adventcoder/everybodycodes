from ec import main
from math import ceil
import click

def p1(camp):
    count = 0
    for i, c in enumerate(camp):
        if c == 'a':
            count += camp[:i].count(c.upper())
    return count

def p2(camp):
    count = 0
    for i, c in enumerate(camp):
        if c.islower():
            count += camp[:i].count(c.upper())
    return count

@click.option('--reps', type=int, default='1000')
@click.option('--distance', type=int, default='1000')
def p3(camp, reps, distance):
    pad = camp * ceil(distance / len(camp))
    lcount = count('', camp, pad, distance)
    mcount = count(pad, camp, pad, distance)
    rcount = count(pad, camp, '', distance)
    return lcount + (reps - 2) * mcount + rcount

def count(lpad, camp, rpad, distance):
    padded = lpad + camp + rpad
    count = 0
    for i, c in enumerate(camp):
        if c.islower():
            start = max(len(lpad) + i - distance, 0)
            stop  = min(len(lpad) + i + distance + 1, len(padded))
            count += padded[start : stop].count(c.upper())
    return count

if __name__ == '__main__':
    main()
