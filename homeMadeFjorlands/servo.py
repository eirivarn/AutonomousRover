from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from const import Const
 
class servo:
    def __init__(self, port):
        self.const = Const()
        factory = PiGPIOFactory()
        self.servo = AngularServo(port, min_pulse_width=0.0006, max_pulse_width=0.0023, pin_factory=factory)

    def openGripper(self):
        self.servo.value = self.const.open_val
 
    def closeGripper(self):
        self.servo.value = self.const.close_val

    def up(self):
        self.servo.value = self.const.up
 
    def down(self):
        self.servo.value = self.const.down
 
        
        

