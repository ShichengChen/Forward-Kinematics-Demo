import cv2
import numpy as np

lines=np.array([[[0,0,1],[1,1,1]],
                [[1,1,1],[2,0,1]],
                [[2,0,1],[3,1,1]]])
def getRtMatrix(theta,x=0,y=0):
    return np.array([[np.cos(theta), -np.sin(theta),x],
                     [np.sin(theta), np.cos(theta),y],
                     [0,0,1]])
def getTransitionMatrix(x=0,y=0):
    return np.array([[1, 0,x],[0, 1,y],[0,0,1]])


#offset matrix from world space to object space
candidate0=getRtMatrix(0)
candidate1=getRtMatrix(3.14/4)
candidate2=getRtMatrix(3.14/2)
# offsetMatrices=np.array([
#     getRtMatrix(-3.14/4,0,0)@getRtMatrix(0,0,0),
#     getRtMatrix(3.14/4,0,0)@getRtMatrix(0,-1,-1),
#     getRtMatrix(-3.14/4,0,0)@getRtMatrix(0,-2,0),
# ])
offsetMatrices=np.array([
    getRtMatrix(0,0,0),
    getRtMatrix(0,-1,-1),
    getRtMatrix(0,-2,0),
])
B,invB=[],[]
for i in range(3):
    B.append(offsetMatrices[i])
    invB.append(np.linalg.inv(B[-1]))
print('B',B,invB)
fa=[-1,0,1]#hierarchical information
degreeOfLines=[0,0,0]
transitionOflines=[0,0]

cv2.namedWindow('Forward Kinematics')
def updateGraph():

    imgsize=[480,640]
    img=np.zeros(imgsize).astype(np.uint8)
    ori = np.array([imgsize[1] // 2, imgsize[0] // 2], dtype=np.int)
    img = cv2.circle(img, tuple((ori).astype(int).tolist()), 4, 255)
    img[imgsize[0] // 2,::3]=255
    img[::3,imgsize[1] // 2]=255
    parents=np.eye(3)
    G=[]
    newlines=np.zeros(lines.shape)
    for i in range(3):
        tx,ty=0,0
        if(i==0):tx,ty=transitionOflines
        Rt=getRtMatrix(degreeOfLines[i],tx,ty)
        parents=parents@invB[i]@Rt@B[i]
        G.append(parents)
        newlines[i]=(parents@lines[i].T).T.copy()

        newlines[i,:,1]*=-1#y coordinate bigger, lower in image, so change to minus
        img=cv2.line(img,tuple((ori+newlines[i][0][:2]*20).astype(int).tolist()),
                         tuple((ori+newlines[i][1][:2]*20).astype(int).tolist()),255)
        img=cv2.circle(img,tuple((ori+newlines[i][0][:2]*20).astype(int).tolist()),3,255)
        img=cv2.circle(img,tuple((ori+newlines[i][1][:2]*20).astype(int).tolist()),3,255)
    cv2.imshow('Forward Kinematics',img)
    cv2.waitKey(1)




updateGraph()


def on_trackbar0(theta0):
    degreeOfLines[0]=theta0/10
    updateGraph()
def on_trackbar1(theta1):
    degreeOfLines[1]=theta1/10
    updateGraph()
def on_trackbar2(theta2):
    degreeOfLines[2]=theta2/10
    updateGraph()
def on_trackbar3(theta1):
    transitionOflines[0]=theta1-20
    updateGraph()
def on_trackbar4(theta2):
    transitionOflines[1]=-(theta2-20)
    updateGraph()

cv2.createTrackbar("line0 rotation", "Forward Kinematics", 0, 2*30, on_trackbar0)
cv2.createTrackbar("line1 rotation", "Forward Kinematics", 0, 2*30, on_trackbar1)
cv2.createTrackbar("line2 rotation", "Forward Kinematics", 0, 2*30, on_trackbar2)
cv2.createTrackbar("line0 transition x", "Forward Kinematics", 20, 2*20, on_trackbar3)
cv2.createTrackbar("line0 transition y", "Forward Kinematics", 20, 2*20, on_trackbar4)

while(1):
    q=cv2.waitKey(1)
    if(q==ord('q')):break