import RPi.GPIO as GPIO
 
class DCmotor:
   
    def __init__(self, speedPin, directionPin):
        self.speedPin = speedPin
        self.directionPin = directionPin
 
        self.speed = 0
       
        GPIO.setwarnings(False)            
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.speedPin, GPIO.OUT)
        GPIO.setup(self.directionPin, GPIO.OUT)
        self.speed_pwm = GPIO.PWM(self.speedPin, 100)
        self.speed_pwm.start(0)
       
    def forward(self, speed):
        GPIO.output(self.directionPin, 1)
        if speed > 100:
            speed = 100
 
        if speed >= 0:
            self._setSpeed(speed)
            self.speed_pwm.ChangeDutyCycle(speed)
        else:
            self.backward(-speed)

        
   
    def backward(self, speed):
        GPIO.output(self.directionPin, 0)
        if speed > 100:
            speed = 100
 
        if speed >= 0:
            self._setSpeed(speed)
            self.speed_pwm.ChangeDutyCycle(speed)
        else:
            self.forward(-speed)
   
 
    def quit(self):
        #print("quit")
        self.stop()
        self.speedPin = 0
        GPIO.cleanup()
        
    def stop(self):
        self._setSpeed(0)
        self.speed_pwm.ChangeDutyCycle(0)
 
    def _setSpeed(self, speed):
        self.speed = speed
 
    def getSpeed(self):
        return self.speed
