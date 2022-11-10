import motorControl
import LineModule

motor = motorControl.motorControl()
lineModule = LineModule.LineDetector(motor)

lineModule.quit()
motor.quit()