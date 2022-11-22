import threading
from time import sleep
import RPi.GPIO as GPIO
 
class DCmotor:
   
    def __init__(self, speedPin, directionPin, const):
        self.speedPin = speedPin
        self.directionPin = directionPin
        self.const = const
        self.sleeping = False
 
        self.speed = 0
       
        GPIO.setwarnings(False)            
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.speedPin, GPIO.OUT)
        GPIO.setup(self.directionPin, GPIO.OUT)
        self.speed_pwm = GPIO.PWM(self.speedPin, 100)
        self.speed_pwm.start(0)
       
    def forward(self, speed):
        if speed > 100:
            speed = 100

        if not self.sleeping:
            if speed >= 0:
                if abs(speed-self.speed) < self.const.minSpeed4init and abs(speed)>abs(self.speed):
                    self.initMotor(speed)
                else:
                    GPIO.output(self.directionPin, 1)
                    self.speed_pwm.ChangeDutyCycle(speed)
            else:
                self.backward(-speed)

            self._setSpeed(speed)

        
   
    def backward(self, speed):
        if speed > 100:
            speed = 100

        if not self.sleeping:
            if speed >= 0:
                if abs(speed-self.speed) < self.const.minSpeed4init and abs(speed)>abs(self.speed):
                    self.initMotor(speed)
                else:
                    GPIO.output(self.directionPin, 0)
                    self.speed_pwm.ChangeDutyCycle(speed)
            else:
                self.forward(-speed)
            self._setSpeed(-speed)
   
 
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

    def initMotor(self, speed):
        dir = 1 if speed >=0 else 0

        thread = threading.Thread(target=self.boozt, args=[dir])
        thread.start()
    

    def boozt(self, dir):
        GPIO.output(self.directionPin, dir)
        self.speed_pwm.ChangeDutyCycle(self.const.speedBoozt)
        self.sleeping = True
        sleep(self.const.initSleep)
        self.sleeping = False

