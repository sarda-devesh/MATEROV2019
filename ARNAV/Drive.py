import numpy as np
import math
class DriveSystem(): 
    cG = [0,0,0]
    #x, y, z, Fxd, Fyd, Fzd, Theta (plane) angle, alpha (vertical) angle
    locations = [[10,10, 0, 135, 0],
                [-10, 10, 0, 45, 0],
                [-10, -10, 0, 135, 0],
                [10, -10, 0, 45, 0],
                [20, 0, 0, 0, 90],
                [-20, 0, 0, 0, 90]]

    sums = []
    maxspeed = 250
    max_amp_per_motor = 12
    total_amp_for_motors = 20 
    threshold = 0.1
    factor = 1.0

    def __init__(self):
        self.coefficients = [[0 for i in range(0, len(self.locations))] for j in range(0,6)] 
        self.max_sum = (1.0 * self.total_amp_for_motors)/self.max_amp_per_motor

    def setFactor(self, newvalue): 
        self.factor = newvalue

    def findForce(self,motornumber): 
        forcez = math.sin(math.radians(self.locations[motornumber][4]))
        rem = (1 - forcez ** 2) ** 0.5
        forcex = rem * math.cos(math.radians(self.locations[motornumber][3]))
        forcey = rem * math.sin(math.radians(self.locations[motornumber][3]))
        return [forcex,forcey, forcez]

    def findRadius(self,motornumber): 
        values = []
        for index in range(0, len(self.cG)): 
            values.append(self.locations[motornumber][index] - self.cG[index])
        return values

    def findTorque(self, radius, force): 
        torx = radius[1] * force[2] - radius[2] * force[1]
        tory = radius[2] * force[0] - radius[0] * force[2]
        torz = radius[0] * force[1] - radius[1] * force[0]
        return torx, tory, torz

    def set_column(self, column):
        height = 0
        forcev = self.findForce(column)
        for item in forcev: 
            self.coefficients[height][column] = item
            height += 1
        torques = self.findTorque(self.findRadius(column), forcev)
        for item in torques: 
            self.coefficients[height][column] = item
            height += 1

    def updatemotor(self, motornumber):
        off = True
        for index in range(0,3):
            if(self.coefficients[index][motornumber] != 0): 
                off = False
                break
        if(off): 
            self.set_column(motornumber)
        else:
            for index in range(0, 6):
                self.coefficients[index][motornumber] = 0

    def update_coefficients(self):
        for column in range(len(self.locations)): 
            self.set_column(column)
        for i in range(0, len(self.coefficients)): 
            value = 0
            for j in self.coefficients[i]: 
                value += abs(j)
            self.sums.append(value)

    def print_coefficient(self,n): 
        for row in self.coefficients:
            t = ""
            for value in row:
                t += str(round(value,n)) + " "
            print(t)

    def adjust_for_amperage(self, formatted): 
        current_total = 0
        for value in formatted: 
            current_total += value ** 2
        if current_total < 0.05 * self.max_sum: 
            return formatted
        current_ratio = (self.max_sum/current_total) ** 0.5
        current_ratio = min(1, current_ratio)
        new_values = [item * current_ratio for item in formatted]
        return new_values

    def solve_system(self,solutions): 
        while(len(solutions) < len(self.coefficients)): 
            solutions.append(0)
        for index in range(len(solutions)): 
            if(abs(solutions[index]) <= self.threshold): 
                solutions[index] = 0
        larger = abs(solutions[2]) > abs(solutions[5])
        if larger: 
            solutions[5] = 0
        else: 
            solutions[2] = 0
        solutions = [solutions[i] * self.sums[i] for i in range(len(self.sums))]
        thrusts = np.linalg.lstsq(self.coefficients, solutions, rcond= None)[0]
        formatted = []
        for index in range(len(thrusts)): 
            if(abs(thrusts[index]) <= self.threshold): 
                formatted.append(0)
            else: 
                value = max(min(thrusts[index], 1),-1)
                formatted.append(self.factor * value)
        return self.adjust_for_amperage(formatted)

if __name__ == "__main__": 
    ds = DriveSystem()
    ds.update_coefficients()
    ds.print_coefficient(3)
    print()
    print(ds.max_sum)
    for index in range(0,6): 
        x = [0 for i in range(0,6)]
        x[index] = 1
        print(ds.solve_system(x))