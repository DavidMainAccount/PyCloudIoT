#PYCLOUDIOT : LIBRARY,2,4,operators_library.py,
import ulab as np
def matrixtimesmatrix(arrayToMultiply):
    return arrayToMultiply*arrayToMultiply

#PYCLOUDIOT : MAIN,7,8,operators_main.py, #IMPORTS :operators_library.py  ;ulab,
N = 10
a = np.ones(N)
matrixtimesmatrix(a)