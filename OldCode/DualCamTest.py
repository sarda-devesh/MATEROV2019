import sys
import numpy as np
import cv2
import threading
import time
class TwoVideo:
    #Set the camera size to fit the screen
    def setCamSize(self,camera):
        camera.set(3,self.W)
        camera.set(4,self.H)

    def getcameravalues(self):
        count = 0
        camnum = 7
        for i in range(0,camnum):
            cap = cv2.VideoCapture(i)
            test,frame = cap.read()
            if(test and count < 4):
                self.cameras[count] = i
        

    #Initialize the two cameras needed
    def startCam(self):
        self.startfirstcamera()
        self.startsecondcamera()

    def startfirstcamera(self):
        self.firstcamera = cv2.VideoCapture(self.first)
        self.setCamSize(self.firstcamera)

    def startsecondcamera(self):
        self.secondcamera = cv2.VideoCapture(self.second)
        self.setCamSize(self.secondcamera)

    def stopCam(self):
        self.firstcamera.release()
        self.secondcamera.release()

    def increase(self,sign):
        self.total += 0.01 * sign
              
    #Initliaze all the necessary variable
    def __init__(self, a, b, c, d):
        self.W = 480
        self.H = 0.75 * self.W
        self.first = a
        self.second = b
        self.firstbackup = c
        self.mini = d
        self.live = True
        self.total = 1.2
        self.back = self.total
        self.result = [0,0,0,0]
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.rightf = 1
        self.startCam()
    
    def changemainsize(self,sign):
        self.total += sign * 0.01
        self.rightf += sign * 0.005

    def changebacksize(self,sign):
        self.back += sign * 0.01

    def flipmini(self):
        self.firstcamera.release()
        temp = self.mini
        self.mini = self.second
        self.second = temp
        self.startfirstcamera()

    def flipfirst(self):
        self.firstcamera.release()
        temp = self.firstbackup
        self.firstbackup = self.first
        self.first = temp
        self.startfirstcamera()

    def changesecond(self):
        self.live = not self.live
        t1 = threading.Thread(target = self.next,args = ())
        t1.start()

    def next(self):
        if not self.live:
            self.takeandsave()
            self.secondcamera.release()
        else:
            self.startsecondcamera()
        time.sleep(5)
            
    def reconnect(self,num):
        if(num == 0):
            self.firstcamera.release()
            self.startfirstcamera()
        else:
            self.secondcamera.release()
            self.startsecondcamera()
        
    def takeandsave(self):
        b,img2 = self.secondcamera.read()
        if not b:
            img2 = cv2.imread("brokenCamera.png", 1)
        img2 = cv2.resize(img2,(0,0),None,self.back,self.back)
        cv2.imshow('Backdisplay',img2)

    def all3(self,motor):
        mv = []
        for i in motor:
            neg = False
            if(i < 0):
                neg = True
                i *= -1
            n = str(i)
            if len(n) < 3:
                for j in range(0,3 - len(n)):
                    n = "0" + n
            if(neg == True):
                n = "-" + n
            else:
                n = "+" + n
            mv.append(n)
        return mv

    def updateframe(self,motor,tempvalue):
        mv = self.all3(motor)
        a, img1 = self.firstcamera.read()
        if not a:
            img1 = cv2.imread("brokenCamera.png", 1)
            self.reconnect(0)
        row1,col1,h1 = img1.shape
        
        if(self.live):
            self.takeandsave()
            
        img = cv2.resize(img1,(0,0),None,self.total,self.total)
        row,col,height = img.shape
        lineuno = "Temp:" + str(tempvalue)
        lineuno += " Lines:" + str(self.result[0])
        lineuno += " Squares:" + str(self.result[1])
        lineuno += " Circle:" + str(self.result[2])
        lineuno += " Triangle:" + str(self.result[3])
        linedoe = ""
        for i in range(0,len(mv)):
            linedoe += "M" + str(i + 1) + ":" + str(mv[i]) + " "
        '''
        top = "M1:" + str(mv[0]) + " M2:" +  str(mv[1])
        second = "M3:" + str(mv[2]) + " M4:" + str(mv[3])
        third = "M5:" + str(mv[4]) + " M6:" + str(mv[5])
        fourth = "M7:" + str(mv[6]) + " M8:" + str(mv[7])
        linedoe = top + " " + second + " " + third + " " + fourth
        '''
        img = cv2.copyMakeBorder(img,0,int(100 * self.rightf),0,0,cv2.BORDER_CONSTANT,value=[0,0,0])
        cv2.putText(img,lineuno,(5,int(row + 30 * self.rightf)),self.font,self.rightf,(255,255,255),1,cv2.LINE_AA)
        cv2.putText(img,linedoe,(5,int(row + 80 * self.rightf)),self.font,self.rightf,(255,255,255),1,cv2.LINE_AA)
        cv2.imshow('Maindisplay', img)

    #Shut down all the process after use
    def endDisplay(self):
        self.stopCam()
        cv2.destroyAllWindows()

#1 and 2 are computer 
test = TwoVideo(0,1,2,3)
done = False
i = -250
while(True):
    k = cv2.waitKey(1)
    sign = 0
    back = 0
    if k & 0xFF == ord('q'):
        break
    if k & 0xFF == ord('a'):
        test.flipfirst()
    if k & 0xFF == ord('f'):
        test.flipmini()
    if k & 0xFF == ord('d'):
        test.changesecond()
    if k & 0xFF == ord('w'):
        sign = 1
    if k & 0xFF == ord('s'):
        sign = -1
    if k & 0xFF == ord('n'):
        back = 1
    if k & 0xFF == ord('m'):
        back = -1   
    x = [i for j in range(0,8)]
    if(sign != 0):
        test.changemainsize(sign)
    if (back != 0):
        test.changebacksize(back)
    test.updateframe(x,"12.34")
    i += 1
    if(i > 250):
        i = -250
test.endDisplay()
