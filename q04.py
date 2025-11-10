from ec import main
from math import floor, ceil, prod

def p1(notes):
    lines = notes.splitlines()
    r = int(lines[0]) / int(lines[-1])
    return floor(2025 * r)

def p2(notes):
    lines = notes.splitlines()
    r = int(lines[0]) / int(lines[-1])
    return ceil(10000000000000 / r)

def p3(notes):
    lines = notes.splitlines()
    tails = [int(line.split('|')[-1]) for line in lines[:-1]]
    heads = [int(line.split('|')[0]) for line in lines[1:]]
    r = prod(tails) / prod(heads)
    return floor(100 * r)

if __name__ == '__main__':
    main()
