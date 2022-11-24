import cv2
import time
import datetime
import imutils
import numpy as np

class MotionDetection:
    def __init__(self, const):
        self.const = const
        self.error = 1
        self.motionDetected = False
        self.lastFreame = None

    def detectMotion(self, image):
    
        greyscale_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
        gaussian_frame = cv2.GaussianBlur(greyscale_frame, (21,21),0)
        blur_frame = cv2.blur(gaussian_frame, (5,5)) 
        greyscale_image = blur_frame 

        if self.lastFreame is None:
            self.lastFreame = greyscale_image 
        else:
            pass


        frame_delta = cv2.absdiff(self.lastFreame, greyscale_image) 
        # edit the ** thresh ** depending on the light/dark in room, change the 100(anything pixel value over 100 will become 255(white))
        thresh = cv2.threshold(frame_delta, 100, 255, cv2.THRESH_BINARY)[1]
        # threshold gives two outputs retval,threshold image. using [1] on the end i am selecting the threshold image that is produced
        dilate_image = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(dilate_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        self.motionDetected = False
        if len(contours) != 0:
            for c in contours:
                if cv2.contourArea(c) > self.const.minMotionArea: # if contour area is less then 800 non-zero(not-black) pixels(white)
                    self.motionDetected = True
                    self.error = 1
                    (x, y, w, h) = cv2.boundingRect(c) # x,y are the top left of the contour and w,h are the width and hieght 

                    cv2.rectangle(image, (x,y), (x+w, y+h), (0, 255, 0), 2)
                    break
        if not self.motionDetected:
            self.error += self.const.deltaError

        self.lastFreame = greyscale_frame

        #now draw text and timestamp on security feed 
        font = cv2.FONT_HERSHEY_SIMPLEX 

       
        cv2.imshow('Security Feed', image)
        cv2.imshow('Threshold(foreground mask)', dilate_image)
        cv2.imshow('Frame_delta', frame_delta)
        return self.error, self.motionDetected

        








