#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */
# /*
# Copyright (c) 2014, Daniel M. Lofaro <dan (at) danLofaro (dot) com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# */
import diff_drive
import ach
import sys
import time
from ctypes import *
import socket
import cv2.cv as cv
import cv2
import numpy as np
import os
import errChanDataType as ci

dd = diff_drive
ref = dd.H_REF()
tim = dd.H_TIME()

ROBOT_DIFF_DRIVE_CHAN   = 'robot-diff-drive'
ROBOT_CHAN_VIEW   = 'robot-vid-chan'
ROBOT_TIME_CHAN  = 'robot-time'
# CV setup 
#capture = cv.CaptureFromCAM(0)
#capture = cv2.VideoCapture(0)

# added
##sock.connect((MCAST_GRP, MCAST_PORT))
newx = 320
newy = 240

nx = 640
ny = 480

r = ach.Channel(ROBOT_DIFF_DRIVE_CHAN)
r.flush()
v = ach.Channel(ROBOT_CHAN_VIEW)
v.flush()
t = ach.Channel(ROBOT_TIME_CHAN)
t.flush()

# make a channel
makeAch = os.popen('ach mk controller-ref-chan')
print makeAch
time.sleep(5)
c = ach.Channel(ci.CONTROLLER_REF_NAME)
err = ci.CONTROLLER_REF()

# initialize errorFound variable
errorFound = 0

while True:

    # Get Frame
    img = np.zeros((newx,newy,3), np.uint8)
    c_image = img.copy()
    vid = cv2.resize(c_image,(newx,newy))
    [status, framesize] = v.get(vid, wait=False, last=True)
    if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
        vid2 = cv2.resize(vid,(nx,ny))
        img = cv2.cvtColor(vid2,cv2.COLOR_BGR2RGB)
    else:
        raise ach.AchException( v.result_string(status) )

    # convert image to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of white color in HSV
    # blue
    upper_white = np.array([130,255,255], dtype=np.uint8)
    lower_white = np.array([110,0,0], dtype=np.uint8)


    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # get moments for image
    mm = cv2.moments(mask, True); 

    # only calculate error and print red dot if we can see the cube
    if mm['m00'] != 0:
        # found green, print red dot at center and (x,y) coordinates
        # where x=0 is leftmost part of image and y=0 is topmost part of image
        cv2.circle(img,(int(mm['m10']/mm['m00']),int(mm['m01']/mm['m00'])),5,cv.CV_RGB(102,0,0),-1)
        cv2.putText(img,"("+str(int(mm['m10']/mm['m00']))+","+str(int(mm['m01']/mm['m00']))+")",(int(mm['m10']/mm['m00'])+10,int(mm['m01']/mm['m00'])+10),cv2.FONT_HERSHEY_SCRIPT_COMPLEX,0.7,cv.CV_RGB(255,255,255),1)
        errorFound = 320 - int(mm['m10']/mm['m00']) 

    # show image from robot's viewfinder
    cv2.imshow('img',img)
    cv2.waitKey(10)
    
    # send error through channel to PID.py in order for that process to control the robot's wheels
    err.err = errorFound
    err.exit = '0'
  
    c.put(err)

    # only break loop under this condition
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        err.err = 0
        # signal P controller process to exit
        err.exit = '1'
	c.put(err)
        break

cv2.destroyAllWindows()
