#PYCLOUDIOT : LIBRARY,2,4,smoke_library.py,
import numpy as np
def smoke(n):
    return np.eye(n)

#PYCLOUDIOT : MAIN,7,8,smoke_main.py, #IMPORTS :smoke_library.py  ;ulab,
n = 3
smoke(n)