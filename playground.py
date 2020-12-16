import matplotlib as mpl
mpl.use('TkAgg')  # or whatever other backend that you want
import cv2
import numpy as np
from utils import *
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import math
from mpl_toolkits.mplot3d import Axes3D



a=np.array([1,1,0,1])
b=AxisRotMat(3.14/4,[0,0,1])@getTransitionMatrix3D(0,0,0),
invb=np.linalg.inv(b)
lt=AxisRotMat(3.14/2,[1,0,0])
print(invb@lt@b@a)