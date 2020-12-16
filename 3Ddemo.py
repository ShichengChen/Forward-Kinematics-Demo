import matplotlib as mpl
mpl.use('TkAgg')  # or whatever other backend that you want
import cv2
import numpy as np
from utils import *
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import math
from mpl_toolkits.mplot3d import Axes3D


lines=np.array([[0,0,0,1],
                [0,1,0,1],[0,2,0,1],[0,3,0,1],
                [1,1,0,1],[1,2,0,1],[1,3,0,1]]).astype(np.float32)




offsetMatrices=np.array([
    AxisRotationMatrix(0,[0,0,1])@getTransitionMatrix3D(0,0,0),
    AxisRotationMatrix(0,[0,0,1])@getTransitionMatrix3D(0,-1,0),
    AxisRotationMatrix(0,[0,0,1])@getTransitionMatrix3D(0,-2,0),
    AxisRotationMatrix(0,[0,0,1])@getTransitionMatrix3D(0,0,0),
    AxisRotationMatrix(0,[0,0,1])@getTransitionMatrix3D(-1,-1,0),
    AxisRotationMatrix(0,[0,0,1])@getTransitionMatrix3D(-1,-2,0),
])
#offset matrix from world space to object space


B,invB=[],[]
for i in range(offsetMatrices.shape[0]):
    B.append(offsetMatrices[i])
    invB.append(np.linalg.inv(B[-1]))
#print('B',B,invB)
fig = plt.figure(figsize=(14,7.5))
ax = fig.add_subplot(111,projection='3d')
#fig, ax = plt.subplots()
plt.subplots_adjust(left=0.5, bottom=0.1)

def plotline(l):
    cl=l.copy()
    cl[:4,:]=cl[3::-1,:]
    return cl

graph,=ax.plot(plotline(lines)[:,0],plotline(lines)[:,1],plotline(lines)[:,2],marker='o')
maxlen=6
ax.plot([0,0],[0,0],[-maxlen,+maxlen])
ax.plot([-maxlen,maxlen],[0,0],[0,0])
ax.plot([0,0],[-maxlen,+maxlen],[0,0])
ax.set_xlim(-maxlen, maxlen)
ax.set_ylim(-maxlen, maxlen)
ax.set_zlim(-maxlen, maxlen)
ax.set_xticks(np.arange(-maxlen,maxlen+1))
ax.set_yticks(np.arange(-maxlen,maxlen+1))
ax.set_zticks(np.arange(-maxlen,maxlen+1))
ax.text(maxlen, 0, 0, "x")
ax.text(0, maxlen, 0, "y")
ax.text(0, 0, maxlen, "z")
# ax.axhline(y=0, color='k')
# ax.axvline(x=0, color='k')
ax.grid()
#ax.margins(x=0)
#plt.show()

sliders = []
names=[ 'l0 Tx','l0 Ty','l0 Tz','l0 Rx','l0 Ry','l0 Rz',
        'l1 Rx','l1 Rz','l2 Rx','l3 Rx',
        'l4 Rx','l4 Rz', 'l5 Rx', 'l6 Rx',]

params=np.zeros(14)


for idx in range(len(names)):
    ax = plt.axes([0.05, 0.05 + 1/(len(names)+1) * idx, 0.4, 1/(len(names)+2)])
    s = Slider(ax, names[idx], -math.pi*2, math.pi*2,valinit=0)
    sliders.append(s)

def updateGraph(_):
    for idx, s in enumerate(sliders):
        params[idx] = s.val
    r0=getRotationMatrix3D(*(params[3:6]))
    t0=getTransitionMatrix3D(*(params[:3]))
    G=[t0@r0]
    paramsidx=[[6,7],[8],[9],[10,11],[12],[13]]
    Axislist=[[[1,0,0],[0,0,1]],[[1,0,0]],[[1,0,0]],
              [[1,0,0],[0,0,1]],[[1,0,0]],[[1,0,0]]]
    fa=[0,1,2,0,4,5]

    newl=np.zeros_like(lines)
    newl[0] = (G[0] @ lines[0].T).T.copy()

    for i,v0 in enumerate(paramsidx):
        local=np.eye(4).astype(np.float32)
        for j,v1 in enumerate(v0):
            local=local@AxisRotationMatrix(params[v1],Axislist[i][j])
        p=G[fa[i]]
        g=p@invB[i]@local@B[i]
        G.append(g)
        print(G[-1])
        newl[i+1]=g@lines[i+1]

    graph.set_data_3d(plotline(newl)[:,0],plotline(newl)[:,1],plotline(newl)[:,2])

    fig.canvas.draw()

for s in sliders:
    s.on_changed(updateGraph)


plt.show()

