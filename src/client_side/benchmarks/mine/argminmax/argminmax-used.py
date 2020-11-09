#PYCLOUDIOT : LIBRARY,2,34,argminmax_library.py,
import ulab as np
def permutations(iterable, r=None):
    # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) --> 012 021 102 120 201 210
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = list(range(n))
    cycles = list(range(n, n-r, -1))
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return

def verifyargmax(n):
    for p in permutations(n):
        m1 = np.argmax(p)
        m2 = np.argmax(np.array(p))
        if m1 != m2 or p[m1] != max(p):
            return 0
    return p[m1]

#PYCLOUDIOT : MAIN,37,38,argminmax_main.py, #IMPORTS :argminmax_library.py  ;ulab,
n = (100,200,300,400)
verifyargmax(n)