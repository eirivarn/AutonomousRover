from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
 
 
class Servo:
       
    def __init__(self, port):
        self.port = port
        self.open = 0.2
        self.close = 0.9
        self.up = 0.9
        self.down = 0.55
        factory = PiGPIOFactory()
        self.servo = AngularServo(port, min_pulse_width=0.0006, max_pulse_width=0.0023, pin_factory=factory)

    def openGripper(self):
        self.servo.value = self.open
 
    def closeGripper(self):
        self.servo.value = self.close

    def lift(self):
        self.servo.value = self.up
 
    def lower(self):
        self.servo.value = self.down
 
 
    
        
        
        

