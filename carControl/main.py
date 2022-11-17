from time import sleep
import keyboard
from motorControl import motorControl
from servo import servo
from getkey import getkey, keys
 
#settings:
turnSpeed = 100
speed = 40
curvRate = 0
curvRateNew = 5
curvRateSenitivity = 2
 
 
def up(motorControl):
    curvRate = 0
    motorControl.forward(speed)
 
def down(motorControl):
    curvRate = 0
    motorControl.backward(speed)
 
def left(motorControl):
    global curvRate
    global curvRateNew
    curvRate += curvRateSenitivity
    if motorControl.getSpeed() == 0:
        motorControl.turnLeft(turnSpeed)
    else:
        motorControl.curv(-curvRateNew)
 
def right(motorControl):
    global curvRate
    global curvRateNew
    curvRate -= curvRateSenitivity
    if motorControl.getSpeed() == 0:
        motorControl.turnRight(turnSpeed)
    else:
        motorControl.curv(curvRateNew)
        
def stop(motorControl):
    curvRate = 0
    motorControl.stop()
    
def quit(motorControl):
    curvRate = 0
    motorControl.quit()
 
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
            up(motor)
        elif key == 's':
            down(motor)
        elif key == 'a':
            left(motor)
        elif key == 'd':
            right(motor)
        elif key == 'q':
            quit(motor)
            break
        elif key == 'e':
            stop(motor)
        elif key == 'i':
            settings(motor)
        
        
        elif key == 'h':
            print('''w s a d: kjører
            q: quit
            e: stop
            i: innstillinger
            o: open
            c: close
            l: lift
            -: lower
            r: pan camera to right position
            f: pan camera to front position
            g: pan camera to left position
            ''')
       
           
        """elif key == 'c':
            settings(motor)
        elif key == 'l':
            settings(motor)
        elif key == 'i':
            settings(motor)
        elif key == 'o':
            settings(motor)
        elif key == 's':
            settings(motor)
        elif key == 's':
            settings(motor)"""
       
 
try:
    main()
 
except KeyboardInterrupt:
    print("Program stopped")
