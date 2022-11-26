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

    forward = False
    backward = False
    rotateRight = False
    rotateLeft = False 

    stop = True

    curvRate = 2    
 
    while True:
        sleep(0.1)
        #key = keyboard.read_key()
        key = getkey()
        
        motor.printSpeeds()
        #key = input('>')
        if key == 'w':
            stop = False
            backward = False
            rotateRight = False
            rotateLeft = False
            if forward == False:
                forward = True
                speedForward = 15
            motor.forward(speedForward)
            speedForward = speedForward + 2 
        
        elif key == 's':
            stop = False
            forward = False
            rotateRight = False
            rotateLeft = False 
            if backward == False:
                backward = True
                speedBackward = 15
            motor.backward(speedBackward)
            speedBackward = speedBackward + 2 
        
        elif key == 'a':
            stop = False
            forward = False
            backward = False
            rotateRight = False
            if rotateLeft == False:
                rotateLeft = True
                speedRotateLeft = 15
            if stop == True:
                motor.rotateLeft(speedRotateLeft)
            else: 
                motor.curveLeft(curvRate)
            SpeedRotateLeft = SpeedRotateLeft + 2

        elif key == 'd':
            stop = False
            forward = False
            backward = False
            rotateLeft = False
            if rotateRight == False:
                speedRotateRight = True
                speedRotateRight = 15
            if stop == True:
                motor.rotateRight(speedRotateRight)
            else: 
                motor.curveRight(curvRate)
            speedRotateRight = speedRotateRight + 2

        elif key == 'q':
            motor.quit()
            break
        elif key == 'e':
            motor.stop()
        elif key == 'o':
            if cameraDown == True:
                cameraServo.lift()
                cameraDown = False
            else: 
                cameraServo.lower()
                cameraDown = True
        elif key == 'SPACE':
            if gripperOpen == True:
                gripperServo.closeGripper()
                gripperOpen = False
            else: 
                gripperServo.openGripper()
                gripperOpen = False


try:
    main()
 
except KeyboardInterrupt:
    print("Program stopped")
