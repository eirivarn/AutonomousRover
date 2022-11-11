from motorControl import MotorControl
from LineModule import LineModule

motor = MotorControl()
lineModule = LineModule(False)

lineModule.quit()
motor.quit()