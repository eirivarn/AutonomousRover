from servo import servo 
from time import sleep

print("Hello")
cameraServo = servo(12)

for i in range(5):
    cameraServo.up()
    sleep(1)
    cameraServo.down()
    sleep(1)
    cameraServo.up()
    sleep(1)
    cameraServo.down()


print("Done")
