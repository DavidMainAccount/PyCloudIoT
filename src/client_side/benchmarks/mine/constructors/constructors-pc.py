#PYCLOUDIOT : LIBRARY,2,4,constructors_library.py,
import numpy as np
def generateLinSpace(N):
    return np.linspace(0, N, N)

#PYCLOUDIOT : MAIN,7,9,constructors_main.py, #IMPORTS :constructors_library.py  ;ulab,
import numpy as np
N = 10000000
generateLinSpace(N)