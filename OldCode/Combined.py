import pygame
from DriveClass import Drive
t = Drive()
size = [1,1]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
done = False
clock = pygame.time.Clock()
pygame.joystick.init()
t.updatecoefficents()
pilotInput = [0 for i in range(0,6)]
while done==False:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done=True
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    pilotInput[0] = joystick.get_axis(0)
    pilotInput[1] = -1.0 * joystick.get_axis(1)
    pilotInput[2] = joystick.get_axis(2)
    pilotInput[3] = joystick.get_axis(3)
    pilotInput[4] = -1.0 * joystick.get_axis(4)
    m = t.getsolution(pilotInput)
    print(m)
    clock.tick(5)
pygame.quit()
