#PYCLOUDIOT : LIBRARY,2,10,compare_library.py,
import ulab as np
def getMinArrayFrom2(a,b):
    return np.minimum(a, b)

def getMaxArrayFrom2(a,b):
    return np.maximum(a, b)

def MaxMinusMin(max,min):
    return max - min

#PYCLOUDIOT : MAIN,13,17,compare_main.py, #IMPORTS :compare_library.py  ;ulab,
import ulab as np
N = 10
a = np.array(range(N), dtype=np.uint8)
b = (N/2) * np.ones(len(a), dtype=np.float)
MaxMinusMin(getMaxArrayFrom2(a,b),getMinArrayFrom2(a,b))