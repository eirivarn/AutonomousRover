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
    curv = 0
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
            elif speed > 0:
                speed = speed + acceleration
                motor.forward(speed)
            else:
                speed = speed - acceleration
                motor.backward(speed)
            
        elif key == 's':
            if  speed == 0:
                speed =  -15
                absSpeed = abs(speed)
                motor.backward(speed)
            elif  speed < 0:
                speed = speed - acceleration
                absSpees = abs(speed)
                motor.backward(absSpees)
            else:
                speed = speed - acceleration
                absSpeed = abs(speed)
                motor.forward(speed)

        elif key == 'a':
            if curve < 0:
                curve = curve - acceleration
                curve = abs(curve)
                motor.curveLeft(curve)
            else: 
                curve = curve + acceleration
                motor.curveRight(curve)

        elif key == 'd':
            if curve > 0:
                curve = curve - acceleration
                motor.curveLeft(curve)
            else: 
                curve = curve + acceleration
                absCurve = abs(curve)
                motor.curveRight(absCurve)

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
