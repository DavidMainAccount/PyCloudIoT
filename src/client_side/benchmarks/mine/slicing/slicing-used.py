#PYCLOUDIOT : LIBRARY,2,17,slicing_library.py,
import ulab as np
def sliceArr(N):
    for num in range(1,N):
        for start in range(-num, num+1):
            for end in range(-num, num+1):
                for stride in (-3, -2, -1, 1, 2, 3):
                    l = list(range(num))
                    a = np.array(l, dtype=np.int8)
                    sl = l[start:end:stride]
                    ll = len(sl)
                    try:
                        sa = list(a[start:end:stride])
                    except IndexError as e:
                        sa = str(e)
                    a[start:end:stride] = np.ones(len(sl)) * -1
    return 1

#PYCLOUDIOT : MAIN,20,21,slicing_main.py, #IMPORTS :slicing_library.py  ;ulab,
N = 30
sliceArr(N)