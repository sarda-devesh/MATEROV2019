import sys
import numpy as np
import cv2
import os 

class Potential:

    def changeangle(self,image):
        (h, w) = image.shape[:2]
        (cX, cY) = (w // 2, h // 2)
        angle = self.angles[self.current]
        M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))
        M[0, 2] += (nW / 2) - cX
        M[1, 2] += (nH / 2) - cY
        return cv2.warpAffine(image, M, (nW, nH))

    def startcam(self,num):
        camera = cv2.VideoCapture(num,cv2.CAP_DSHOW)
        if camera is None or not camera.isOpened():
            return None
        self.setCamSize(camera)
        return camera
    
    def update_values(self, broken, arr, code = 0): 
        if(len(broken) == len(arr)): 
            for index, item in enumerate(broken): 
                if code != 0: 
                    item = float(item)
                else: 
                    item = int(item)
                arr[index] = item
    
    def readlines(self):
        if os.path.exists(self.filename):
            with open(self.filename) as file: 
                lines = file.readline().split(" ")
                if len(lines) == 2: 
                    ratiovals = lines[0].strip().split(",")
                    self.update_values(ratiovals, self.ratios, code= 1)  
                    anglevals = lines[1].strip().split(",")
                    self.update_values(anglevals, self.angles)

    def __init__(self,n,start):
        self.filename = 'bootup.txt'
        self.cameras = []
        self.W = 1080
        self.H = 0.75 * self.W
        count = 0
        for i in range(0,n):
            camera = self.startcam(i)
            if camera is not None: 
                self.cameras.append(camera)
                count += 1
        print("Can connect to " + str(count) + " cameras")
        self.angles = [0 for i in range(0,count)]
        self.ratios = [1.0 for i in range(0,count)]
        self.readlines()
        self.current = start
        self.max = n

    def setCamSize(self,camera):
        camera.set(3,self.W)
        camera.set(4,self.H)

    def changedirection(self, sign):
        self.current = (self.current + sign) % self.max

    def changesize(self, sign):
        self.ratios[self.current] += sign * 0.01

    def reconnect(self,num):
        self.cameras[num].release()
        self.cameras[num] = self.startcam(num)

    def rotateimage(self, sign):
        self.angles[self.current] = (self.angles[self.current] + 90 * sign) % 360    

    def all3(self,motor):
        mv = []
        for i in motor:
            neg = False
            if(i < 0):
                neg = True
                i *= -15
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

    def updateframe(self):
        a, img1 = self.cameras[self.current].read()
        if not a:
            img1 = cv2.imread("brokenCamera.png", 1)
            self.reconnect(self.current)
        else:
            img1 = self.changeangle(img1)
            img1 = cv2.resize(img1,(0,0),None,self.ratios[self.current],self.ratios[self.current])
        cv2.imshow('Display',img1)
    

    def convert_arr_to_line(self, arr): 
        t = ""
        for index in range(0, len(arr)): 
            t += str(arr[index])
            if index != len(arr) - 1: 
                t += ","
        return t

    def stopCam(self):
        for camera in self.cameras:
            camera.release()
        cv2.destroyAllWindows()
        with open(self.filename, 'w+') as file: 
            file.write(self.convert_arr_to_line(self.ratios) + " ")
            file.write(self.convert_arr_to_line(self.angles) + "\n")
        

if __name__ == '__main__':
    video = Potential(3,0)
    while(True):
        k = cv2.waitKey(1)
        m = k & 0xFF
        if m == ord('q'):
            break
        if m == ord('a'):
            video.changedirection(-1)
        elif m == ord('d'):
            video.changedirection(1)
        if m == ord('s'):
            video.changesize(-1)
        elif m == ord('w'):
            video.changesize(1)
        if m == ord('r'):
            video.rotateimage(-1)
        elif m == ord('t'):
            video.rotateimage(1)
        video.updateframe()
    video.stopCam()
