from ec import main
from functools import cache
import click

def p1(notes):
    names, rules = parse(notes)
    return next(n for n in names if check(n, rules))

def p2(notes):
    names, rules = parse(notes)
    return sum(i+1 for i, n in enumerate(names) if check(n, rules))

@click.option('--min-size', type=int, default='7')
@click.option('--max-size', type=int, default='11')
def p3(notes, min_size, max_size):
    prefixes, rules = parse(notes)

    @cache
    def suffixes(pc, max_size):
        res = ['']
        if max_size > 0 and pc in rules:
            for c in rules[pc]:
                for s in suffixes(c, max_size - 1):
                    res.append(c + s)
        return res

    names = set()
    for p in prefixes:
        if len(p) <= max_size and check(p, rules):
            for s in suffixes(p[-1], max_size - len(p)):
                if len(p) + len(s) >= min_size:
                    names.add(p + s)

    return len(names)

def check(name, rules):
    for i, c in enumerate(name):
        if i + 1 < len(name) and name[i + 1] not in rules[c]:
            return False
    return True

def parse(notes):
    chunks = notes.split("\n\n")
    names = chunks[0].split(',')

    rules = {}
    for line in chunks[1].splitlines():
        pair = line.split('>')
        rules[pair[0].strip()] = set(pair[1].strip().split(','))
    
    return names, rules

if __name__ == '__main__':
    main()
