import cv2
import numpy as np
number_of_cameras = 5
width = 1080 
height = int(0.75 * width)

def setCamSize(camera):
    camera.set(3,width)
    camera.set(4,height)

def test_function():
    streams = []
    for index in range(0, number_of_cameras): 
        camera = cv2.VideoCapture(index)
        ret, frame = camera.read()
        text = "Can read "
        if not ret: 
            text = "Can't read "
        else: 
            setCamSize(camera)
            streams.append(camera)
        display = text + " frame " + str(index)
        print(display)

    for camera in streams:
        camera.release()  
    cv2.destroyAllWindows()

def addition_function():
    n = 1
    b = 1
    while(n <= 2015): 
        a_next = n + 1
        if b <= a_next: 
            b += a_next
            #print("Function first")
        elif b > a_next: 
            b -= a_next
            #print("Function second")
        #print("A_next is " + str(a_next))
        #print("B is " + str(b))
        if b == 1: 
            print(n)
        n += 1