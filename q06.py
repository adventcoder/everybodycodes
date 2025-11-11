from ec import main

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

def p3(camp):
    padded = camp * 3
    n = len(camp)
    return count(padded, 0, n) + 998 * count(padded, n, 2*n) + count(padded, 2*n, 3*n)

def count(camp, start, stop):
    count = 0
    for i in range(start, stop):
        c = camp[i]
        if c.islower():
            span = camp[max(i - 1001, 0) : min(i + 1001, len(camp))]
            count += span.count(c.upper())
    return count

if __name__ == '__main__':
    main()
