from ec import main

def p1(notes):
    names, steps = parse(notes)
    i = 0
    for step in steps:
        i = min(max(i + step, 0), len(names) - 1)
    return names[i]

def p2(notes):
    names, steps = parse(notes)
    i = 0
    for step in steps:
        i = (i + step) % len(names)
    return names[i]

def p3(notes):
    names, steps = parse(notes)
    for step in steps:
        i = step % len(names)
        names[i], names[0] = names[0], names[i]
    return names[0]

def parse(notes):
    names_chunk, steps_chunk = notes.split("\n\n")
    names = names_chunk.split(',')
    steps = [int(s.replace('L', '-').replace('R', '+')) for s in steps_chunk.split(',')]
    return names, steps

if __name__ == "__main__":
    main()
