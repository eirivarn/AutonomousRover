from servo import servo

tiltServo = servo(13)

tiltServo.lower()

sleep(2)

tiltServo.lift()

