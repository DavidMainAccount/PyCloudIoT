#PYCLOUDIOT : LIBRARY,2,6,cron_library.py,
def cronbach(itemscores):
    itemvars = itemscores.var(axis=1, ddof=1)
    tscores = itemscores.sum(axis=0)
    nitems = len(itemscores)
    return nitems / (nitems-1) * (1 - itemvars.sum() / tscores.var(ddof=1))

#PYCLOUDIOT : MAIN,9,13,cron_main.py, #IMPORTS :cron_library.py  ;ulab,
import numpy as np
np.random.seed(0)
N = 600
items = np.random.rand(N,N)
print(cronbach(items))