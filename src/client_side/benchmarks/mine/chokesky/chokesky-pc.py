#PYCLOUDIOT : LIBRARY,2,18,chokesky_library.py,
import numpy as np
from numpy import linalg
def getLinAlg(arrayToCalc):
    try: 
        a = linalg.cholesky(arrayToCalc)
        return a
    except:
        return "Matrix is not positive definite"

def countPositiveDefinite(N):
    count = 0
    for p in (0,N):
        a = np.random.rand(2,2)
        print(getLinAlg(a))
        if(type(getLinAlg(a)) != str):
            count = count + 1
    return count

#PYCLOUDIOT : MAIN,21,22,chokesky_main.py, #IMPORTS :chokesky_library.py  ;ulab,
N = 2
countPositiveDefinite(N)


# si no existe ulab.random.rand
# b = ulab.array([[0.54548 , 0.88647], [0.254464, 0.545]]) 
# print(b)
# print(getLinAlg(b))
