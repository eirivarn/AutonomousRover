from DCmotor import DCmotor
import numpy as np
from servo import servo
from time import sleep
 
class MotorControl:
    def __init__(self, const):
        self.const = const

        self.turnSpeed = self.const.turnSpeed
        self.speed = self.const.speed


        self.lSpeedPin = self.const.lSpeedPin
        self.lDirPin = self.const.lDirPin
        self.rSpeedPin = self.const.rSpeedPin
        self.rDirPin = self.const.rDirPin
 
        self.leftMotor = DCmotor(self.lSpeedPin ,self.lDirPin)
        self.rightMotor = DCmotor(self.rSpeedPin ,self.rDirPin)

        self.prevAngle, self.prevOffset = 0, 0

        self.error = 0
        self.sumOfErrors = np.zeros(20)

        self.kp = const.kp
        self.kd = const.kd
        self.ki = const.ki
    
    def followLine(self, line, angle, offset ,speed, lostLine):
        if lostLine: 
            print("Lost the line")
            self.findLine()
        else:  
            np.delete(self.sumOfErrors, 0) 
            sumOfErrors = np.sum(self.sumOfErrors)
            self.sumOfErrors = np.append(self.sumOfErrors, self.error)
            self.error = self.kp * offset + self.kd * angle + self.ki*sumOfErrors
            self.curve(self.error, speed)
            self.prevAngle, self.prevOffset = angle, offset

    def turnToPos(self, pos):
        speed = self.turnSpeed
        if pos in range(-150, 150):
            speed = int(speed* 0.7)
        if pos > 0:
            self.turnRight(speed)
        elif pos < 0:
            self.turnLeft(speed)
        elif pos in range(-self.const.posDistBuffer, self.const.posDistBuffer):
            self.stop()
    
    def goToCup(self, cupPos):
        if cupPos in range(-self.const.cupPosBuffer, self.const.cupPosBuffer):
            self.curve(cupPos*self.kp, self.speed)
        else:
            self.turnToPos(cupPos)


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
 
 
    def rotateRight(self, speed):
        print("Turn right")
        self.rightMotor.backward(speed)
        self.leftMotor.forward(speed)
       
       
    def rotateLeft(self, speed):
        print("Turn left")
        self.rightMotor.forward(speed)
        self.leftMotor.backward(speed)

    def turnRight(self, speed):
        print("Turn right")
        self.rightMotor.backward(0)
        self.leftMotor.forward(speed)

    def turnLeft(self, speed):
        print("Turn left")
        self.rightMotor.forward(speed)
        self.leftMotor.backward(0)
 
    def curve(self, curveRate, speed):
        if curveRate < 0: 
            self.leftMotor.forward(speed - curveRate)
            self.rightMotor.forward(speed + 0.8*curveRate)
        else: 
            self.leftMotor.forward(speed - 0.8*curveRate)
            self.rightMotor.forward(speed+curveRate)
        
    def findLine(self):
        if self.prevOffset > 0: 
            self.turnLeft(self.const.turnSpeed)
        else:
            self.turnRight(self.const.turnSpeed)


       
    def getSpeed(self):
        return self.leftMotor.getSpeed()

    def printSpeeds(self):
        print(self.leftMotor.getSpeed(), self.rightMotor.getSpeed())