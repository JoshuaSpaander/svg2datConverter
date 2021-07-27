'''
This module slices a line given 2 points M and L in numpy array coordinates. M is the starting point and L is the end point
'''
import numpy as np
#### Line ####
def SliceLine(M,L,Res):    
    #M = np.array([[100, 10]])
    #L = np.array([[200, 10]])
    #NPoints = int(np.sqrt((L[0][0]-M[0][0])**2 + (L[0][1]-M[0][1])**2)/Res)
    Points = M

    for Dot in range(Res):
        Point = M + (L-M)*Dot/Res
        Points = np.vstack((Points,Point))
    
    return Points