from RobotController import Robot
import keyboard
from getkey import getkey, keys

if __name__ == "__main__":
    while True:
        key_pressed = getkey(blocking=False)
        if key_pressed == "q":
            exit()
        print("\n\nStarting!\n")
        robot = Robot()
        image = robot.camera.startVideoCapture(robot)
        robot.update(image)


