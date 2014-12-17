#UNDERGRADUATE (MUST USE SIM TIME)

import hubo_ach as ha
import ach
import sys
import time
import math
from ctypes import *

# Wait for bounce when hubo drops in to ripple out
time.sleep(10)

# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)
	
s.flush()
r.flush()
# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()
# feed-back will now be refered to as "ref"
ref = ha.HUBO_REF()

# Get the current feed-forward (state) 
[statuss, framesizes] = s.get(state, wait=False, last=False)

#START STANDING UP STRAIGHT
ref.ref[ha.RHP] = 0
ref.ref[ha.RKN] = 0
ref.ref[ha.RAP] = 0
ref.ref[ha.LHP] = 0
ref.ref[ha.LKN] = 0
ref.ref[ha.LAP] = 0
ref.ref[ha.LSR] = 0
ref.ref[ha.LEB] = 0
ref.ref[ha.LSY] = 0

# Write to the feed-forward channel
r.put(ref)


#-----------------------------------------------------------------------------

time.sleep(10)

#-----------------------------------------------------------------------------

s.flush()
r.flush()
# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()
# feed-back will now be refered to as "ref"
ref = ha.HUBO_REF()

# Get the current feed-forward (state) 
[statuss, framesizes] = s.get(state, wait=False, last=False)

#PICK UP HAND FOR WAVING
ref.ref[ha.LSR] = 1.3
ref.ref[ha.LEB] = -1.0
ref.ref[ha.LSY] = 1.5

# Write to the feed-forward channel
r.put(ref)

#-----------------------------------------------------------------------------

time.sleep(20)

#-----------------------------------------------------------------------------

#START WAVING ONE HAND


for j in range(50):

	# Sleep for half the period (T = 1 Second, therefore f = 1 Hz)
	time.sleep(0.1)			

	# Flush state and ref channels
	s.flush()
	r.flush()

	# feed-forward will now be refered to as "state"
	state = ha.HUBO_STATE()

	# feed-back will now be refered to as "ref"
	ref = ha.HUBO_REF()

	# Get the current feed-forward (state) 
	[statuss, framesizes] = s.get(state, wait=False, last=False)

	#Set Left Elbow Bend (LEB) and Right Shoulder Pitch (RSP) to  -0.2 rad and 0.1 rad respectively
	ref.ref[ha.LSR] = 1.3
	ref.ref[ha.LEB] = -1.0 - ((1.0*j)/30.0)
	ref.ref[ha.LSY] = 1.5
		

	# Write to the feed-forward channel
	r.put(ref)


for j in range(30):

	# Sleep for half the period (T = 1 Second, therefore f = 1 Hz)
	time.sleep(0.1)			

	# Flush state and ref channels
	s.flush()
	r.flush()

	# feed-forward will now be refered to as "state"
	state = ha.HUBO_STATE()

	# feed-back will now be refered to as "ref"
	ref = ha.HUBO_REF()

	# Get the current feed-forward (state) 
	[statuss, framesizes] = s.get(state, wait=False, last=False)

	#Set Left Elbow Bend (LEB) and Right Shoulder Pitch (RSP) to  -0.2 rad and 0.1 rad respectively
	ref.ref[ha.LSR] = 1.3
	ref.ref[ha.LEB] = -2.0 + ((1.0*j)/30.0)
	ref.ref[ha.LSY] = 1.5


	# Write to the feed-forward channel
	r.put(ref)
	

#-----------------------------------------------------------------------------

time.sleep(1)

#-----------------------------------------------------------------------------

#MOVE THE HUBO'S BODY UP AND DOWN AT 0.25 HZ (WITHIN 0.01 HZ "SIMTIME") BY
# BENDING ONLY YOUR LEGS (DO THIS WHILE CONTINUING TO WAVE)
#GO UP AND DOWN WHILE WAVING FOR 3 CYCLES MOVING UP AND DOWN.

Complete = 0

# Get the current feed-forward (state) 
[statuss, framesizes] = s.get(state, wait=False, last=False)
t3 = state.time

cycles = 0

