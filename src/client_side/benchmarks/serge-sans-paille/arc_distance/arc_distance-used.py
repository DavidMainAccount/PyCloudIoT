#PYCLOUDIOT : LIBRARY,2,4,arcdistance_library.py,
import ulab as np
def arc_distance(theta_1, phi_1,
                       theta_2, phi_2):
    """
    Calculates the pairwise arc distance between all points in vector a and b.
    """
    temp = np.sin((theta_2-theta_1)/2)**2+np.cos(theta_1)*np.cos(theta_2)*np.sin((phi_2-phi_1)/2)**2
    distance_matrix = 2 * (np.arctan2(np.sqrt(temp),np.sqrt(1-temp)))
    return distance_matrix

#PYCLOUDIOT : MAIN,13,14,arcdistance_main.py, #IMPORTS :arcdistance_library.py  ;ulab,
N = 10000
np.random.seed(0)
t0, p0, t1, p1 = np.random.randn(N), np.random.randn(N), np.random.randn(N), np.random.randn(N)
print(arc_distance(t0, p0, t1, p1))