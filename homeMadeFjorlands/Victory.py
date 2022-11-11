from motorControl import MotorControl
from LineModule import LineModule

def Victory(motorControl, lineModule):
    motorControl.quit()
    lineModule.quit()
    print('Victory')

def Fail(motorControl, lineModule):
    motorControl.quit()
    lineModule.quit()
    print('Failed')
