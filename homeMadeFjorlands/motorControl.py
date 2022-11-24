from DCmotor import DCmotor
import numpy as np
from servo import Servo
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
 
        self.leftMotor = DCmotor(self.lSpeedPin ,self.lDirPin, const)
        self.rightMotor = DCmotor(self.rSpeedPin ,self.rDirPin, const)

        self.prevAngle, self.prevOffset = 0, 0

        self.error = 0
        self.sumOfErrors = np.zeros(20)

        self.kp = const.kp
        self.kd = const.kd
        self.ki = const.ki
    
    def followLine(self, line, angle, offset ,speed, lostLine, motionError = 1):
        if lostLine: 
            print("Lost the line")
            self.findLine()
        else:  
            np.delete(self.sumOfErrors, 0) 
            sumOfErrors = np.sum(self.sumOfErrors)
            self.sumOfErrors = np.append(self.sumOfErrors, self.error)
            self.error = self.kp * offset + self.kd * angle + self.ki*sumOfErrors
            speed = speed*motionError
            self.curve(self.error, speed)
            self.prevAngle, self.prevOffset = angle, offset

    def turnToPos(self, pos, motionError = 1):
        speed = self.turnSpeed * motionError
        if pos in range(-150, 150):
            speed = int(speed* 0.7)
        if pos > 0:
            self.rotateRight(speed)
        elif pos < 0:
            self.rotateLeft(speed)
        elif pos in range(-self.const.posDistBuffer, self.const.posDistBuffer):
            self.stop()
    

    def goToPos(self, pos, speed, motionError = 1):
        if type(pos) == None:
            self.followLine(None, 0, -pos, speed, False, motionError) ##TODO mulighet for å finne ut om vi har mistet linja her?? trengs sannsynlig vis ikke

    def forward(self, speed, motionError=1):
        self.leftMotor.forward(speed * motionError)
        self.rightMotor.forward(speed * motionError)
        print('forward', speed)
 
    def backward(self, speed, motionError=1):
        self.leftMotor.backward(speed * motionError)
        self.rightMotor.backward(speed * motionError)
        print('backward', speed)
 
 
    def stop(self):
        self.leftMotor.stop()
        self.rightMotor.stop()
        print('stop')
    
    def quit(self):
        self.leftMotor.quit()
        self.rightMotor.quit()
        print('quit')
 
 
    def rotateRight(self, speed, motionError = 1):
        print("Rotate right")
        self.rightMotor.backward(speed * motionError)
        self.leftMotor.forward(speed * motionError)
       
       
    def rotateLeft(self, speed, motionError = 1):
        print("Rotate left")
        self.rightMotor.forward(speed * motionError)
        self.leftMotor.backward(speed * motionError)

    def turnRight(self, speed, motionError=1):
        print("Turn right")
        self.rightMotor.backward(0)
        self.leftMotor.forward(speed * motionError)

    def turnLeft(self, speed, motionError = 1):
        print("Turn left")
        self.rightMotor.forward(speed * motionError)
        self.leftMotor.backward(0)
 
    def curve(self, curveRate, speed):
        if curveRate < 0: 
            self.leftMotor.forward(speed - curveRate)
            self.rightMotor.forward(speed + curveRate)
        else: 
            self.leftMotor.forward(speed - curveRate)
            self.rightMotor.forward(speed+curveRate)
        
    def findLine(self):
        if self.prevOffset > 0: 
            self.rotateLeft(self.const.turnSpeed)
        else:
            self.rotateRight(self.const.turnSpeed)


       
    def getSpeed(self):
        return self.leftMotor.getSpeed(), self.rightMotor.getSpeed()

    def printSpeeds(self):
        print(self.leftMotor.getSpeed(), self.rightMotor.getSpeed())