from time import sleep


tiltServo = servo(12)

tiltServo.lower()

sleep(2)

tiltServo.lift()

