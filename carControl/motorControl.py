from DCmotor import DCmotor
 
class motorControl:
    def __init__(self):
        self.lSpeedPin = 7
        self.lDirPin = 11
        self.rSpeedPin = 13
        self.rDirPin = 15
 
        self.leftMotor = DCmotor(self.lSpeedPin ,self.lDirPin)
        self.rightMotor = DCmotor(self.rSpeedPin ,self.rDirPin)
 
    def forward(self, speed):
        self.leftMotor.forward(speed)
        self.rightMotor.forward(speed)
        print('forward', speed)
 
    def backward(self, speed):
        self.leftMotor.backward(speed)
        self.rightMotor.backward(speed)
        print('backward', speed)

    def rotateRight(self, speed):
        self.rightMotor.backward(speed)
        self.leftMotor.forward(speed)
       
    def rotateLeft(self, speed):
        self.rightMotor.forward(speed)
        self.leftMotor.backward(speed)
 
    def curve(self, curveRate):
        self.leftMotor.forward(curveRate)
        self.rightMotor.backward(curveRate)

    def stop(self):
        self.leftMotor.stop()
        self.rightMotor.stop()
        print('stop')
    
    def quit(self):
        self.leftMotor.quit()
        self.rightMotor.quit()
        print('quit')
 

    def getSpeed(self):
        return self.leftMotor.getSpeed()

    def printSpeeds(self):
        print(self.leftMotor.getSpeed(), self.rightMotor.getSpeed())
