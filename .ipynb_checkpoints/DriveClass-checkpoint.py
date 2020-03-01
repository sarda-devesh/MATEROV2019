#import statments
import math
import numpy as np
import random
#x goes first then y and then z in coordiantes
class Drive:
    cG = [0,0,0]
    locations = [[9,19.5,0],[-9,19.5,0],[-9,-19.5,0],[9,-19.5,0],[9,0.01,0],[-9,-0.01,0]]
    thetan = [(45 * math.pi)/180.0 for i in range(0,6)] #Toe
    alphan = [(20 * math.pi)/180.0 for i in range(0,6)] #Lateral 
    acoe = [[0 for i in range(0,6)] for j in range(0,6)] 
    fsigns = [[1,-1,-1],[1,1,1],[1,-1,-1],[1,1,1],[0,0,2],[0,0,2]]
    total = [0 for i in range(0,6)]
    factor = 1.0
    #calculate the unit force (Page 2 - 3) in document
    
    def calculateforces(s,n):
        tnx = s.fsigns[n][0] * math.cos(s.thetan[n])
        tny = s.fsigns[n][1] * math.sin(s.thetan[n])
        tnz = s.fsigns[n][2] * math.tan(s.alphan[n])
        lengthn = math.sqrt(tnx ** 2 + tny ** 2 + tnz ** 2)
        return [tny/lengthn,tnx/lengthn,tnz/lengthn]

    def adjust(s):
        s.factor = 1.5 - s.factor

    #Calculating the radius needed for the cross product
    def calulaterTn(s,n):
        x = s.locations[n][0] - s.cG[0]
        y = s.locations[n][1] - s.cG[1]
        z = s.locations[n][2] - s.cG[2]
        return [y,x,z]

    #Calculate torque given the vectors of radius and force
    def Torque(s,radius,force):
        aTx = (radius[1] * force[2] - radius[2] * force[1])
        aTy = (radius[2] * force[0] - radius[0] * force[2])
        aTz = (radius[0] * force[1] - radius[1] * force[0])
        return [aTy,aTx,aTz]

    #Update the values in the a table
    def updatecoefficents(s):
        for i in range(0,6):
            currentforce = s.calculateforces(i)
            for j in range(0,3):
                s.acoe[j][i] = currentforce[j]
            currenttorque = s.Torque(s.calulaterTn(i),currentforce)
            for j in range(3,6):
                s.acoe[j][i] = currenttorque[j-3]
        for i in range(0,6):
            tot = 0.0
            for j in range(0,6):
                tot += abs(s.acoe[i][j])
            s.total[i] = tot
        s.total[2] *= 0.6
            
    def solvelinearequation(s,answers):
        if(len(s.acoe) == len(answers)):
            return np.linalg.solve(s.acoe,answers)
        raise SystemExit(0)

    def printarray(s):
        for i in range(0,6):
            v = ""
            for j in range(0,6):
                v += str(round(s.acoe[i][j],3)) + " "
            print(v)

    def arrayrounded(s,y,n):
        v = ""
        for i in range(0,len(y)):
            v += str(round(y[i],n)) + " "
        return v

    def adjustmotorvalues(s,motor):
        r = []
        maxv = math.fabs(motor[0])
        for i in range(0,len(motor)):
            r.append(motor[i])
            v = abs(motor[i])
            if(v > maxv):
                maxv = v
        maxv = max(maxv,1)
        for i in range(0,len(r)):
            r[i] = r[i]/maxv
            sign = 1
            if(r[i] < 0):
                sign = -1
            r[i] = sign * r[i]
            r[i] = int(s.factor * 250.0 * (sign * r[i]))
        return r
              
    def getsolution(s,y):
         for i in range(0,6):
             if(abs(np.round(y[i],4)) <= 0.1):
                 y[i] = 0
             if(y[2] != 0 and y[5] != 0):
                 x1 = abs(y[2])
                 x2 = abs(y[5])
                 if(x1 >= x2):
                     y[5] = 0
                 else:
                     y[2] = 0
             y[i] *= s.total[i]
         v = s.solvelinearequation(y)
         return s.adjustmotorvalues(v)


t = Drive()
t.updatecoefficents()
t.printarray()
for i in range(0,6): 
    x = [0 for j in range(0,6)]
    x[i] = 1
    print(t.getsolution(x))
