from RobotController import Robot
from getkey import getkey
from threading import Event, Thread

if __name__ == "__main__":
    SHUTDOWN = Event()

    def shutdown_on_key():
            while True:
                key_pressed = getkey(blocking=True)
                if key_pressed == 'q':
                    SHUTDOWN.set()
                    return

    t = Thread(target=shutdown_on_key)
    t.start()

    while not SHUTDOWN.is_set():
        print("\n\nStarting!\n")
        robot = Robot()
        image = robot.camera.startVideoCapture(robot)
        robot.update(image)


