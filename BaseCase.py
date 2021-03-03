import cv2 

def set_size(stream): 
    stream.set(cv2.CAP_PROP_FRAME_WIDTH, 100)
    stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 100)

number = 1
second = 0
stream1 = cv2.VideoCapture(number + cv2.CAP_DSHOW)
set_size(stream1)
stream2 = cv2.VideoCapture(second + cv2.CAP_DSHOW)
set_size(stream2)
start = cv2.imread("brokenCamera.png")
while(True):  
    print(str(stream1.isOpened()) + " " + str(stream2.isOpened()))
    ret, frame = stream1.read()
    if ret: 
        cv2.imshow("Display1", frame)
    else: 
        cv2.imshow("Display1", start) 
        stream = cv2.VideoCapture(number + cv2.CAP_DSHOW)
    ret, frame = stream2.read()
    if ret: 
        cv2.imshow("Display2", frame)
    else: 
        cv2.imshow("Display2", start) 
        stream2 = cv2.VideoCapture(second + cv2.CAP_DSHOW)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'): 
        break
cv2.destroyAllWindows()
stream1.release()
stream2.release()