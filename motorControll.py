import RPi.GPIO as GPIO
from time import sleep

class motorController:
    
    def __init__(self):
        self.l_speed = 7
        self.l_direction = 11
        
        self.r_speed = 13
        self.r_direction = 15
        
        GPIO.setwarnings(False)            
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.l_speed, GPIO.OUT)
        GPIO.setup(self.l_direction, GPIO.OUT)
        GPIO.setup(self.r_speed, GPIO.OUT)
        GPIO.setup(self.r_direction, GPIO.OUT)
        self.l_speed_pwm = GPIO.PWM(self.l_speed, 100)
        self.r_speed_pwm = GPIO.PWM(self.r_speed, 100)
        self.l_speed_pwm.start(0)
        self.r_speed_pwm.start(0)
        
    def forward(self):
        print("Driving forward")
        GPIO.output(self.l_direction, 1)
        GPIO.output(self.r_direction, 1)
        self.l_speed_pwm.ChangeDutyCycle(30)
        self.r_speed_pwm.ChangeDutyCycle(30)
    
    def backward(self):
        print("Driving backward")
        GPIO.output(self.l_direction, 0)
        GPIO.output(self.r_direction, 0)
        self.l_speed_pwm.ChangeDutyCycle(10)
        self.r_speed_pwm.ChangeDutyCycle(10)
    
    def turnRight(self):
        print("Turn right")
        GPIO.output(self.l_direction, 1)
        GPIO.output(self.r_direction, 1)
        self.l_speed_pwm.ChangeDutyCycle(0)
        self.r_speed_pwm.ChangeDutyCycle(30)
        
    def turnLeft(self):
        print("Turn right")
        GPIO.output(self.l_direction, 1)
        GPIO.output(self.r_direction, 1)
        self.l_speed_pwm.ChangeDutyCycle(30)
        self.r_speed_pwm.ChangeDutyCycle(0)
        
        
    def stop(self):
        print("Stop")
        self.r_speed_pwm.stop()
        self.r_speed_pwm.stop()
        GPIO.cleanup()
    
        
motorController = motorController()
#motorController.turnRight()
sleep(0)
#motorController.stop()
sleep(0)
motorController.forward()
sleep(5)
motorController.stop()


        
        
        