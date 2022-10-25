import math

def hello():
    return "Hello, World!"


def isnear(a,b,tol=1e-9): return abs(a-b)<tol

def fact2(n):
    """https://stackoverflow.com/a/54698884/

    This implementation only works for n >= -1. All other values will return,
    but be nonsense.
    """
    return math.prod(range(n, 0, -2))
