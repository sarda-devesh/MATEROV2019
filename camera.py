import cv2 
import os 
import serial 
import sys 

def test_cameras(number): 
    inputvideo = cv2.VideoCapture(number)
    while(True):
        ret, frame = inputvideo.read()
        if ret:
            cv2.imshow('Display', frame)
        else: 
            dis = cv2.imread("IMG_20190316_224302737.jpg")
            dis = cv2.resize(dis, None, fx = 0.1, fy = 0.1)
            cv2.imshow('Display', dis)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            inputvideo.release()
            cv2.destroyAllWindows()
            break
        if k == ord('a'): 
            inputvideo.release()
            cv2.destroyAllWindows()
            test_cameras(number - 1)
        if k == ord('d'): 
            inputvideo.release()
            cv2.destroyAllWindows()
            test_cameras(number + 1)

if __name__ == '__main__': 
    test_cameras(0)