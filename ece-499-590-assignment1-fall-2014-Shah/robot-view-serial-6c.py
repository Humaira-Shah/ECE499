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

    # turn
    buff = AX.setVelocity(0,0x1FF)
    ref = ser.serial_sim(r,ref,buff)
    buff = AX.setVelocity(1,0x00)
    ref = ser.serial_sim(r,ref,buff)

    timeToSleep = 6.65

    # get sim time
    [status, framesize] = t.get(tim, wait=False, last=True)
    if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
        pass
        #print 'Sim Time = ', tim.sim[0]
    else:
        raise ach.AchException( v.result_string(status) )


    current = tim.sim[0]
    desiredTime = current + timeToSleep
    while(tim.sim[0] < desiredTime):
        # get sim time
        [status, framesize] = t.get(tim, wait=False, last=True)
        if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
            pass
            #print 'Sim Time = ', tim.sim[0]
        else:
            raise ach.AchException( v.result_string(status) )


    # slow down
    startVelocity = 0x1FF
    RTIME = 30
    finalVelocity = 0

    for j in range(RTIME + 1):
        currentVelocity = (startVelocity/RTIME) * (RTIME-j)
        buff = AX.setVelocity(0,currentVelocity)
        ref = ser.serial_sim(r,ref,buff)
        timeToSleep = 0.1

        # get sim time
        [status, framesize] = t.get(tim, wait=False, last=True)
        if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
            pass
            #print 'Sim Time = ', tim.sim[0]
        else:
            raise ach.AchException( v.result_string(status) )


        current = tim.sim[0]
        desiredTime = current + timeToSleep
        while(tim.sim[0] < desiredTime):
            # get sim time
            [status, framesize] = t.get(tim, wait=False, last=True)
            if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
                pass
                #print 'Sim Time = ', tim.sim[0]
            else:
                raise ach.AchException( v.result_string(status) )

    # speed up to forward full speed
    RTIME = 30
    finalVelocity = 0x3FF

    for j in range(RTIME + 1):
        currentVelocity = (finalVelocity/RTIME) * (j)
        buff = AX.setVelocity(0,currentVelocity)
        ref = ser.serial_sim(r,ref,buff)
        buff = AX.setVelocity(1,currentVelocity)
        ref = ser.serial_sim(r,ref,buff)
        timeToSleep = 0.1

        # get sim time
        [status, framesize] = t.get(tim, wait=False, last=True)
        if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
            pass
            #print 'Sim Time = ', tim.sim[0]
        else:
            raise ach.AchException( v.result_string(status) )


        current = tim.sim[0]
        desiredTime = current + timeToSleep
        while(tim.sim[0] < desiredTime):
            # get sim time
            [status, framesize] = t.get(tim, wait=False, last=True)
            if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
                pass
                #print 'Sim Time = ', tim.sim[0]
            else:
                raise ach.AchException( v.result_string(status) )

    # stay at full speed for some amount of time
    timeToSleep = 15

    # get sim time
    [status, framesize] = t.get(tim, wait=False, last=True)
    if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
        pass
        #print 'Sim Time = ', tim.sim[0]
    else:
        raise ach.AchException( v.result_string(status) )


    current = tim.sim[0]
    desiredTime = current + timeToSleep
    while(tim.sim[0] < desiredTime):
        # get sim time
        [status, framesize] = t.get(tim, wait=False, last=True)
        if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
            pass
            #print 'Sim Time = ', tim.sim[0]
        else:
            raise ach.AchException( v.result_string(status) )    

    # slow down to stationary to prepare for turn
    startVelocity = 0x3FF
    RTIME = 30
    finalVelocity = 0

    for j in range(RTIME + 1):
        currentVelocity = (startVelocity/RTIME) * (RTIME-j)
        buff = AX.setVelocity(0,currentVelocity)
        ref = ser.serial_sim(r,ref,buff)
        buff = AX.setVelocity(1,currentVelocity)
        ref = ser.serial_sim(r,ref,buff)
        timeToSleep = 0.1

        # get sim time
        [status, framesize] = t.get(tim, wait=False, last=True)
        if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
            pass
            #print 'Sim Time = ', tim.sim[0]
        else:
            raise ach.AchException( v.result_string(status) )


        current = tim.sim[0]
        desiredTime = current + timeToSleep
        while(tim.sim[0] < desiredTime):
            # get sim time
            [status, framesize] = t.get(tim, wait=False, last=True)
            if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
                pass
                #print 'Sim Time = ', tim.sim[0]
            else:
                raise ach.AchException( v.result_string(status) )



#-----------------------------------------------------
#--------[ Do not edit below ]------------------------
#-----------------------------------------------------
