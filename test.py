from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils

# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--video", required = True, help = "path to the video thread")
#args = vars(ap.parse_args())
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()


threshold1=0
threshold2=200

#cap = cv2.VideoCapture(0)
while(True):
    frame = vs.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)

    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)
    blurred = cv2.blur(gradient, (9, 9))
    (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)

    # by their area, keeping only the largest one
    (cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
    # compute the rotated bounding box of the largest contour
    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.boxPoints(rect))
    cv2.drawContours(frame, [box], -1, (0, 255, 0), 3)
    #mask = cv2.threshold(gray,threshold1, threshold2, cv2.THRESH_BINARY)
   # mask = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
  #  conter, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  #  cv2.drawContours(mask, conter, -1, (255, 0, 0), 3, cv2.LINE_4, hierarchy, 1)
    cv2.imshow('Video', frame)
    cv2.imshow('Frame', closed)
  #  print(frame)
    #print(gray)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
vs.release()
cv2.destroyAllWindows()