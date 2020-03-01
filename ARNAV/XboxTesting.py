import pygame
import serial
import sys
import time
import numpy as np 
import cv2
from Drive import *
from Display import *
from StreamThread import *

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

#t = "None"
#while(t == "None"):
    #t  = serial_ports()
#ser = serial.Serial(t, baudrate=9600,  timeout=0)
size = [100,100]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
print("Found Joystick")

num_val = 50
num_mot = 6
num_cam = 4
values = [[0 for i in range(num_val)] for j in range(num_mot)] 
totals = [0 for i in range(num_mot)]
current_avgs = [0 for i in range(num_mot)]
pilotInput = [0 for i in range(num_mot)]

val_index = 0
current_size = 0
error_range = 0.08
done = False
toWrite = False 

names = ["X", "Y", "Z", "RX", "RY", "RZ"]
motors = ["M1", "M2", "M3", "M4", "M5", "M6"]
dis_1 = ValueDisplay(names)
dis_2 = ValueDisplay(motors)
pilotInput = [0 for number in range(len(names))]
ds = DriveSystem()
ds.update_coefficients()
streams = []

for index in range(0, num_cam):
    current = StreamReader(index)
    streams.append(current.start())
large_cam = 0
combined = combine_frames(dis_1.get_frame(pilotInput), dis_2.get_frame(pilotInput))

time_count = 0
time_total = 0
print("Finished Initialization")

while done==False:
    start = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            done=True
        if event.type == pygame.JOYBUTTONDOWN: 
            if joystick.get_button(4): 
                large_cam = (large_cam - 1) % num_cam
            if joystick.get_button(5): 
                large_cam = (large_cam + 1) % num_cam
    if current_size < num_val: 
        current_size += 1
    pilotInput[0] = joystick.get_axis(0) #movement: x - axis
    pilotInput[1] = -1 * joystick.get_axis(1) #movement: y - axis
    pilotInput[2] = -1 * joystick.get_axis(3) #movement: z - axis
    pilotInput[5] = joystick.get_axis(4) #rotation: z - axis
    x,y = joystick.get_hat(0)
    pilotInput[3] = x#rotation: x - axis
    pilotInput[4] = y#rotation: y - axis
    solution = ds.solve_system(pilotInput)
    for pi_index in range(len(solution)): 
        totals[pi_index] += solution[pi_index] - values[pi_index][val_index]
        values[pi_index][val_index] = solution[pi_index]
        new_avg = totals[pi_index]/current_size
        if abs(new_avg - current_avgs[pi_index]) > error_range: 
            if abs(new_avg) <= 1.25 * error_range: 
                new_avg = 0
            current_avgs[pi_index] = new_avg
            toWrite = True
    dis = read_stream(streams, large_cam)
    if dis is None:
        continue
    if (current_size > num_val/2 and toWrite): 
        top = dis_1.get_frame(pilotInput)
        bottom = dis_2.get_frame(current_avgs)
        combined = combine_frames(top, bottom)
        motorvalues = [int(round(1500 + 400 * number)) for number in current_avgs]
        output = ", ".join(map(str, motorvalues)) + ";"
        #ser.write(output.encode("utf-8"))
        toWrite = False
    dis_height, dis_width, ch = dis.shape
    cb_height, cb_width, cb_ch = combined.shape
    if cb_height != dis_height: 
        scale = (1.0 * dis_height)/cb_height
        combined = cv2.resize(combined, None, fx = scale, fy = scale, interpolation= cv2.INTER_NEAREST)
    footage = np.hstack((dis, combined))
    cv2.imshow("Result", footage)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'): 
        done = True 
    val_index = (val_index + 1) % num_val
    time_total += time.time() - start
    time_count += 1 
print(time_count/time_total)
for item in streams: 
    item.stop()
cv2.destroyAllWindows()
pygame.quit()
#ser.close()