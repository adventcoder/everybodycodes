from ec import main
from collections import Counter
from itertools import pairwise, combinations
import click
import math
from PIL import Image, ImageDraw

def parse(notes):
    return map(int, notes.split(','))

@click.option('--nails', type=int, default='32')
def p1(notes, nails):
    return sum(2*abs(b-a) == nails for a, b in pairwise(parse(notes)))

@click.option('--nails', type=int, default='256')
@click.option('--image-path', type=click.Path())
@click.option('--image-size', type=int, default='5000')
def p2(notes, nails, image_path, image_size):
    knots = 0
    art = StringArt(nails)
    for a, b in pairwise(parse(notes)):
        knots += art.crossings(a, b)
        art.add(a, b)

    if image_path is not None:
        art.save_image(image_size, image_size, image_path)

    return knots

@click.option('--nails', type=int, default='256')
@click.option('--image-path', type=click.Path())
@click.option('--image-size', type=int, default='5000')
def p3(notes, nails, image_path, image_size):
    art = StringArt(nails)
    for a, b in pairwise(parse(notes)):
        art.add(a, b)

    if image_path is not None:
        art.save_image(image_size, image_size, image_path)

    most_cuts = 0
    for a, b in combinations(range(1, nails + 1), 2):
        most_cuts = max(most_cuts, art.crossings(a, b))
    return most_cuts

class StringArt:
    def __init__(self, nails):
        self.nails = nails
        self.edges = Counter()

    def add(self, a, b):
        if a > b:
            a, b = b, a
        self.edges[(a, b)] += 1

    def crossings(self, a, b):
        if a > b:
            a, b = b, a
        count = self.edges[(a, b)]
        for (c, d), n in self.edges.items():
            if (a < c < b < d) or (c < a < d < b):
                count += n
        return count

    def save_image(self, w, h, path):
        img = Image.new('RGB', (w, h), 'white')
        draw = ImageDraw.Draw(img)

        stroke = 10
        pad = stroke / 2
        draw.ellipse((pad, pad, w - pad, h - pad), outline='red', width=stroke)

        angle = 2*math.pi / self.nails
        ox, oy = w/2, h/2
        xs = [ox + (ox - stroke)*math.cos(angle*i) for i in range(self.nails)]
        ys = [oy + (oy - stroke)*math.sin(angle*i) for i in range(self.nails)]

        for a, b in self.edges:
            i = (a - 1) % self.nails
            j = (b - 1) % self.nails
            draw.line((xs[i], ys[i], xs[j], ys[j]), fill='blue', width=1)

        for i in range(self.nails):
            draw.ellipse((xs[i] - stroke, ys[i] - stroke, xs[i] + stroke, ys[i] + stroke), fill='red')

        img.save(path)

if __name__ == '__main__':
    main()
