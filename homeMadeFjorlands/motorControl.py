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

        self.prevAngle, self.prevDist = 0, 0

        self.kp = const.kp
        self.ap = const.ap
 
    def followLine(self, line, angle, lateralOffset ,speed):
        self.stop()
        sleep(0.1)
        angle = int(angle)
        lateralOffset = int(lateralOffset)
        if angle and lateralOffset == 999: 
            print("No line found")
            self.backward(speed)

        elif (lateralOffset in range(-40, 40) and angle in range (-5,5)):
            self.forward(speed)

        elif (angle in range(-10,10)):
            self.curve(lateralOffset*self.kp, speed)

        elif (lateralOffset in range(-400,-80) and angle in range (10, 30)) or (lateralOffset in range(-80,400) and angle in range(-30,-10)):
            self.forward(speed)

        elif (lateralOffset in range(-80, 800) and angle > 0) or (lateralOffset in range(-800, 80) and angle < 0):
            self.curve(angle*self.ap*np.abs(lateralOffset*self.kp), speed)
        
        elif (angle in range (-80, 80)):
            self.curve(angle*self.ap, speed)

        elif (angle in range(-89,89)):
            self.turnToPos(angle)

        else:
            print('Nå er det et tilfelle som ikke er tatt høyde for!!!!!!')
            self.stop()
        

        '''
        elif (lateralOffset < 0 and angle == 0):
            self.curveRight(-lateralOffset/10, speed)

        elif (lateralOffset > 0 and angle == 0):
            self.curveLeft(lateralOffset/10, speed)

        elif (lateralOffset < 0 and angle < 0):
            self.forward(speed)

        elif (lateralOffset > 0 and angle > 0):
            self.forward(speed)

        elif (lateralOffset > 0 and angle < 0):  
            self.curveLeft(-angle*self.ap + lateralOffset*self.kp, speed)

        elif (lateralOffset < 0 and angle > 0):
            self.curveRight(angle*self.ap - lateralOffset*self.kp, speed)'''
        

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
 
 
    def turnRight(self, speed):
        print("Turn right")
        self.rightMotor.backward(speed)
        self.leftMotor.forward(speed)
       
       
    def turnLeft(self, speed):
        print("Turn left")
        self.rightMotor.forward(speed)
        self.leftMotor.backward(speed)
 
    def curveLeft(self, curveRate, speed):
        self.leftMotor.forward(speed - curveRate)
        self.rightMotor.forward(speed + curveRate)
        print('curve left', curveRate)

    def curveRight(self, curveRate, speed):
        self.leftMotor.forward(speed + curveRate)
        self.rightMotor.forward(speed - curveRate)
        print('curve right', curveRate)
 
    def curve(self, curveRate, speed):
        self.leftMotor.forward(speed + curveRate)
        self.rightMotor.forward(speed - curveRate)
        sleep(0.1)


       
    def getSpeed(self):
        return self.leftMotor.getSpeed()

    def printSpeeds(self):
        print(self.leftMotor.getSpeed(), self.rightMotor.getSpeed())