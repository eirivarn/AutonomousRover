from Task1 import Task1
from Task2 import Task2
from Task3 import Task3
from Task4 import Task4
from Victory import Victory, Fail
from motorControl import MotorControl
from LineModule import LineModule
from CupModule import CupModule
from CaptureImage import CaptureImage
from Task import Task

if __name__ == "__main__":

    print("\n\nStarting!\n")

    motor = MotorControl()
    lineModule = LineModule(False)
    cupModule = CupModule(False)

    camera = CaptureImage(motor, lineModule, cupModule)

    global activeTask
    activeTask = 1

    camera.startVideoCapture()
    
    
def update(image):
    if activeTask == 1:
        task1 = Task1(motor, lineModule, cupModule)
        task1.update(image)
    elif activeTask == 2:
        task2 = Task2(motor, lineModule, cupModule)
        task2.update(image)
    elif activeTask == 3:
        task3 = Task3(motor, lineModule, cupModule)
        task3.update(image)
    elif activeTask == 4:
        task4 = Task4(motor, lineModule, cupModule)
        task4.update(image)
    elif activeTask == 5:
        Victory(motor, lineModule)

def setActiveTask(task):
    global activeTask
    activeTask = task
