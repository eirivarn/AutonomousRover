import cv2
import time
import datetime
import imutils

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

        if first_frame is None:
            first_frame = greyscale_image 
            # first frame is set for background subtraction(BS) using absdiff and then using threshold to get the foreground mask
            # foreground mask (black background anything that wasnt in image in first frame but is in newframe over the threshold will
            # be a white pixel(white) foreground image is black with new object being white...there is your motion detection
        else:
            pass


        frame = imutils.resize(frame, width=500)
        frame_delta = cv2.absdiff(first_frame, greyscale_image) 
        # calculates the absolute diffrence between each element/pixel between the two images, first_frame - greyscale (on each element)
        
        # edit the ** thresh ** depending on the light/dark in room, change the 100(anything pixel value over 100 will become 255(white))
        thresh = cv2.threshold(frame_delta, 100, 255, cv2.THRESH_BINARY)[1]
        # threshold gives two outputs retval,threshold image. using [1] on the end i am selecting the threshold image that is produced

        dilate_image = cv2.dilate(thresh, None, iterations=2)
        # dilate = dilate,grow,expand - the effect on a binary image(black background and white foregorund) is to enlarge/expand the white 
        # pixels in the foreground wich are white(255), element=Mat() = default 3x3 kernal matrix and iterartions=2 means it
        # will do it twice

        cnt = cv2.findContours(dilate_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
        # contours gives 3 diffrent ouputs image, contours and hierarchy, so using [1] on end means contours = [1](cnt)
        # cv2.CHAIN_APPROX_SIMPLE saves memory by removing all redundent points and comppressing the contour, if you have a rectangle
        # with 4 straight lines you dont need to plot each point along the line, you only need to plot the corners of the rectangle
        # and then join the lines, eg instead of having say 750 points, you have 4 points.... look at the memory you save!


        self.motionDetected = False
        for c in cnt:
            if cv2.contourArea(c) > 800: # if contour area is less then 800 non-zero(not-black) pixels(white)
                self.motionDetected = True
                self.error = 1
                break
        if not self.motionDetected:
            self.error += self.const.deltaError


        ''' now draw text and timestamp on security feed 
        font = cv2.FONT_HERSHEY_SIMPLEX 

       
        cv2.imshow('Security Feed', frame)
        cv2.imshow('Threshold(foreground mask)', dilate_image)
        cv2.imshow('Frame_delta', frame_delta)'''
        return self.error, self.motionDetected

        








