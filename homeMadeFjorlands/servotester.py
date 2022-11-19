from servo import servo 
from time import sleep

print("Hello")
cameraServo = servo(12)
gripperServo = servo(13)


for i in range(5):
    cameraServo.up()
    gripperServo.open()
    sleep(1)
    cameraServo.down()
    gripperServo.close()

    sleep(1)
    cameraServo.up()
    gripperServo.open()
    sleep(1)
    cameraServo.down()
    gripperServo.close()

cameraServo.detatch()
gripperServo.detatch()

print("Done")
