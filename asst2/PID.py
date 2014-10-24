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

# Additional includes----------
import actuator_sim as ser
import AX12funcADJUSTED as AX
#------------------------------

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

c = ach.Channel(ci.CONTROLLER_REF_NAME)
# feed-forward will now be refered to as "err"
err = ci.CONTROLLER_REF()
c.put(err)
c.flush()

# open file that you will write data to
#f = open('outputASST2.csv','w')

while(1):

	# get sim time at beginning of loop
	[status, framesize] = t.get(tim, wait=False, last=True)
	if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
		pass
		#print 'Sim Time = ', tim.sim[0]
	else:
        	raise ach.AchException( v.result_string(status) )
	t1 = tim.sim[0]


	# get most recent new err or wait until we have a new err available
	[status, framesize] = c.get(err, wait=True, last=True)

	# Kp = 17, this is only a P controller
	magnitude = err.err
	if magnitude < 0 :
		magnitude = -magnitude
	# get Kp*magnitude
	magnitude = int(17*magnitude)
	print 'Error = ',err.err

	#write data to csv file
	#f.write(str(err.err)+","+str(tim.sim[0])+"\n")
	
	# make sure we aren't over acceptable velocity value
	if magnitude > 1023 :
		magnitude = 1023

	if err.err < 0 :
		#go clockwise
		print 'Sim Time = ', tim.sim[0]
		buff = AX.setVelocity(0,-(magnitude))
		ref = ser.serial_sim(r,ref,buff)
		buff = AX.setVelocity(1,(magnitude))
		ref = ser.serial_sim(r,ref,buff)

	elif err.err == 0:
		#perfect. stay put.
		print 'Sim Time = ', tim.sim[0]
		buff = AX.setVelocity(0,-(magnitude))
		ref = ser.serial_sim(r,ref,buff)
		buff = AX.setVelocity(1,(magnitude))
		ref = ser.serial_sim(r,ref,buff)		
	else:
		#go counterclockwise
		print 'Sim Time = ', tim.sim[0]
		buff = AX.setVelocity(0,(magnitude))
		ref = ser.serial_sim(r,ref,buff)
		buff = AX.setVelocity(1,-(magnitude))
		ref = ser.serial_sim(r,ref,buff)

	if err.exit == '1':
		# close csv file
		#f.close()
		#close channel
		os.popen('ach rm controller-ref-chan')
		#exit process
		exit()

	# update rate of loop peaks at 20Hz	
	desiredTime = t1 + 0.05
	while(tim.sim[0] < desiredTime):
		[status, framesize] = t.get(tim, wait=False, last=True)
		if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
			pass
			#print 'Sim Time = ', tim.sim[0]
		else:
			raise ach.AchException( v.result_string(status) )

