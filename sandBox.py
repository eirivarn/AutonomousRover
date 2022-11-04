from gpiozero import Servo
from time import sleep

servo = Servo(21)

servo.max()
sleep(1)
servo.min()
sleep(1)
servo.detach()
