import cv2
import numpy as np


def getRtMatrix2D(theta,x=0,y=0):
    return np.array([[np.cos(theta), -np.sin(theta),x],
                     [np.sin(theta), np.cos(theta),y],
                     [0,0,1]])
def getTransitionMatrix2D(x=0,y=0):
    return np.array([[1, 0,x],[0, 1,y],[0,0,1]])

def getInhomogeneousLine(lines:np.ndarray):
    l=lines.copy()
    l=l.reshape(-1,l.shape[-1])[:,:-1]
    return l