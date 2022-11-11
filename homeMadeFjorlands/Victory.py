from motorControl import motorControl
from LineModule import LineModule

def Victory(motorControl, lineModule):
    motorControl.quit()
    lineModule.quit()
    print('Victory')

def Fail(motorControl, lineModule):
    motorControl.quit()
    lineModule.quit()
    print('Failed')
