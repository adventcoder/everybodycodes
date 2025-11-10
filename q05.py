from ec import main

def p1(notes):
    _, bone = parse(notes)
    return quality(bone)

def p2(notes):
    qualities = []
    for line in notes.splitlines():
        _, bone = parse(line)
        qualities.append(quality(bone))
    return max(qualities) - min(qualities)

def p3(notes):
    pairs = []
    for line in notes.splitlines():
        id, bone = parse(line)
        pairs.append((score(bone), id))
    pairs.sort(reverse=True)
    return sum(id * (i+1) for i, (_, id) in enumerate(pairs))

def score(bone):
    score = [quality(bone)]
    for seg in bone:
        score.append(int(''.join(str(n) for n in seg if n is not None)))
    return score

def quality(bone):
    return int(''.join(str(seg[1]) for seg in bone))

def parse(line):
    pair = line.split(':')
    id = int(pair[0])
    bone = []
    for num in map(int, pair[1].split(',')):
        for seg in bone:
            if num < seg[1] and seg[0] is None:
                seg[0] = num
                break
            elif num > seg[1] and seg[2] is None:
                seg[2] = num
                break                
        else:
            bone.append([None, num, None])
    return id, bone

if __name__ == '__main__':
    main()
