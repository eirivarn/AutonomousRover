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

motorController = motorControl()
cameraServo = Servo(12)
gripperServo = Servo(13)

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

 
def settings(motorControl):
    global curvRate
    global speed
    global turnSpeed
    global curvRateSenitivity
    stop(motorControl)
    print(f'''Choos setting to change:
    1: turnSpeed  = {turnSpeed}
    2: speed = {speed}
    3: Curv-rate senitivity = {curvRateSenitivity}
    4: exit
    ''')
    ans = input('>')
    if ans == '1':
        print(f'turn speed = {turnSpeed}')
        turnSpeed = input('New val >')
        print('done')
    elif ans == '2':
        print(f'speed = {speed}')
        speed = input('New val >')
        print('done')
    elif ans == '3':
        print(f'Curv-rate senitivity = {curvRateSenitivity}')
        curvRateSenitivity = input('New val >')
        print('done')
    else:
        print('done')
 
 
def main():
    #tiltServo = servo(30)
    #gripServo = servo(31)
    #cameraSeervo = servo(32)
 
    motor = motorControl()
 
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
            right(motor)
        elif key == 'q':
            quit(motor)
            break
        elif key == 'e':
            stop(motor)
        elif key == 'i':
            settings(motor)
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
            else: 
                gripperServo.openGripper()

       
 
try:
    main()
 
except KeyboardInterrupt:
    print("Program stopped")
