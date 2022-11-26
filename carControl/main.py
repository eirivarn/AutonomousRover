from time import sleep
import keyboard
from motorControl import motorControl
from servo import Servo
from getkey import getkey, keys
 

    
 
def main():
    motor = motorControl()
    cameraServo = Servo(12)
    gripperServo = Servo(13)

    cameraDown = True
    gripperOpen = True

    speed = 0
    curve = 0
    acceleration = 5


    stop = True


    forward = False
    backward = False

 
    while True:
        sleep(0.1)
        #key = keyboard.read_key()
        key = getkey()
        
        motor.printSpeeds()
        #key = input('>')
        if key == 'w':
            if speed == 0:
                speed = 15
                motor.forward(speed)
            speed = speed + acceleration
            motor.forward(speed)
            
        elif key == 's':
            if  speed == 0:
                speed =  -15
                motor.forward(speed)
            speed = speed - acceleration
            motor.forward(speed)

        elif key == 'a':
            if curve == 0:
                curveRate = - 15
                motor.rotateLeft(-curveRate)
            else: 
                curve = curve - acceleration
                motor.curve(curve)

        elif key == 'd':
            if curve == 0:
                curveRate = 15
                motor.rotateLeft(curveRate)
            else: 
                curve = curve + acceleration
                motor.curve(curve)

        elif key == 'q':
            motor.quit()
            break
        elif key == 'e':
            speed = 0
            motor.stop()
        elif key == 'o':
            if cameraDown == True:
                cameraServo.lift()
                cameraDown = False
            else: 
                cameraServo.lower()
                cameraDown = True
        elif key == 'p':
            if gripperOpen == True:
                gripperServo.closeGripper()
                gripperOpen = False
            else: 
                gripperServo.openGripper()
                gripperOpen = True


try:
    main()
 
except KeyboardInterrupt:
    print("Program stopped")
