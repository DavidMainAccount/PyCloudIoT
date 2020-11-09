#PYCLOUDIOT : LIBRARY,2,10,checkmask_library.py,
import ulab as np
def check_mask(db, mask=(1, 0, 1)):
    out = np.zeros(db.shape[0],dtype=bool)
    for idx, line in enumerate(db):
        target, vector = line[0], line[1:]
        if (mask == np.bitwise_and(mask, vector)).all():
            if target == 1:
                out[idx] = 1
    return out

#PYCLOUDIOT : MAIN,13,16,checkmask_main.py, #IMPORTS :checkmask_library.py  ;ulab,
n=1000
np.random.seed(0)
db = np.array(np.random.randint(2, size=(n, 4)), dtype=bool)
check_mask(db)