from DCmotor import DCmotor
import numpy as np
from servo import servo
from getkey import getkey, keys
 
class MotorControl:
    def __init__(self):
        self.lSpeedPin = 7
        self.lDirPin = 11
        self.rSpeedPin = 13
        self.rDirPin = 15
 
        self.leftMotor = DCmotor(self.lSpeedPin ,self.lDirPin)
        self.rightMotor = DCmotor(self.rSpeedPin ,self.rDirPin)

        self.prevAngle, self.prevDist = 0, 0

        self.kp = 0.2
        self.ap = 1
 
    def followLine(self, line, angle, lateralOffset ,speed):
        if (lateralOffset == 0 and angle == 0):
            self.forward(speed)

        elif (lateralOffset < 0 and angle == 0):
            self.curveRight(-lateralOffset/10, speed)

        elif (lateralOffset > 0 and angle == 0):
            self.curveLeft(lateralOffset/10, speed)

        elif (lateralOffset < 0 and angle < 0):
            self.curveRight(-lateralOffset*self.kp, speed)

        elif (lateralOffset > 0 and angle > 0):
            self.curveLeft(lateralOffset*self.kp, speed)

        elif (lateralOffset > 0 and angle < 0):  
            self.curveLeft(-angle*self.ap + lateralOffset*self.kp, speed)

        elif (lateralOffset < 0 and angle > 0):
            self.curveRight(angle*self.ap - lateralOffset*self.kp, speed)
        

    def turnToPos(pos):
        pass 
    
    def goToCup(cupPos):
        pass #TODO basicly same as follow line exept 1point exept list of points



    def forward(self, speed):
        self.leftMotor.forward(speed)
        self.rightMotor.forward(speed)
        print('forward', speed)
 
    def backward(self, speed):
        self.leftMotor.backward(speed)
        self.rightMotor.backward(speed)
        print('backward', speed)
 
 
    def stop(self):
        self.leftMotor.stop()
        self.rightMotor.stop()
        print('stop')
    
    def quit(self):
        self.leftMotor.quit()
        self.rightMotor.quit()
        print('quit')
 
 
    def turnRight(self, speed):
        print("Turn right")
        self.rightMotor.backward(speed)
        self.leftMotor.forward(speed)
       
       
    def turnLeft(self, speed):
        print("Turn left")
        self.rightMotor.forward(speed)
        self.leftMotor.backward(speed)
 
    def curveLeft(self, curveRate, speed):
        self.leftMotor.forward(speed)
        self.rightMotor.forward(speed + curveRate)
        print('curve left', curveRate)

    def curveRight(self, curveRate, speed):
        self.leftMotor.forward(speed + curveRate)
        self.rightMotor.forward(speed)
        print('curve right', curveRate)
 
       
    def getSpeed(self):
        return self.leftMotor.getSpeed()

    def printSpeeds(self):
        print(self.leftMotor.getSpeed(), self.rightMotor.getSpeed())