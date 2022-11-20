import time
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
from const import Const
import numpy as np

camera = PiCamera()
camera.resolution = (640, 480)
rawCapture = PiRGBArray(camera, size=(640, 480))
image = None

const = Const()

def startVideoCapture():
    time.sleep(0.1)
    for frame in camera.capture_continuous(rawCapture, format=("bgr"), use_video_port=True):
        time.sleep(0.0001)

        image = frame.array
        
        up = 100
        lower = np.array([0, 0, 0], dtype = "uint8")
        upper = np.array([up, up, up], dtype = "uint8")
        mask = cv2.inRange(image, lower, upper)
        image = cv2.bitwise_and(image, image, mask = mask)
        image = cv2.bitwise_not(image, image, mask = mask)
        image = (255-image)
        pixels = 10

        w, h  = image.shape[:2]

        #points = np.array([])

        x = np.array([])
        y = np.array([])

        for i in range(0,w,pixels):
            for j in range(0,h,pixels):
                if (image[i][j] == [0,0,0]).all():
                    #points.append([i,j])
                    x = np.append(x ,i)
                    y = np.append(y, j)
        
        poly = np.polyfit(x,y,2)
        draw_x = np.linspace(0,w, int(w/pixels))
        draw_y = np.polyval(poly, draw_x)

        draw_points = (np.asarray([draw_x, draw_y]).T).astype(np.int32)
        cv2.polylines(image, [draw_points], False, (0,0,255))

        cv2.imshow('image', image)

        frame.truncate(0)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break

startVideoCapture()