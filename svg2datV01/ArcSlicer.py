'''
This module slices an arc as a cricle by the given resolution (note not an ellipse, as this feature is pending) 
starting at point M and ending at point A. It follows the svg format rules for arc formatting.
'''
import numpy as np

#### Rotation Matrix ####
def T_rot(Gamma):
    return np.array([[np.cos(Gamma),-np.sin(Gamma)],[np.sin(Gamma),np.cos(Gamma)]])

#### Arc Slicing####
def SliceArc(M,rx,ry,phi,BigCircleFlag,FlipFlag,A,Res):
    a = max(rx,ry)
    b = a#min(rx,ry)
    
    rMA = A-M
    magrMA = np.sqrt(rMA[0][0]**2+rMA[0][1]**2)
    if a < magrMA or b < magrMA:
        a = magrMA
        b = magrMA

    magrMC = a
    theta = 2*np.arcsin(magrMA/(2*magrMC))

    if BigCircleFlag == 1:
        theta = 2*np.pi-theta

    if FlipFlag == 1:
        theta = -theta

    rMC = (1/(2*np.cos((np.pi-theta)/2)))*np.matmul(rMA,T_rot((np.pi-theta)/2))
    C = M+rMC
    rCM = -rMC

    Points = M
    for increment in range(Res):
        Point = C+np.matmul(rCM,T_rot(theta*increment/Res))
        Points = np.vstack((Points,Point))
    
    return Points