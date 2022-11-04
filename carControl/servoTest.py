from servo import servo
from time import sleep


def servotest():
    myServo = servo(18 ,'ang')
    myServo.lift()
    print('lift')
    sleep(2)
    myServo.lower()
    print('lower')
    sleep(2)
    
for i in range(5):
    servotest()