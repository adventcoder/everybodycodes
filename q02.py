import ec
from dataclasses import dataclass
import multiprocessing as mp

@dataclass(frozen=True)
class Complex:
    x: int
    y: int

    @classmethod
    def parse(cls, s: str):
        return cls(*map(int, s.strip('[]').split(',')))

    def __str__(self):
        return f"[{self.x},{self.y}]"

    def __add__(a, b):
        return Complex(a.x + b.x, a.y + b.y)

    def __mul__(a, b):
        return Complex(a.x*b.x - a.y*b.y, a.x*b.y + a.y*b.x)

    def __truediv__(a, b):
        return Complex(int(a.x / b.x), int(a.y / b.y))

def p1(notes):
    A = Complex.parse(notes.replace('A=', ''))
    r = Complex(0, 0)
    for _ in range(3):
        r = r * r / Complex(10, 10) + A
    return r

def p2(notes):
    A = Complex.parse(notes.replace('A=', ''))
    B = A + Complex(1001, 1001)
    return worker(A, B, 10)

def p3(notes):
    A = Complex.parse(notes.replace('A=', ''))
    B = A + Complex(1001, 1001)
    args = [(A + Complex(x, y), B, 10) for y in range(10) for x in range(10)]
    with mp.Pool() as pool:
        return sum(pool.starmap(worker, args))

def worker(A, B, step):
    count = 0
    for y in range(A.y, B.y, step):
        for x in range(A.x, B.x, step):
            count += check(Complex(x, y))
    return count

def check(p):
    r = Complex(0, 0)
    N = Complex(100_000, 100_000)
    for _ in range(100):
        r = r * r / N + p
        if abs(r.x) > 1_000_000 or abs(r.y) > 1_000_000:
            return False
    return True

if __name__ == "__main__":
    ec.main()