while(Complete == 0):
		
	# moving up and down cycle is at 0.25 Hz simtime which is within 0.01 Hz simtime
	# while loop is completed when 3 cycles have been completed

	if(cycles >= 3):
		Complete = 1
	else:
		cycles+=1
		for x in range(25):
			# move up and down at 0.25 Hz
			# while waving also

			# Get the current feed-forward (state) 
			[statuss, framesizes] = s.get(state, wait=False, last=False)
			t1 = state.time	

			#wave AND move down and up in 4 seconds
			bend = 0.3 - (0.3*math.cos(((float(x+1))/25)*2*math.pi))
			elbowBend = 1.0
				
			if (x > 19):
				elbowBend -= ((((x-20)+1))/5)
			elif (x > 14):
				elbowBend -= ((((x-15)+1))/5)
			elif (x > 9):
				elbowBend -= ((((x-10)+1))/5)
			elif (x > 4):
				elbowBend -= ((((x-5)+1))/5)
			else:
				elbowBend -= (((x+1))/5)

			ref.ref[ha.LHP] = -(bend/2)
			ref.ref[ha.LKN] = (bend)
			ref.ref[ha.LAP] = -(bend/2)
			ref.ref[ha.RHP] = -(bend/2)
			ref.ref[ha.RKN] = (bend)	
			ref.ref[ha.RAP] = -(bend/2)
			
			ref.ref[ha.LSR] = 1.3
			ref.ref[ha.LEB] = -1.0 - elbowBend
			ref.ref[ha.LSY] = 1.5			

			# Write to the feed-forward channel
			r.put(ref)

			# Get the current feed-forward (state) 
			[statuss, framesizes] = s.get(state, wait=False, last=False)
			t2 = state.time
				
			# 0.08 is (4/25), use this number since we do 
			# 25 iterations to complete this 4 second movement
			# sequence
			while(t2 < (t1 + 0.16)):
				# Get the current feed-forward (state) 
				[statuss, framesizes] = s.get(state, wait=False, last=False)
				t2 = state.time
	
#-----------------------------------------------------------------------------

#STOP MOVING UP AND DOWN
#WAIT A MINIMUM OF 5 SECONDS (WHILE CONTINUING TO WAVE)
for p in range(2):
	for x in range(25):
		#waving only (at least 5 sec, we do 8 sec from the two cycles through this for loop)

		# Get the current feed-forward (state) 
		[statuss, framesizes] = s.get(state, wait=False, last=False)
		t1 = state.time	

		elbowBend = 1.0
				
		if (x > 20):
			elbowBend -= ((((x-20)+1))/5)
		elif (x > 15):
			elbowBend -= ((((x-15)+1))/5)
		elif (x > 10):
			elbowBend -= ((((x-10)+1))/5)
		elif (x > 5):
			elbowBend -= ((((x-5)+1))/5)
		else:
			elbowBend -= (((x+1))/5)

		ref.ref[ha.LSR] = 1.3
		ref.ref[ha.LEB] = -1.0 - elbowBend
		ref.ref[ha.LSY] = 1.5			

		# Write to the feed-forward channel
		r.put(ref)

		# Get the current feed-forward (state) 
		[statuss, framesizes] = s.get(state, wait=False, last=False)
		t2 = state.time
				
		# 0.08 is (4/25), use this number since we do 
		# 25 iterations to complete this 4 second movement
		# sequence
		while(t2 < (t1 + 0.16)):
			# Get the current feed-forward (state) 
			[statuss, framesizes] = s.get(state, wait=False, last=False)
			t2 = state.time

#-----------------------------------------------------------------------------

#STOP WAVING HAND
#STAND UP STRAIGHT (ORIGINAL POSITION)

s.flush()
r.flush()
# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()
# feed-back will now be refered to as "ref"
ref = ha.HUBO_REF()

# Get the current feed-forward (state) 
[statuss, framesizes] = s.get(state, wait=False, last=False)

#START STANDING UP STRAIGHT
ref.ref[ha.RHP] = 0
ref.ref[ha.RKN] = 0
ref.ref[ha.RAP] = 0
ref.ref[ha.LHP] = 0
ref.ref[ha.LKN] = 0
ref.ref[ha.LAP] = 0
ref.ref[ha.LSR] = 0
ref.ref[ha.LEB] = 0
ref.ref[ha.LSY] = 0

# Write to the feed-forward channel
r.put(ref)

#-----------------------------------------------------------------------------

# Close the connection to the channels
r.close()
s.close()


#-----------------------------------------------------------------------------



#WRITE UP YOUR STEP BY STEP STRATEGY FOR IMPLEMENTING THE ABOVE PROBLEM (SUBMIT
# THIS ON BLACKBOARD).

#POST VIDEO OF SYSTEM WORKING ON YOUTUBE

#POST LINK AND SOURCE CODE ON BLACKBOARD
