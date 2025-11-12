from ec import main
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

    names = set()

    def gen(name):
        if len(name) >= min_size:
            names.add(name)
        if len(name) < max_size:
            for c in rules[name[-1]]:
                gen(name + c)

    for prefix in prefixes:
        if len(prefix) <= max_size and check(prefix, rules):
            gen(prefix)

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
