import cv2
import numpy as np
import imutils
import dobot
import serial
from serial.tools import list_ports

port = list_ports.comports()[0].device
d1 = dobot.Dobot(port = port, verbose = True)

i = -42

def dobot(dX,dY):
    d1.movel(dX,dY,-58,r) # z = -40 for cube
    d1.delay(1)
    d1.suck(True)
    d1.delay(0.5)
    d1.movel(205,0,95,r)
    d1.delay(1)
    d1.movel(205,0,95,R)
    d1.delay(1)
    d1.jump(125,-200,i,R) # z = -38 for cube
    d1.delay(1)
    d1.suck(False)
    d1.delay(0.5)
    d1.jump(205,0,95,r)
    d1.delay(3)
    d1.motor(20)
               
x1=191
y1=-104
r = 112
ke = 0

d1.motor(20)
d1.movel(205,0,95,112)
d1.delay(2)

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(15, 10.0)
cap.set(10, -10.0)
cap.set(11, 25.0)
cap.set(13, 13.0)

while True:
    _,frame = cap.read()
    blurred_frame = cv2.GaussianBlur(frame,(5,5),0)
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
    lower_blur = np.array([40,50,20]) 
    upper_blur = np.array([70,255,255])
    mask = cv2.inRange(hsv, lower_blur, upper_blur)

    cv2.imshow("frame",frame)
    cv2.imshow("mask",mask)

    cnts = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        area = cv2.contourArea(c)
        
        if area > 15000:
            print(area)
            d1.delay(2.5)
            d1.motor(0)
            
            angle = cv2.minAreaRect(c)[2]
      
            cv2.drawContours(frame, [c], 0, (0,255,0), 2)
            #print(angle)
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            R = r + angle
            #print("R :", R)
            output_string = " " + str(angle)
            cv2.circle(frame, (cX,cY), 7, (255,255,255), -1)
            #cv2.putText(frame, output_string, (cX-20, cY-20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255), 1)
            cv2.imshow("frame",frame)
            #cv2.waitKey(0)
            dX = x1 + ((480-cY)*0.34)
            dY = y1 + ((640-cX)*0.36)
                
            if ke >= 3:
                dobot(dX,dY)
                i = i + 7
                ke = 0
            ke = ke+1
            print(ke)
            
    k = cv2.waitKey(1)
    if k == 27:
        break

d1.motor(0)
d1.close()
cap.release()
cv2.destroyAllWindows()        