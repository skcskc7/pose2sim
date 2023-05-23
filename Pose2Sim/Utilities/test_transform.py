import numpy as np
M = np.identity(4)
tvec = np.array([1,2,3])
R = np.array([[1,0,0],[0,1,0],[0,0,1]])

M[:3,:3] = R
M[:3,3] = tvec

theta = np.pi/2.0
RR = np.array([[np.cos(theta),0,np.sin(theta)],[0,1,0],[-np.sin(theta), 0, np.cos(theta)]])
M2 = np.identity(4)
M2[:3,:3] = RR.T

print(np.dot(M2, M))