import sys
import numpy as np
import cv2

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

    def __init__(self,n,start):
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
        self.angles = [0 for i in range(0,n)]
        self.ratios = [1.0 for i in range(0,n)]
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

    def stopCam(self):
        for camera in self.cameras:
            camera.release()
        cv2.destroyAllWindows()
        print(self.angles)
        print(self.ratios)

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
        if m == ord('w'):
            video.changesize(-1)
        elif m == ord('s'):
            video.changesize(1)
        if m == ord('r'):
            video.rotateimage(-1)
        elif m == ord('t'):
            video.rotateimage(1)
        video.updateframe()
    video.stopCam()
