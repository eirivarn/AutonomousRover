from time import sleep
import keyboard
from motorControl import motorControl
from servo import Servo
from getkey import getkey, keys
 
#settings:
forward = False
backward = False
rotateRight = False
rotateLeft = False 

stop = False

curvRate = 2

cameraDown = True

gripperOpen = True


def driveForward(motorController):
    backward = False
    rotateRight = False
    rotateLeft = False 
    if forward == False:
        forward = True
        speedForward = 15
    motorController.forward(speedForward)
    speedForward = speedForward + 2 
 
def driveBackward(motorController):
    forward = False
    rotateRight = False
    rotateLeft = False 
    if backward == False:
        backward = True
        speedBackward = 15
    motorController.backward(speedBackward)
    speedBackward = speedBackward + 2 

def driveRotateLeft(motorController):
    forward = False
    backward = False
    turnRight = False
    if rotateLeft == False:
        rotateLeft = True
        rotateLeft = 15
    motorController.rotateLeft(SpeedRotateLeft)
    SpeedRotateLeft = SpeedRotateLeft + 2

def driveRotateRight(motorController):
    forward = False
    backward = False
    turnLeft = False
    if rotateRight == False:
        rotateRight = True
        rotateRight = 15
    motorController.rotateLeft(speedRotateRight)
    speedRotateRight = speedRotateRight + 2
 
def curveLeft(motorController):
    motorController.curveLeft(curvRate)

def curveRight(motorController):
    motorController.curveRight(curvRate) 
        
def Stop(motorController):
    motorController.stop()
    
def quit(motorController):
    motorController.quit()
 
 
def main():
    motor = motorControl()
    cameraServo = Servo(12)
    gripperServo = Servo(13)
 
    while True:
        sleep(0.1)
        #key = keyboard.read_key()
        key = getkey()
        
        motor.printSpeeds()
        #key = input('>')
        if key == 'w':
            driveForward(motor)
        elif key == 's':
            driveBackward(motor)
        elif key == 'a':
            if stop == True:
                driveRotateLeft(motor)
            else: 
                curveLeft(motor)
        elif key == 'd':
            if stop == True:
                driveRotateRight(motor)
            else: 
                curveRight(motor)
        elif key == 'q':
            quit(motor)
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
