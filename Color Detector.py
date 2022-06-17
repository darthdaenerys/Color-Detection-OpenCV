# import modules and libraries
import cv2
import numpy as np

# parameters
width=640
height=360
hl=0
hh=10
sl=0
sh=10
vl=0
vh=10

# Trackbar functions
def HueLow(val):
    global hl
    hl=val
def HueHigh(val):
    global hh
    hh=val
def SatLow(val):
    global sl
    sl=val
def SatHigh(val):
    global sh
    sh=val
def ValLow(val):
    global vl
    vl=val
def ValHigh(val):
    global vh
    vh=val

# camera properties
camera=cv2.VideoCapture(0,cv2.CAP_DSHOW)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
camera.set(cv2.CAP_PROP_FRAME_WIDTH,width)
camera.set(cv2.CAP_PROP_FPS,30)
camera.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

cv2.namedWindow('Trackbar 1')
cv2.resizeWindow('Trackbar 1',320,300)
cv2.createTrackbar('Hue Low','Trackbar 1',0,180,HueLow)
cv2.createTrackbar('Hue High','Trackbar 1',10,180,HueHigh)
cv2.createTrackbar('Sat Low','Trackbar 1',0,255,SatLow)
cv2.createTrackbar('Sat High','Trackbar 1',10,255,SatHigh)
cv2.createTrackbar('Val Low','Trackbar 1',0,255,ValLow)
cv2.createTrackbar('Val High','Trackbar 1',10,255,ValHigh)

# program loop
while True:
    _,frame=camera.read()
    frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lowerbound=np.array([hl,sl,vl])
    upperbound=np.array([hh,sh,vh])
    mymask=cv2.inRange(frameHSV,lowerbound,upperbound)
    myobj=cv2.bitwise_and(frame,frame,mask=mymask)
    cv2.imshow('Object',myobj)
    cv2.imshow('Mask',mymask)
    cv2.imshow('Camera',frame)
    cv2.moveWindow('Mask',0,height-10)
    cv2.moveWindow('Camera',0,0)
    cv2.moveWindow('Object',width,height-10)
    if cv2.waitKey(5) & 0xff==ord('q'):
        break
camera.release()