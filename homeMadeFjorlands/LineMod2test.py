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
        
        pixels = 10

        w, h  = image.shape[:2]

        points = np.array([])

        x = np.array([])
        y = np.array([])

        for yi in range(0,h-1,pixels):
            for xi in range(0,w-1,pixels):
                if (mask[yi][xi] != [0,0,0]).all():
                    #points = np.append(points, (i,j))
                    cv2.circle(image, (xi,yi), radius=3, color=(0, 0, 255), thickness=-1)
                    x = np.append(x ,xi)
                    y = np.append(y, yi)
        if len(x)!=0:
            poly = np.polyfit(x,y,2)
            draw_x = np.linspace(0,w, int(w/pixels))
            draw_y = np.polyval(poly, draw_x)

            draw_points = (np.asarray([draw_x, draw_y]).T).astype(np.int32)
            #for point in points:
             #   cv2.circle(image, point, radius=3, color=(0, 0, 255), thickness=-1)
            cv2.polylines(image, [draw_points], False, (0,0,255))


        cv2.imshow('image', image)

        frame.truncate(0)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break

startVideoCapture()
cv2.destroyAllWindows()