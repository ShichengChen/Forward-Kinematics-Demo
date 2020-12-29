import matplotlib as mpl
mpl.use('TkAgg')  # or whatever other backend that you want
import cv2
import numpy as np
from utils import *
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import math

lines=np.array([[0,0,1],
                [1,0,1],
                [3,0,1],
                [3.5,0,1]])



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

    parents=getRtMatrix2D(degreeOfLines[0],lines[0,0],lines[0,1])
    G=[parents]
    newlines=np.zeros(lines.shape)
    newlines[1]=parents@lines[1]
    for i in range(1,3):
        t=lines[i]-lines[i-1]
        t1=lines[i+1]-lines[i]
        t1[-1]=1
        Rt=getRtMatrix2D(degreeOfLines[i],t[0],t[1])
        G.append(G[-1] @ Rt)
        newlines[i+1]=G[-1]@t1

    print(newlines)

    cl = getInhomogeneousLine(newlines)
    graph.set_data(cl[:,0],cl[:,1])
    fig.canvas.draw()

for s in sliders:
    s.on_changed(updateGraph)


plt.show()