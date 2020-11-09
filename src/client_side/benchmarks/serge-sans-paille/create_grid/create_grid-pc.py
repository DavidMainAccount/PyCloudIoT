#PYCLOUDIOT : LIBRARY,2,10,creategrid_library.py,
import ulab as np
def create_grid(x):
    N = x.shape[0]
    z = np.zeros((N, N, 3))
    z[:,:,0] = x.reshape(-1,1)
    z[:,:,1] = x
    fast_grid = z.reshape(N*N, 3)
    return fast_grid

#PYCLOUDIOT : MAIN,13,16,creategrid_main.py, #IMPORTS :creategrid_library.py  ;ulab,
N = 800
x = np.arange(0,1,1./N)
create_grid(x)