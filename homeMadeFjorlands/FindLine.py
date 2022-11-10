import time
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
import sys
from motorControl import motorControl

class FindLine:
    def __init__(self):
        #__start filming and setting video dimensions__
        self.camera = PiCamera()
        self.camera.resolution = (640, 368)
        #camera.rotation = 180
        self.rawCapture = PiRGBArray(self.camera, size=(640, 368))
        #self.motorController = motorControler
        time.sleep(0.1)
        

    def startVideoCapture(self):
        time.sleep(0.0001)
        for frame in self.camera.capture_continuous(self.rawCapture, format=("bgr"), use_video_port=True):
            time.sleep(0.0001)
            image = frame.array
            img = self.findLine(image)
            if img == []:
                break

            cv2.imshow('Image', img)
            self.rawCapture.truncate(0)
            print('i')

            if cv2.waitKey(1) & 0xff == ord('q'):
                break
    

    def findLine(self, img):
        h = img.shape[0]
        w = img.shape[1]
        start_height = h - 5
        no_points_count=0
        #img.shape = (h,w) # set the correct dimensions for the numpy array for easier access to rows, now rows are columns

        #start_time = time.clock()
        gImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB) # Drawing color points requires RGB image
        # ret, thresh = cv2.threshold(img, 105, 255, cv2.THRESH_BINARY)
        thresh = cv2.adaptiveThreshold(gImg,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

        signed_thresh = thresh[start_height].astype(np.int16) # select only one row
        diff = np.diff(signed_thresh)   #The derivative of the start_height line

        points = np.where(np.logical_or(diff > 200, diff < -200)) #maximums and minimums of derivative

        cv2.line(img,(0,start_height),(640,start_height),(0,255,0),1) # draw horizontal line where scanning 

        if len(points) > 0 and len(points[0]) > 1: # if finds something like a black line
            #if GetSpeed() == 0: # if is stopped but finds a line
              #  BaseSpeed(Speed)

            middle = np.floor((points[0][0] + points[0][1]) / 2)
            print(points[0][0], points[0][1], middle)

            cv2.circle(img, (points[0][0], start_height), 2, (255,0,0), -1)
            cv2.circle(img, (points[0][1], start_height), 2, (255,0,0), -1)
            cv2.circle(img, (middle, start_height), 2, (0,0,255), -1)

            print(int((middle-320)/int(sys.argv[1])))
            #Direction(int((middle - 320)/float(sys.argv[1])))
        else:
            start_height -= 5
            start_height = start_height % h
            no_points_count += 1
            #Speed -= 0.1
            #BaseSpeed(Speed)
            #if Speed <= 0:
             #   return []        

        #print("Loop took:", str((time.clock()- start_time) * 1000), 'ms')

        #frames.append(frame_rgb)
        #frames.append(thresh)	
        #if psutil.virtual_memory().percent >= 85:
         #   del frames[0]

        if no_points_count > 50:
            print("Line lost")
            return []

        return img

    def quit(self):
        cv2.destroyAllWindows()