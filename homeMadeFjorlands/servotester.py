from servo import servo 
from time import sleep

print("Hello")
cameraServo = servo(12)

cameraServo.down()
sleep(1)
cameraServo.up()

print("Done")
