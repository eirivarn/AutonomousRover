from time import sleep
from servo import servo

tiltServo = servo(12)

tiltServo.lower()

sleep(2)

tiltServo.lift()

