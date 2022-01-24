import time
import numpy as np
import cv2
import threading
import time
import random

def photo(path):

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read() 
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,1,255,cv2.THRESH_BINARY)
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x,y,w,h = cv2.boundingRect(cnt)
    crop = frame[y:y+h,x:x+w]
    cv2.imwrite(path+str(random.random()*100)+'stand.jpg', crop)
    print("The time is %s" % time.ctime())
    cap.release
    
if __name__ == "__main__":
    photo('stands\\')
