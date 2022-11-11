from picamera import PiCamera


class CaptureImage:

    def __init__(self):
        
        camera = PiCamera()
        camera.resolution = (640, 368)

        return camera