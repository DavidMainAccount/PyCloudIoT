#PYCLOUDIOT : LIBRARY,2,4,smoke_library.py,
import ulab
def smoke(n):
    return ulab.eye(n)

#PYCLOUDIOT : MAIN,7,8,smoke_main.py, #IMPORTS :smoke_library.py  ;ulab,
n = 3
smoke(n)