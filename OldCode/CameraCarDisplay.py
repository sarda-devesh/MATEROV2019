import sys
import numpy as np
import cv2
import threading
#from object_detection.objectdetection_image import Detect

class Video:

   #Set the camera size to fit the screen
   def setcamerasize(self,camera):
      camera.set(3,1080)
      camera.set(4,720)

   #Initialize the two cameras needed
   def setcameras(self):
      self.cap = cv2.VideoCapture(self.frontCam)
      self.setcamerasize(self.cap)
      self.cop = cv2.VideoCapture(self.rearCam)
      self.setcamerasize(self.cop)
      self.clawcam = cv2.VideoCapture(self.claw)
      self.setcamerasize(self.clawcam)
      
   #Initliaze all the necessary variable
   def __init__(self,a,b,c,d):
      self.frontCam = a
      self.rearCam = b
      self.claw = c
      self.otherclaw = d
      self.setcameras()
      self.capNum = 0
      self.rf = 0.5
      self.sc = 0.5 * self.rf
      self.clawfac = self.rf * 0.75
      self.leftf = 0.4
      self.rightf = 0.4 
      self.total = 1.1
      self.font = cv2.FONT_HERSHEY_SIMPLEX
      #self.ir = Detect()
      self.result = [0,0,0,0]

   def changerearsize(self,sign):
      self.sc += sign * 0.01


   def changesize(self,sign):
      self.total += sign * 0.01

   def flipcameras(self):
      temp = self.frontCam
      self.frontCam = self.rearCam
      self.rearCam = temp
      temp = self.claw
      self.claw = self.otherclaw
      self.otherclaw = temp
      self.setcameras()

   def rotateimage(self,image):
      rows,cols,channels = image.shape
      M = cv2.getRotationMatrix2D((cols/2,rows/2),180,1)
      return cv2.warpAffine(image,M,(cols,rows))

   def updateframe(self,storeImage,text,find,mv):
       # Capture frame-by-frame
       met, img1 = self.cap.read()
       if(storeImage == True):
          path = "C:\\distance" + str(self.capNum) + ".jpg"
          cv2.imwrite(path,img1)
          self.capNum += 1
       if (find == True):
          path = "detect" + str(self.capNum) + ".jpg"
          self.capNum += 1
          cv2.imwrite(path,img1)
          t1 = threading.Thread(target = self.imagerec,args = (path))
          t1.start()
       mot, img2 = self.cop.read()
       # Resize input image to fit screen
       img1 = cv2.resize(img1, (0, 0), None,self.rf,self.rf)
       img2 = cv2.resize(img2, (0, 0), None,self.sc,self.sc)
       row1,col1,h1 = img1.shape
       row2,col2,h2 = img2.shape
       border = int((col1 - col2)/2)
       img2 = cv2.copyMakeBorder(img2,0,0,border,col1-border-col2,cv2.BORDER_CONSTANT,value=[0,0,0])
       img1 = np.concatenate((img2,img1),axis = 0)
       left = int(border + col2)
       #Add the text to the image
       row1,col1,h1 = img1.shape
       
       mat, img3 = self.clawcam.read()
       img3 = cv2.resize(img3,(0,0), None, self.clawfac,self.clawfac)
       row3,col3,h3 = img3.shape
       border = int((row1 - row3)/2)
       img3 = cv2.copyMakeBorder(img3,border,row1 - border - row3,0,0,cv2.BORDER_CONSTANT,value=[0,0,0])
       img1 = np.concatenate((img1,img3),axis = 1)
      
       cv2.putText(img1,"Temp: " + str(text),(5,15),self.font,self.leftf,(255,255,255),1,cv2.LINE_AA)
       cv2.putText(img1,"Lines: " + str(self.result[0]),(5,45),self.font,self.leftf,(255,255,255),1,cv2.LINE_AA)
       cv2.putText(img1,"Squares: " + str(self.result[1]),(5,75),self.font,self.leftf,(255,255,255),1,cv2.LINE_AA)
       cv2.putText(img1,"Circle: " + str(self.result[2]),(5,105),self.font,self.leftf,(255,255,255),1,cv2.LINE_AA)
       cv2.putText(img1,"Triangle: " + str(self.result[3]),(5,135),self.font,self.leftf,(255,255,255),1,cv2.LINE_AA)
       top = "M1:" + str(mv[0]) + " M2:" +  str(mv[1])
       second = "M3:" + str(mv[2]) + " M4:" + str(mv[3])
       third = "M5:" + str(mv[4]) + " M6:" + str(mv[5])
       fourth = "M7:" + str(mv[6]) + " M8:" + str(mv[7])
       cv2.putText(img1,top,(left,30),self.font,self.rightf,(255,255,255),1,cv2.LINE_AA)
       cv2.putText(img1,second,(left,60),self.font,self.rightf,(255,255,255),1,cv2.LINE_AA)
       cv2.putText(img1,third,(left,90),self.font,self.rightf,(255,255,255),1,cv2.LINE_AA)
       cv2.putText(img1,fourth,(left,120),self.font,self.rightf,(255,255,255),1,cv2.LINE_AA)
       img1 = cv2.resize(img1,(0,0),None,self.total,self.total)
       cv2.imshow('Display', img1)

       
   #Shut down all the process after use
   def end(self):
      self.release()
      self.delete()

   def release(self):
      self.cap.release()
      self.cop.release()
      self.clawcam.release()

   def delete(self):
      cv2.destroyAllWindows()

   #Perform image recognition on the input frame
   def imagerec(self,path):
    self.result.clear()
    v = self.ir.process(path)
    for i in range(0,len(v)):
       self.result.append(v[i])

'''
test = Video(0,1,3,2)
done = False
while(True):
   k = cv2.waitKey(1)
   if k & 0xFF == ord('q'):
        break
   take = False
   sign = 0
   total = 0
   find = False
   if k & 0xFF == ord('c'):
      find = True
   if k & 0xFF == ord('a'):
        sign = 1
   if k & 0xFF == ord('d'):
        sign = -1
   if k & 0xFF == ord('w'):
        total = 1
   if k & 0xFF == ord('s'):
        total = -1
   if k & 0xFF == ord('n'):
        test.flipcameras()
   test.updateframe(take,"12.34",find,[-250,-250,-250,-250,-250,-250,-250,-250])
   if(sign != 0):
      test.changerearsize(sign)
   if(total != 0):
      test.changesize(total)
test.end()
'''
