from DCmotor import DCmotor
 
 
class motorControl:
    def __init__(self):
        self.lSpeedPin = 7
        self.lDirPin = 11
        self.rSpeedPin = 13
        self.rDirPin = 15
 
        self.leftMotor = DCmotor(self.lSpeedPin ,self.lDirPin)
        self.rightMotor = DCmotor(self.rSpeedPin ,self.rDirPin)

        self.prevAngle, self.prevDist = 0, 0
 
    def drive(self, speedLeft, speedRight):
        if speedLeft < 0:
            self.leftMotor.backward(abs(speedLeft))
        else:
            self.leftMotor.forward(speedLeft)

        if speedRight < 0:
            self.rightMotor.backward(abs(speedRight))
        else:
            self.rightMotor.forward(speedRight)        


        print('Speed left: ', speedLeft, 'Speed right: ', speedRight)


    def setAngLDist(self, angle, dist):
        if angle != self.prevAngle:
            self.prevAngle = angle
            #self.curv(angle/10)
            speed = 30
            self.forward(speed)
            lSpeed = speed + angle
            rSpeed = speed - angle
            self.drive(lSpeed, rSpeed)


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
 
    def curv(self, curvRate):  #pos curvRate curves to the left, neg curvs right
        leftSpeed = self.leftMotor.getSpeed()
        rightSpeed = self.rightMotor.getSpeed()
        #if leftSpeed+curvRate<100 or rightSpeed-curvRate>100:
        #    curvRates = [100-leftSpeed, 100-rightSpeed]
        #    curvRate = min(curvRates)
       
 
        self.leftMotor.forward(leftSpeed + curvRate)
        self.rightMotor.forward(rightSpeed - curvRate)
        print(curvRate)
 
       
    def getSpeed(self):
        return self.leftMotor.getSpeed()

    def printSpeeds(self):
        print(self.leftMotor.getSpeed(), self.rightMotor.getSpeed())