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
                if backward == True:
                    speedBackward = speedBackward - curvRate
                    motor.backwards()
                else:
                    forward = True
                    speedForward = 20
            motor.forward(speedForward)
            speedForward = speedForward + curvRate
        
        elif key == 's':
            stop = False
            forward = False
            rotateRight = False
            rotateLeft = False 
            if backward == False:
                if forward == True:
                    speedForward = speedForward - curvRate
                    motor.forward(speedForward)
                else:
                    backward = True
                    speedBackward = 20
            motor.backward(speedBackward)
            speedBackward = speedBackward + curvRate
        
        elif key == 'a':
            stop = False
            forward = False
            backward = False
            rotateRight = False
            if rotateLeft == False:
                if rotateRight == True:
                    speedRotateRight = speedRotateRight - curvRate
                    motor.rotateLeft
                else: 
                    rotateLeft = True
                    speedRotateLeft = 20
            else: 
                speedRotateLeft = 0
            if stop == True:
                motor.rotateLeft(speedRotateLeft)
            else: 
                motor.curveLeft(curvRate)
                curvRate = curvRate + curvRate
            SpeedRotateLeft = SpeedRotateLeft + curvRate

        elif key == 'd':
            stop = False
            forward = False
            backward = False
            rotateLeft = False
            if rotateRight == False:
                if rotateLeft == True:
                    speedRotateLeft = speedRotateLeft - curvRate
                else: 
                    speedRotateRight = True
                    speedRotateRight = 20
            else: 
                speedRotateLeft = 0
            if stop == True:
                motor.rotateRight(speedRotateRight)
            else: 
                motor.curveRight(curvRate)
                curvRate = curvRate + curvRate
            speedRotateRight = speedRotateRight + curvRate

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
