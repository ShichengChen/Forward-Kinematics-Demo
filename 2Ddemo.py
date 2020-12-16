import matplotlib as mpl
mpl.use('TkAgg')  # or whatever other backend that you want
import cv2
import numpy as np
from utils import *
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import math

lines=np.array([[[0,0,1],[1,1,1]],
                [[1,1,1],[2,0,1]],
                [[2,0,1],[3,1,1]]])


offsetMatrices=np.array([
    getRtMatrix2D(-3.14/4,0,0)@getRtMatrix2D(0,0,0),
    getRtMatrix2D(3.14/4,0,0)@getRtMatrix2D(0,-1,-1),
    getRtMatrix2D(-3.14/4,0,0)@getRtMatrix2D(0,-2,0),
])
#offset matrix from world space to object space
# offsetMatrices=np.array([
#     getRtMatrix(0,0,0),
#     getRtMatrix(0,-1,-1),
#     getRtMatrix(0,-2,0),
# ])
B,invB=[],[]
for i in range(3):
    B.append(offsetMatrices[i])
    invB.append(np.linalg.inv(B[-1]))
#print('B',B,invB)
degreeOfLines=[0,0,0]
transitionOflines=[0,0]

fig, ax = plt.subplots(figsize=(14,7.5))
plt.subplots_adjust(left=0.5, bottom=0.1)
cl=getInhomogeneousLine(lines)
print(cl,cl[:,0],cl[:,1])
graph,=plt.plot(cl[:,0],cl[:,1],marker='o')
plt.xlim(-8, 8)
plt.ylim(-8, 8)
plt.xticks(np.arange(-8,9))
plt.yticks(np.arange(-8,9))
ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')
ax.grid()
#ax.margins(x=0)
#plt.show()

sliders = []
names=['l0 R','l1 R','l2 R','l0 T x','l0 T y']

for idx in range(5):
    ax = plt.axes([0.05, 0.05 + 1/(len(names)+1) * idx, 0.4, 1/(len(names)+2)])
    s = Slider(ax, names[idx], -math.pi*2, math.pi*2,valinit=0)
    sliders.append(s)

def updateGraph(_):
    for idx, s in enumerate(sliders):
        if(idx<3):degreeOfLines[idx] = s.val
        else:transitionOflines[idx-3]=s.val

    parents=getRtMatrix2D(0,transitionOflines[0],transitionOflines[1])
    G=[]
    newlines=np.zeros(lines.shape)
    for i in range(3):
        #tx,ty=0,0
        #if(i==0):tx,ty=transitionOflines
        Rt=getRtMatrix2D(degreeOfLines[i],0,0)
        parents=parents@invB[i]@Rt@B[i]
        G.append(parents)
        newlines[i]=(parents@lines[i].T).T.copy()

    cl = getInhomogeneousLine(newlines)
    graph.set_data(cl[:,0],cl[:,1])
    fig.canvas.draw()

for s in sliders:
    s.on_changed(updateGraph)


plt.show()