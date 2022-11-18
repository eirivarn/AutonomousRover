from servo import servo

tiltServo = servo(13, "ang")

tiltServo.lower()

sleep(2)

tiltServo.lift()

