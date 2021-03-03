import numpy as np 
import cv2 
from Drive import DriveSystem
import random
import pygame
import time

class ValueDisplay: 
    height = 400
    lower = 40

    def __init__(self, names): 
        self.width = int(self.height/len(names)) 
        for index in range(len(names)): 
            names[index] = " " + names[index] + " "
        self.half_y = int(self.height/2)
        self.names = names

    def get_frame(self, values): 
        assert len(values) == len(self.names)
        height, width = self.height + self.lower, self.width * len(self.names)
        frame = np.zeros((height, width, 3), dtype= np.uint8)
        frame.fill(255)
        cv2.line(frame, (0, int(height - self.lower)), (width, int(height - self.lower)), (0, 0, 0), thickness= 2)
        for index in range(len(values)): 
            number = values[index]
            change = int(abs(self.half_y * number))
            lower_x = int(self.width * index)
            top_x = int(self.width * (index + 1))
            color = (0, 0, 255)
            lower_y = self.half_y - change
            top_y = self.half_y
            if number > 0: 
                color = (0, 255, 0)
            if number < 0: 
                lower_y = self.half_y
                top_y = self.half_y + change
            cv2.rectangle(frame,(lower_x, lower_y), (top_x, top_y), color, -1)
            point = (int(lower_x), int(height - 0.4 * self.lower))
            cv2.putText(frame,self.names[index], point, cv2.FONT_HERSHEY_SIMPLEX,1,(0, 0, 0), 1, cv2.LINE_AA) 
            cv2.line(frame, (lower_x, 0), (lower_x, int(height - self.lower)), (0, 0, 0), thickness= 2)
        return frame
    
def combine_frames(top, bottom): 
    toph, topw, topch = top.shape
    both, botw, botch = bottom.shape
    bottom = cv2.resize(bottom, None, fx = topw/botw, fy = toph/both, interpolation= cv2.INTER_NEAREST)
    return np.vstack((top, bottom))

if __name__ == "__main__":
    size = [100,100]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    names = ["X", "Y", "Z", "RX", "RY", "RZ"]
    motors = ["M1", "M2", "M3", "M4", "M5", "M6"]
    dis_1 = ValueDisplay(names)
    dis_2 = ValueDisplay(motors)
    pilotInput = [0 for number in range(len(names))]
    ds = DriveSystem()
    ds.update_coefficients()
    done = False
    while not done: 
        start = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                done=True
        pilotInput[0] = joystick.get_axis(0) #movement: x - axis
        pilotInput[1] = -1 * joystick.get_axis(1) #movement: y - axis
        pilotInput[2] = -1 * joystick.get_axis(3) #movement: z - axis
        pilotInput[5] = joystick.get_axis(4) #rotation: z - axis
        x,y = joystick.get_hat(0)
        pilotInput[3] = x#rotation: x - axis
        pilotInput[4] = y#rotation: y - axis
        top = dis_1.get_frame(pilotInput)
        values = ds.solve_system(pilotInput)
        bottom = dis_2.get_frame(values)
        combined = combine_frames(top, bottom)
        cv2.imshow("Output",combined)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'): 
            done = True 
    cv2.destroyAllWindows()
    pygame.quit()