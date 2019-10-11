import cv2
import threading

class camThread(threading.Thread):
    def __init__(self, previewName, camID1, camID2):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID1 = camID1
        self.camID2 = camID2
        self.count = 0
        
    def run(self):
        camPreview(self.previewName, self.camID1, self.camID2)

def setCamSize(camera):
    camera.set(3,self.W)
    camera.set(4,self.H)
    
num = 0
live = True
def 

def camsecond(previewName,camID):
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(
    
def camfirst(previewName, camID1, camID2):
    cv2.namedWindow(previewName)
    cam1 = cv2.VideoCapture(camID1)
    cam2 = cv2.VideoCapture(camID2)
    setCamSize(cam1)
    setCamSize(cam2)
    while True:
        k = cv2.waitKey(1)
        if k & 0xFF == ord('q'):
            break
        rval, frame = cam1.read()
        if not rval:
            r2, take = cam2.read()
            if r2:
                frame = take
            else:
                frame = cv2.imread("brokenCamera.png",1)
        cv2.imshow(previewName, frame)
    cam1.release()
    cam2.release()
    cv2.destroyWindow(previewName)

# Create two threads as follows
thread1 = camThread("Camera 0", 0)
thread2 = camThread("Camera 1", 1)
thread3 = camThread("Camera 2", 2)
thread1.start()
thread2.start()
thread3.start()
