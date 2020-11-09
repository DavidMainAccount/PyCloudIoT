#PYCLOUDIOT : LIBRARY,2,4,polyval_library.py,
import ulab as np
def polyfitCalc(array1, array2):
    return np.polyfit(array1, array2, 3)

#PYCLOUDIOT : MAIN,7,10,polyval_main.py, #IMPORTS :polyval_library.py  ;ulab,
N = 10000000
x = np.linspace(-5, 5, num=N)
y = x*x + np.sin(x)*3.0
polyfitCalc(x,y)