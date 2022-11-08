from threading import Thread, RLock
from time import sleep

from LineBehavior import FollowLine
from Wheel import Wheel
from Camera import PiVideoStream

class RoverHandler:
    """
    Initializes and starts a thread where it loops over sensors and logs data as it comes in.
    """

    def __init__(self):
        self.actionLock = RLock()

        # Hardware
        self.LWheel = Wheel(7, 11)

        self.RWheel = Wheel(13, 15)

        self.camera = PiVideoStream()
        self.camera.start() 

        # Behaviors
        self.behavior = FollowLine(self)

        # Threading
        self.stopped = False
        self.mainThread = Thread(target=self.mainThread)
        self.mainThread.start()

    def mainThread(self):
        while not self.stopped:
            sleep(.001)  # Let other threads do stuff

            with self.actionLock:

                # Do Behavior Updates
                self.behavior.update()
        self.close()

    def close(self):
        # Run this when ending the main python script
        print("Robot| Closing Robot Thread")

        # Safely close main threads
        self.stopped = True
        self.mainThread.join(2)


        # In case the thread didn't close, use the lock when closing up
        with self.actionLock:
            self.LWheel.close()
            self.RWheel.close()


