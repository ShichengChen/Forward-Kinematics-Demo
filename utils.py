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


def getTransitionMatrix3D(x=0,y=0,z=0):
    return np.array([[1, 0,0,x],[0, 1,0,y],[0, 0,1,z],[0,0,0,1]])

def AxisRotationMatrix(angles,rotation_axis):
    ''' rotation matrix from rotation around axis
        see https://en.wikipedia.org/wiki/Rotation_matrix#Axis_and_angle
         [[cos+self.xx*(1-cos), self.xy*(1-cos)-self.z*sin, self.xz*(1-cos)+self.y*sin, 0.0],
          [self.xy*(1-cos)+self.z*sin, cos+self.yy*(1-cos), self.yz*(1-cos)-self.x*sin, 0.0],
          [self.xz*(1-cos)-self.y*sin, self.yz*(1-cos)+self.x*sin, cos+self.zz*(1-cos), 0.0],
          [0.0, 0.0, 0.0, 1.0]]
    '''
    x,y,z=rotation_axis
    xx,xy,xz,yy,yz,zz=x*x,x*y,x*z,y*y,y*z,z*z
    c = np.cos(angles)
    s = np.sin(angles)
    i = 1 - c
    rot_mats=np.eye(4).astype(np.float32)
    rot_mats[0,0] =  xx * i + c
    rot_mats[0,1] =  xy * i -  z * s
    rot_mats[0,2] =  xz * i +  y * s

    rot_mats[1,0] =  xy * i +  z * s
    rot_mats[1,1] =  yy * i + c
    rot_mats[1,2] =  yz * i -  x * s

    rot_mats[2,0] =  xz * i -  y * s
    rot_mats[2,1] =  yz * i +  x * s
    rot_mats[2,2] =  zz * i + c
    rot_mats[3,3]=1
    return rot_mats

def getRotationMatrix3D(thetax,thetay,thetaz):
    rx=AxisRotationMatrix(thetax,[1,0,0])
    ry=AxisRotationMatrix(thetay,[0,1,0])
    rz=AxisRotationMatrix(thetaz,[0,0,1])
    return rx@ry@rz
