import cv2

_, frame = cv2.VideoCapture(0).read()

h, w  = frame.shape[:2]
middleX = int(w/2)
middleY = int(h/2)

print(frame[middleX][middleY])