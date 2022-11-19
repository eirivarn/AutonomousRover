from servo import servo 
from time import sleep

print("Hello")
cameraServo = servo(12)
gripperServo = servo(13)

cameraServo.down()
gripperServo.close()

print("Done")
