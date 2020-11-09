#PYCLOUDIOT : LIBRARY,2,5,linalg_library.py,
import numpy as np
from numpy import linalg
def detLinAlg(arrayToOperate):
    return linalg.det(linalg.inv(arrayToOperate))

#PYCLOUDIOT : MAIN,8,9,linalg_main.py, #IMPORTS :linalg_library.py  ;ulab,
N = 10000
print(detLinAlg(np.random.rand(N,N)))