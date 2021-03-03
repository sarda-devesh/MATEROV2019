#Import all the necessary classes
import pygame
import serial
from DriveClass import Drive
import numpy as np
import cv2
import sys
from WindowDisplay import Video
import threading

#Set the necessary constants
clawspeed = 80
rollspeed = 0.75
size = [100,100]
tempval = 0

#Code to get the first avaliable port
def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            return port
        except (OSError, serial.SerialException):
            pass
    return "None"

#Declare and initialize the variables necessary
drive = Drive()
t = "None"
while(t == "None"):
    t  = serial_ports()
ser = serial.Serial(t, baudrate=9600,  timeout=0)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
clock.tick(10)
pygame.joystick.init()
pilotInput = [0 for i in range(0,6)]
joystick = pygame.joystick.Joystick(0)
joystick.init()
drive.updatecoefficents()
inputsigns = [-1, -1, -1, 1, 1, -1, 1, 1]
video = Video(0,1,2,3)
temperaturevalue = ""
reading= []
done = False
while done==False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            done=True
    #Update the motor values based on the user input
    pilotInput[0] = inputsigns[0] * joystick.get_axis(0) #movement: x - axis
    pilotInput[1] = inputsigns[1] * joystick.get_axis(1) #movement: y - axis
    pilotInput[2] = inputsigns[2] * joystick.get_axis(3) #movement: z - axis
    pilotInput[5] = inputsigns[3] * joystick.get_axis(4) #rotation: z - axis
    x,y = joystick.get_hat(0)
    pilotInput[3] = x * rollspeed * inputsigns[4] #rotation: x - axis
    pilotInput[4] = y * rollspeed * inputsigns[5] #rotation: y - axis
    motorv = drive.getsolution(pilotInput)
    
    claw1 = inputsigns[6] * joystick.get_axis(2)
    if(abs(claw1) < 0.2):
        claw1 = 0
    clawfirst = int(claw1 * clawspeed)
    motorv.append(clawfirst)
    claw2 = 0
    if joystick.get_button(4):
        claw2 = inputsigns[7]
    if joystick.get_button(5):
        claw2 = -1 * inputsigns[7]
    clawsecond = int(claw2 * clawspeed)
    motorv.append(clawsecond)
    
    if joystick.get_button(2):
        tempval = 1 - tempval
    motorv.append(tempval)
    if joystick.get_button(6):
        motorv.append(1)
    elif joystick.get_button(7):
        motorv.append(-1)
    k = cv2.waitKey(1)
    if k & 0xFF == ord('q'):
        done = True
        
    motorvs = "" 
    for i in range(0,len(motorv) - 1):
        motorvs += str(motorv[i]) + ","

    motorvs += str(motorv[len(motorv) - 1]) + ";"
    ser.write(motorvs.encode("utf-8"))
    take = False
    sign = 0
    find = False
    #Adjust Temperature Reding based on input from sensor
    if(ser.in_waiting > 0):
        temperaturevalue = str(ser.readline())
        index = temperaturevalue.index("\\")
        temperaturevalue = temperaturevalue[2:index]
        tempval = 0
    #Perform fuctions on the camera display
    if joystick.get_button(0):
        take = True
    if joystick.get_button(1):
        find = True
    if joystick.get_button(3):
        for i in range(0,5):
            if(i != 2):
                inputsigns[i] *= -1
    #Display the camera outputs
    if sign != 0:
        video.changesize(sign)
    if joystick.get_button(8):
        drive.adjust()
    if joystick.get_button(9):
        video.changesize(1)
    #if (tempval == 0):
        #temperaturevalue = ""
    video.updateframe(take,temperaturevalue,find,motorv)
pygame.quit()
video.endDisplay()
ser.close()
