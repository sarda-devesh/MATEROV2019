#import statments
import math
import numpy as np
import random
#user input from 1 to -1
#define globals
#x goes first then y and then z in coordiantes
class Drive:
    fn = [1 for i in range(0,6)]
    cG = [0,0,0]
    locations = [[5,-4,0],
                 [5,4,0],
                 [-5,4,0],
                 [-5,-4,0],
                 [4,0,0],
                 [-4,0,0]]
    thetan = [(math.pi)/9.0 for i in range(0,6)]
    alphan = [(8.11 * math.pi)/180.0 for i in range(0,6)]
    acoe = [[0 for i in range(0,6)] for j in range(0,6)]
    fsigns = [[1,1,1],[1,-1,-1],[1,1,1],[1,-1,-1],[0,0,1],[0,0,1]]
    #calculate the unit force (Page 2 - 3) in document
    def calculateforces(s,n):
        tnx = s.fsigns[n][0] * s.fn[n] * math.cos(s.thetan[n])
        tny = s.fsigns[n][1] * s.fn[n] * math.sin(s.thetan[n])
        tnz = s.fsigns[n][2] * s.fn[n] * math.tan(s.alphan[n])
        lengthn = math.sqrt(tnx ** 2 + tny ** 2 + tnz ** 2)
        v = [tnx/lengthn,tny/lengthn,tnz/lengthn]
        return v

    #Calculating the radius needed for the cross product
    def calulaterTn(s,n):
        x = s.locations[n][0] - s.cG[0]
        y = s.locations[n][1] - s.cG[1]
        z = s.locations[n][2] - s.cG[2]
        b = [x,y,z]
        return b

    #Calculate torque given the vectors of radius and force
    def Torque(s,radius,force):
        aTx = (radius[1] * force[2] - radius[2] * force[1])
        aTy = (radius[2] * force[0] - radius[0] * force[2])
        aTz = (radius[0] * force[1] - radius[1] * force[0])
        return [aTx,aTy,aTz]

    #Update the values in the a table
    def updatecoefficents(s):
        for i in range(0,6):
            currentforce = s.calculateforces(i)
            for j in range(0,3):
                s.acoe[j][i] = currentforce[j]
            currenttorque = s.Torque(s.calulaterTn(i),currentforce)
            for j in range(3,6):
                s.acoe[j][i] = currenttorque[j - 3]
                

    def solvelinearequation(s,answers):
        if(len(s.acoe) == len(answers)):
            return np.linalg.solve(s.acoe,answers)
        else:
            return -1

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
        max = math.fabs(motor[0])
        for i in range(0,len(motor)):
            if(motor[i] == 0.0):
                r.append(0.0)
            else:
                r.append(motor[i])
            v = math.fabs(motor[i])
            if(v > max):
                max = v        
        if(max > 1):
            for i in range(0,len(r)):
                r[i] = r[i]/max    #convert the decimals to percent
        #for i in range(0,len(r)):
               # r[i] = 100.0 * r[i]
        return r

    def getsolution(s,y):
        return s.arrayrounded(s.solvelinearequation(y),3)

#t1 = Drive()
#t1.updatecoefficents()
#x = [3.72,0,0,0,0,0]
#print(t1.getsolution(x))
