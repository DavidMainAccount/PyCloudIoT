#PYCLOUDIOT : LIBRARY,2,4,polyfit_library.py,
import ulab as np
def polyvalCalc(array1, array2):
    return np.polyval(array1, array2)

#PYCLOUDIOT : MAIN,7,10,polyfit_main.py, #IMPORTS :polyfit_library.py  ;ulab,
N = 1000
x = np.linspace(0, 10, num=N)
p = [1, 2, 3,4]
polyvalCalc(x,p)