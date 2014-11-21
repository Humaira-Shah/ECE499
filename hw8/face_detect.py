#)!/usr/bin/env python

import ach
import sys
import time
from ctypes import *
import socket
import cv2.cv as cv
import cv2
import numpy as np
import AngVelChan as angle

# information on error from center of img will
# be sent over a channel to dyn_move_example
# process
a = ach.Channel(angle.CONTROLLER_REF_NAME)
a.flush()
angvel = angle.CONTROLLER_REF()
a.put(angvel)

# get xml file that contains OpenCV data used to detect face 
# create haar cascade and initialize it for use
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

# get feed from camera
video_capture = cv2.VideoCapture()
video_capture.open(0)
cv.NamedWindow("img", cv.CV_WINDOW_AUTOSIZE)

while(1):

	# read the visual input from the camera frame-by-frame
	ret, img = video_capture.read()

	# get img center coords for error calculations
	imgCenterX = img.shape[1]/2
	imgCenterY = img.shape[0]/2

	# convert to grayscale in order to process img
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	gray = cv2.equalizeHist(gray)

	# get np array of of rectangles where face was believed to be found
	faceDetected = faceCascade.detectMultiScale(gray,
					scaleFactor=1.4,
					minNeighbors=2,
					minSize=(30, 30),
					flags = cv2.CASCADE_SCALE_IMAGE)

	for x, y, w, h in faceDetected:
		# draw rectangle around detected face
		cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,255), 2)

	if(not(len(faceDetected))):
		# when we can't detect a face we have the detection coordinates
		# in the center of the img so that the camera servos will see
		# zero error over the channel and won't move
		xcoord = imgCenterX
		ycoord = imgCenterY
	else:
		xcoord = (x+(x+w))/2 # get xcoord for middle of face rectangle
		ycoord = (y+(y+h))/2 # get ycoord for middle of face rectangle

	# get error fraction of how far face center is from center of image
	xerr = (float(xcoord-imgCenterX))/imgCenterX
	yerr = (float(imgCenterY-ycoord))/imgCenterY

	# send error to dyn_move_example.py file
	angvel.X=xerr
	angvel.Y=yerr
	a.put(angvel)

	# Show image with rectangle drawn on it
	cv2.imshow('face detector', img)

	# If user clicks cv window and presses escape, program will break loop
	k = cv2.waitKey(5) & 0xFF 
	if k == 27:
		break

# release capture and destroy windows
video_capture.release()
cv2.destroyAllWindows()
