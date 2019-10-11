import sys
import numpy as np
import cv2

class Video:
    #Set the camera size to fit the screen
    def setCamSize(self,camera):
        camera.set(3,self.W)
        camera.set(4,self.H)

    #Initialize the two cameras needed
    def startCam(self):
        self.TL = cv2.VideoCapture(self.TopLeft)
        self.setCamSize(self.TL)
        self.TR = cv2.VideoCapture(self.TopRight)
        self.setCamSize(self.TR)
        self.BL = cv2.VideoCapture(self.BotLeft)
        self.setCamSize(self.BL)
        self.BR = cv2.VideoCapture(self.BotRight)
        self.setCamSize(self.BR)

    def stopCam(self):
        self.TL.release()
        self.TR.release()
        self.BL.release()
        self.BR.release()

    #Initliaze all the necessary variable
    def __init__(self, a, b, c, d):
        self.W = 1280
        self.H = 720
        self.TopLeft = a
        self.TopRight = b
        self.BotLeft = c
        self.BotRight = d
        self.total = 0.69 #0.5,0.69
        self.result = [0,0,0,0]
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.rightf = 1.0
        self.startCam()
        self.capNum = 0
    
    def changesize(self,sign):
        self.total += sign * 0.01

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

    def updateframe(self,storeImage,text,find,motorvalues):
        mv = self.all3(motorvalues)
        a, imgTL = self.TL.read()
        b, imgTR = self.TR.read()
        c,imgBL = self.BL.read()
        d,imgBR = self.BR.read()
        if not a:
            imgTL = cv2.imread("brokenCamera.png", 1)
            self.TL.release()
            self.TL = cv2.VideoCapture(self.TopLeft)
            self.setCamSize(self.TL)
        if not b:
            imgTR = cv2.imread("brokenCamera.png", 1)
            self.TR = cv2.VideoCapture(self.TopRight)
            self.setCamSize(self.TR)
        if not c:
            imgBL = cv2.imread("brokenCamera.png", 1)
            self.BL = cv2.VideoCapture(self.BotLeft)
            self.setCamSize(self.BL)
        if not d:
            imgBR = cv2.imread("brokenCamera.png", 1)
            self.BR = cv2.VideoCapture(self.BotRight)
            self.setCamSize(self.BR)
        tW = self.W * 2
        tH = self.H * 2
        imgL = np.vstack((imgTL, imgBL))
        imgR = np.vstack((imgTR, imgBR))
        img = np.hstack((imgL, imgR))
        if(storeImage == True):
          path = "D:\\distance" + str(self.capNum) + ".jpg"
          cv2.imwrite(path,img)
          self.capNum += 1
          print("Image Captured: {0}".format(str(self.capNum)))
        if (find == True):
          path = "D:\\detect" + str(self.capNum) + ".jpg"
          self.capNum += 1
          cv2.imwrite(path,img)
          t1 = threading.Thread(target = self.imagerec,args = (path))
          t1.start()
        img = cv2.resize(img,(0,0),None,self.total,self.total)
        row,col,height = img.shape
        lineuno = "Temp:" + str(text)
        lineuno += " Lines:" + str(self.result[0])
        lineuno += " Squares:" + str(self.result[1])
        lineuno += " Circle:" + str(self.result[2])
        lineuno += " Triangle:" + str(self.result[3])
        top = "M1:" + str(mv[0]) + " M2:" +  str(mv[1])
        second = "M3:" + str(mv[2]) + " M4:" + str(mv[3])
        third = "M5:" + str(mv[4]) + " M6:" + str(mv[5])
        fourth = "M7:" + str(mv[6]) + " M8:" + str(mv[7])
        linedoe = top + " " + second + " " + third + " " + fourth
        img = cv2.copyMakeBorder(img,0,100,0,0,cv2.BORDER_CONSTANT,value=[0,0,0])
        cv2.putText(img,lineuno,(5,row + 30),self.font,self.rightf,(255,255,255),1,cv2.LINE_AA)
        cv2.putText(img,linedoe,(5,row + 80),self.font,self.rightf,(255,255,255),1,cv2.LINE_AA)
        cv2.imshow('Display', img)

        
    #Shut down all the process after use
    def endDisplay(self):
        print(self.total)
        self.stopCam()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    #1 and 3 are computer 
    test = Video(0,1,2,3)
    done = False
    i = -10
    while(True):
        store = False
        k = cv2.waitKey(1)
        if k & 0xFF == ord('q'):
            break
        if k & 0xFF == ord('s'):
            test.changesize(-1)
        if k & 0xFF == ord('w'):
            test.changesize(1)
        if k & 0xFF == ord('d'):
            store = True
        values = [i for k in range(0,8)]
        test.updateframe(store,"12.34",False,values)
        i += 1
        if(i > 10):
            i = -10
    test.endDisplay()
