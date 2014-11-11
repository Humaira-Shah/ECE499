import hubo_ach as ha
import ach
import sys
import time
import math
import os
import supplyPositionDataType as ci
from ctypes import *

s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)
# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()

# feed-back will now be refered to as "ref"
ref = ha.HUBO_REF()

# make a channel
makeAch = os.popen('ach mk controller-ref-chan')
print makeAch
time.sleep(5)
c = ach.Channel(ci.CONTROLLER_REF_NAME)
pos = ci.CONTROLLER_REF()

f = open('hw7-ikEXTRA.txt','r')
positions = f.readlines()
f.close()

for i in range(len(positions)):
	positions[i] = positions[i][:-1]

for i in range(len(positions)):
	positions[i] = positions[i].split()

for i in range(len(positions)):
	for j in range(len(positions[i])):
		positions[i][j] = float(positions[i][j])
		positions[i][j] = int(positions[i][j] * 1000)


while True:

	for i in range(len(positions)):

		# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
		s.flush()
		r.flush()	

		# Get the current feed-forward (state) 
		[statuss, framesizes] = s.get(state, wait=False, last=False)

		tOne = state.time

		# send new position through channel
		pos.x = positions[i][0]
		pos.y = positions[i][1]
		pos.z = positions[i][2]
		c.put(pos)

		# Get the current feed-forward (state) 
		[statuss, framesizes] = s.get(state, wait=False, last=False)
		
		tTwo = state.time
		
		while((tOne + 3) > tTwo):
			# Get the current feed-forward (state) 
			[statuss, framesizes] = s.get(state, wait=False, last=False)
		
			tTwo = state.time
