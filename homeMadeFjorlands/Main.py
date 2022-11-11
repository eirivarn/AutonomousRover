from Task1 import Task1
from Task2 import Task2
from Task3 import Task3
from Task4 import Task4
from Victory import Victory, Fail
from motorControl import MotorControl
from LineModule import LineModule
from CupModule import CupModule


if __name__ == "__main__":

    print("\n\nStarting!\n")

    motor = MotorControl()
    lineModule = LineModule(False)
    #cupModule = CupModule(False)

    def doCourse():
        victory = False

        task1 = Task1(motor, lineModule, cupModule)
        task1.execute()
        if task1.completed():
            task2 = Task2(motor, lineModule)
            task2.execute()
            if task2.completed():
                task3 = Task3(motor, lineModule)
                task3.execute()
                if task3.completed():
                    task4 = Task4(motor, lineModule)
                    task4.execute()
                    if task4.completed():
                        Victory(motor, lineModule)
                        vitory = True
        if not vitory:
            Fail(motor, lineModule)
    

    lineModule.startVideoCapture()

    
