import cv2
import numpy as np
import pickle

width=640
height=360

with open('Tracking2ObjData.pkl','rb') as f:
    hl1=pickle.load(f)
    hh1=pickle.load(f)
    hl2=pickle.load(f)
    hh2=pickle.load(f)
    sl=pickle.load(f)
    sh=pickle.load(f)
    vl=pickle.load(f)
    vh=pickle.load(f)
    f.close()

def HueLow1(val):
    global hl1
    hl1=val
def HueHigh1(val):
    global hh1
    hh1=val
def HueLow2(val):
    global hl2
    hl2=val
def HueHigh2(val):
    global hh2
    hh2=val
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

camera=cv2.VideoCapture(0,cv2.CAP_DSHOW)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
camera.set(cv2.CAP_PROP_FRAME_WIDTH,width)
camera.set(cv2.CAP_PROP_FPS,30)
camera.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

cv2.namedWindow('Trackbar 1')
cv2.namedWindow('Trackbar 2')

cv2.createTrackbar('Hue Low 1','Trackbar 1',hl1,180,HueLow1)
cv2.createTrackbar('Hue High 1','Trackbar 1',hh1,180,HueHigh1)
cv2.createTrackbar('Hue Low 2','Trackbar 1',hl2,180,HueLow2)
cv2.createTrackbar('Hue High 2','Trackbar 1',hh2,180,HueHigh2)
cv2.createTrackbar('Sat Low','Trackbar 2',sl,255,SatLow)
cv2.createTrackbar('Sat High','Trackbar 2',sh,255,SatHigh)
cv2.createTrackbar('Val Low','Trackbar 2',vl,255,ValLow)
cv2.createTrackbar('Val High','Trackbar 2',vh,255,ValHigh)

while True:
    _,frame=camera.read()
    frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    lb1=np.array([hl1,sl,vl])
    lb2=np.array([hl2,sl,vl])
    ub1=np.array([hh1,sh,vh])
    ub2=np.array([hh2,sh,vh])

    mask1=cv2.inRange(frameHSV,lb1,ub1)
    mask2=cv2.inRange(frameHSV,lb2,ub2)
    mask3=cv2.bitwise_or(mask1,mask2)
    
    cntrs,_=cv2.findContours(mask3,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(frame,cntrs,-1,(0,255,0),2)
    for c in cntrs:
        if cv2.contourArea(c)>=150:
            cv2.drawContours(frame,[c],0,(0,255,0),2)
            x,y,w,h=cv2.boundingRect(c)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

    cv2.imshow('Color Tracking',frame)
    cv2.imshow('Mask Region',mask3)
    cv2.moveWindow('Mask Region',0,height)
    cv2.moveWindow('Color Tracking',0,0)

    if cv2.waitKey(5) & 0xff==ord('q'):
        with open('Tracking2ObjData.pkl','wb') as f:
            hl1=pickle.dump(hl1,f)
            hh1=pickle.dump(hh1,f)
            hl2=pickle.dump(hl2,f)
            hh2=pickle.dump(hh2,f)
            sl=pickle.dump(sl,f)
            sh=pickle.dump(sh,f)
            vl=pickle.dump(vl,f)
            vh=pickle.dump(vh,f)
            f.close()
        break
camera.release()