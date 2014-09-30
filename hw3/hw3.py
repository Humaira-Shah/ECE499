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

import actuator_sim as ser
#-----------------------------------------------------
#--------[ Do not edit above ]------------------------
#-----------------------------------------------------

# Add imports here
import AX12funcADJUSTED as AX
import controller_include as ci

# Add state variables here
leftWheelSpeed = 0
rightWheelSpeed = 0
userRequest = 0

# Add constants here
KEY_UP = 65
KEY_DOWN = 66
KEY_RIGHT = 67
KEY_LEFT = 68
USER_QUIT = 100

#-----------------------------------------------------
#--------[ Do not edit below ]------------------------
#-----------------------------------------------------
dd = diff_drive
ref = dd.H_REF()
tim = dd.H_TIME()

ROBOT_DIFF_DRIVE_CHAN   = 'robot-diff-drive'
ROBOT_CHAN_VIEW   = 'robot-vid-chan'
ROBOT_TIME_CHAN  = 'robot-time'
# CV setup 
r = ach.Channel(ROBOT_DIFF_DRIVE_CHAN)
r.flush()
t = ach.Channel(ROBOT_TIME_CHAN)
t.flush()

#-----------------------------------------------------
#--------[ Do not edit above ]------------------------
#-----------------------------------------------------

# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
c = ach.Channel(ci.CONTROLLER_REF_NAME)
#s.flush()
#r.flush()

# feed-forward will now be refered to as "state"
controller = ci.CONTROLLER_REF()

c.put(controller)

#-----------------------------------------------------
#--------[ Do not edit below ]------------------------
#-----------------------------------------------------

i=0


print '======================================'
print '============= Robot-View ============='
print '========== Daniel M. Lofaro =========='
print '========= dan@danLofaro.com =========='
print '======================================'
ref.ref[0] = 0
ref.ref[1] = 0
while True:
    [status, framesize] = t.get(tim, wait=False, last=True)
    if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
        pass
        #print 'Sim Time = ', tim.sim[0]
    else:
        raise ach.AchException( v.result_string(status) )

#-----------------------------------------------------
#--------[ Do not edit above ]------------------------
#-----------------------------------------------------
    # Main Loop
    # Def:
    # tim.sim[0] = Sim Time
   
    # get desired time to start next loop
    desiredTime = tim.sim[0] + 0.05 # for 20 Hz

    #LOOP CODE HERE
    
    #get user's preferred action
    print "USER, PLEASE ENTER ARROW KEY OR QUIT WITH 'q' IN C TERMINAL\n"
    [statuss, framesizes] = c.get(controller, wait=True, last=False)
    userRequest = ord(controller.key)

    #perform action based on userRequest
    if(userRequest == USER_QUIT):
        print "USER HAS SELECTED QUIT, PLEASE CLOSE SIMULATION WINDOW MANUALLY\n"
        time.sleep(5)
        c.close()
        sys.exit(0)
    else:
        if(userRequest == KEY_UP):
            print "INCREASE WHEEL VELOCITIES\n"
            if(leftWheelSpeed >= 993):
                leftWheelSpeed = 1023
            else:
                leftWheelSpeed += 30
            if(rightWheelSpeed >= 993):
                rightWheelSpeed = 1023
            else:
                rightWheelSpeed += 30
        elif(userRequest == KEY_DOWN):
            print "DECREASE WHEEL VELOCITIES\n"
            if(leftWheelSpeed <= -993):
                leftWheelSpeed = -1023
            else:
                leftWheelSpeed -= 30
            if(rightWheelSpeed <= -993):
                rightWheelSpeed = -1023
            else:
                rightWheelSpeed -= 30
        elif(userRequest == KEY_LEFT):
            print "TURN LEFT\n"
            if(rightWheelSpeed <= 993):
                rightWheelSpeed += 30
            elif(rightWheelSpeed < 1023):
                rightWheelSpeed = 1023
            else:
                if(leftWheelSpeed >= -993):
                    leftWheelSpeed -= 30
                else:
                    leftWheelSpeed = -1023
        elif(userRequest == KEY_RIGHT):
            print "TURN RIGHT\n"
            if(leftWheelSpeed <= 993):
                leftWheelSpeed += 30
            elif(leftWheelSpeed < 1023):
                leftWheelSpeed = 1023
            else:
                if(rightWheelSpeed >= -993):
                    rightWheelSpeed -= 30
                else:
                    rightWheelSpeed = -1023

    #update wheel velocities
    buff = AX.setVelocity(1,leftWheelSpeed)
    ref = ser.serial_sim(r,ref,buff)
    buff = AX.setVelocity(0,rightWheelSpeed)
    ref = ser.serial_sim(r,ref,buff)

    # get new sim time
    [status, framesize] = t.get(tim, wait=False, last=True)
    if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
        pass
        #print 'Sim Time = ', tim.sim[0]
    else:
        raise ach.AchException( v.result_string(status) )

    # blocking while loop
    while(tim.sim[0] < desiredTime):
        # get new sim time
        [status, framesize] = t.get(tim, wait=False, last=True)
        if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
            pass
            #print 'Sim Time = ', tim.sim[0]
        else:
            raise ach.AchException( v.result_string(status) )

#-----------------------------------------------------
#--------[ Do not edit below ]------------------------
#-----------------------------------------------------
