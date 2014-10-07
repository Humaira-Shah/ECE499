# /*
# Copyright (c) 2013, Daniel M. Lofaro
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



import hubo_ach as ha
import ach
import sys
import time
import math
from ctypes import *

time.sleep(10)



time.sleep(2)
s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)
# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()
	
# feed-back will now be refered to as "ref"
ref = ha.HUBO_REF()


#---------------------------------------------------------------------
# BEND
#---------------------------------------------------------------------

	
for x in range(500):	

	# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
	s.flush()
	r.flush()	


	# Get the current feed-forward (state) 
	[statuss, framesizes] = s.get(state, wait=False, last=False)

	tOne = state.time

	
	#Set Left Shoulder Roll (LSR), Left Elbow Bend (LEB), and Left Shoulder Yaw (LSY)

	bend = 0.73 - (0.73*math.cos(((float(x+1))/1000)*2*math.pi))

	print x

	print bend		

	ref.ref[ha.RHP] = -(bend/2)
	ref.ref[ha.RKN] = (bend)
	ref.ref[ha.RAP] = -(bend/2)

	ref.ref[ha.LHP] = -(bend/2)
	ref.ref[ha.LKN] = (bend)
	ref.ref[ha.LAP] = -(bend/2)

	# Write to the feed-forward channel
	r.put(ref)

	# Get the current feed-forward (state) 
	[statuss, framesizes] = s.get(state, wait=False, last=False)
		
	tTwo = state.time
		
	while((tOne + 0.001) > tTwo):
		# Get the current feed-forward (state) 
		[statuss, framesizes] = s.get(state, wait=False, last=False)
		
		tTwo = state.time
	
	print tTwo
	print tOne
	print "\n"

#------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# MOVE CENTER OF MASS OVER RIGHT FOOT
#--------------------------------------------------------------------------------

for x in range(8):	
	
	# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
	s.flush()
	r.flush()

	# Get the current feed-forward (state) 
	[statuss, framesizes] = s.get(state, wait=False, last=False)
	
	#Set Left Shoulder Roll (LSR), Left Elbow Bend (LEB), and Left Shoulder Yaw (LSY)

	ref.ref[ha.RHR] = ((x*0.02)+0.02)
	ref.ref[ha.RAR] = -((x*0.02)+0.02)
	
	ref.ref[ha.LHR] = ((x*0.02)+0.02)
	ref.ref[ha.LAR] = -((x*0.02)+0.02)

	ref.ref[ha.RHP] = -0.73
	ref.ref[ha.RKN] = 1.46
	ref.ref[ha.RAP] = -0.73

	ref.ref[ha.LHP] = -0.73
	ref.ref[ha.LKN] = 1.46
	ref.ref[ha.LAP] = -0.73

	# Write to the feed-forward channel
	r.put(ref)
	
	# sleep a little
	time.sleep(1)

while(1):


	#------------------------------------------------------------------------------------
	#---------------------------------------------------------------------
	# PICK UP LEFT LEG
	#---------------------------------------------------------------------
	
	for x in range(20):	
		
		# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
		s.flush()
		r.flush()
	
		# Get the current feed-forward (state) 
		[statuss, framesizes] = s.get(state, wait=False, last=False)

		#Set Left Shoulder Roll (LSR), Left Elbow Bend (LEB), and Left Shoulder Yaw (LSY)
	
		ref.ref[ha.LHR] = 0.15
		ref.ref[ha.LAR] = -0.15
		
		ref.ref[ha.RHR] = 0.15
		ref.ref[ha.RAR] = -0.15

		ref.ref[ha.RHP] = -0.73
		ref.ref[ha.RKN] = 1.46
		ref.ref[ha.RAP] = -0.73

		leftKneeBend = 1.46 + ((x*0.02))

		ref.ref[ha.LHP] = -leftKneeBend/2
		ref.ref[ha.LKN] = leftKneeBend
		ref.ref[ha.LAP] = -leftKneeBend/2

		# Write to the feed-forward channel
		r.put(ref)

		# sleep a little
		time.sleep(1)

	time.sleep(3)

	#------------------------------------------------------------------------------------
	#---------------------------------------------------------------------
	# EXTEND LEFT LEG (KNEE)
	#---------------------------------------------------------------------
	
	for x in range(30):	
		
		# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
		s.flush()
		r.flush()
	
		# Get the current feed-forward (state) 
		[statuss, framesizes] = s.get(state, wait=False, last=False)

		#Set Left Shoulder Roll (LSR), Left Elbow Bend (LEB), and Left Shoulder Yaw (LSY)
	
		ref.ref[ha.LHR] = 0.15
		ref.ref[ha.LAR] = -0.15
		
		ref.ref[ha.RHR] = 0.15
		ref.ref[ha.RAR] = -0.15

		rightKneeBend = 1.46 + ((x*0.01)+0.01)

		ref.ref[ha.RHP] = -.73 #-(rightKneeBend/2)
		ref.ref[ha.RKN] = 1.46 #rightKneeBend
		ref.ref[ha.RAP] = -.73 #-(rightKneeBend/2)

		ref.ref[ha.LHP] = -0.93 
		ref.ref[ha.LKN] = 1.86 - ((x*0.02)+0.02)
		ref.ref[ha.LAP] = -0.93 + ((x*0.02)+0.02)

		# Write to the feed-forward channel
		r.put(ref)

		# sleep a little
		time.sleep(1)

	#------------------------------------------------------------------------------------
	#---------------------------------------------------------------------
	# SHIFT MASS FORWARD AND TO LEFT
	#---------------------------------------------------------------------
	
	for x in range(30):	
		
		# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
		s.flush()
		r.flush()
	
		# Get the current feed-forward (state) 
		[statuss, framesizes] = s.get(state, wait=False, last=False)

		#Set Left Shoulder Roll (LSR), Left Elbow Bend (LEB), and Left Shoulder Yaw (LSY)
	
		ref.ref[ha.LHR] = 0.15 - ((x*0.01)+0.01)
		ref.ref[ha.LAR] = -0.15 + ((x*0.01)+0.01)
		
		ref.ref[ha.RHR] = 0.15 - ((x*0.01)+0.01)
		ref.ref[ha.RAR] = -0.15 + ((x*0.01)+0.01)

		ref.ref[ha.RHP] = -.73 + ((x*0.01)+0.01)
		ref.ref[ha.RKN] = 1.46 - ((x*0.01)+0.01)
		ref.ref[ha.RAP] = -.73

		ref.ref[ha.LHP] = -0.93 + ((x*0.01)+0.01)
		ref.ref[ha.LKN] = 1.26
		ref.ref[ha.LAP] = -0.33 - ((x*0.01)+0.01)

		# Write to the feed-forward channel
		r.put(ref)

		# sleep a little
		time.sleep(1)

	#------------------------------------------------------------------------------------
	#---------------------------------------------------------------------
	# PICK UP RIGHT LEG
	#---------------------------------------------------------------------
	
	for x in range(30):	
		
		# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
		s.flush()
		r.flush()
	
		# Get the current feed-forward (state) 
		[statuss, framesizes] = s.get(state, wait=False, last=False)

		#Set Left Shoulder Roll (LSR), Left Elbow Bend (LEB), and Left Shoulder Yaw (LSY)
	
		ref.ref[ha.LHR] = -0.15
		ref.ref[ha.LAR] = 0.15
		
		ref.ref[ha.RHR] = -0.15
		ref.ref[ha.RAR] = 0.15

		ref.ref[ha.RHP] = -.43 - ((x*0.01)+0.01)
		ref.ref[ha.RKN] = 1.16 + ((x*0.01)+0.01)
		ref.ref[ha.RAP] = -.73

		ref.ref[ha.LHP] = -0.63
		ref.ref[ha.LKN] = 1.26
		ref.ref[ha.LAP] = -0.63

		# Write to the feed-forward channel
		r.put(ref)

		# sleep a little
		time.sleep(1)

	#------------------------------------------------------------------------------------
	#---------------------------------------------------------------------
	# GET EQUAL BEND
	#---------------------------------------------------------------------
	
	for x in range(20):	
		
		# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
		s.flush()
		r.flush()
	
		# Get the current feed-forward (state) 
		[statuss, framesizes] = s.get(state, wait=False, last=False)

		#Set Left Shoulder Roll (LSR), Left Elbow Bend (LEB), and Left Shoulder Yaw (LSY)
	
		ref.ref[ha.LHR] = -0.15
		ref.ref[ha.LAR] = 0.15
		
		ref.ref[ha.RHR] = -0.15
		ref.ref[ha.RAR] = 0.15

		ref.ref[ha.RHP] = -.73
		ref.ref[ha.RKN] = 1.46
		ref.ref[ha.RAP] = -.73

		leftKneeBend = 1.26 + ((x*0.01)+0.01)

		ref.ref[ha.LHP] = -leftKneeBend/2
		ref.ref[ha.LKN] = leftKneeBend
		ref.ref[ha.LAP] = -leftKneeBend/2

		# Write to the feed-forward channel
		r.put(ref)

		# sleep a little
		time.sleep(1)

	time.sleep(10)

	#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
	# OTHER SIDE

	#------------------------------------------------------------------------------------
	#---------------------------------------------------------------------
	# PICK UP RIGHT LEG
	#---------------------------------------------------------------------
	
	for x in range(20):	
		
		# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
		s.flush()
		r.flush()
	
		# Get the current feed-forward (state) 
		[statuss, framesizes] = s.get(state, wait=False, last=False)

		#Set Left Shoulder Roll (LSR), Left Elbow Bend (LEB), and Left Shoulder Yaw (LSY)
	
		ref.ref[ha.RHR] = -0.15
		ref.ref[ha.RAR] = 0.15
		
		ref.ref[ha.LHR] = -0.15
		ref.ref[ha.LAR] = 0.15

		ref.ref[ha.LHP] = -0.73
		ref.ref[ha.LKN] = 1.46
		ref.ref[ha.LAP] = -0.73

		rightKneeBend = 1.46 + ((x*0.02))

		ref.ref[ha.RHP] = -rightKneeBend/2
		ref.ref[ha.RKN] = rightKneeBend
		ref.ref[ha.RAP] = -rightKneeBend/2

		# Write to the feed-forward channel
		r.put(ref)

		# sleep a little
		time.sleep(1)

	time.sleep(3)

	#------------------------------------------------------------------------------------
	#---------------------------------------------------------------------
	# EXTEND RIGHT LEG (KNEE)
	#---------------------------------------------------------------------
	
	for x in range(30):	
		
		# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
		s.flush()
		r.flush()
	
		# Get the current feed-forward (state) 
		[statuss, framesizes] = s.get(state, wait=False, last=False)

		#Set Left Shoulder Roll (LSR), Left Elbow Bend (LEB), and Left Shoulder Yaw (LSY)
	
		ref.ref[ha.RHR] = -0.15
		ref.ref[ha.RAR] = 0.15
		
		ref.ref[ha.LHR] = -0.15
		ref.ref[ha.LAR] = 0.15

		ref.ref[ha.LHP] = -.73 #-(rightKneeBend/2)
		ref.ref[ha.LKN] = 1.46 #rightKneeBend
		ref.ref[ha.LAP] = -.73 #-(rightKneeBend/2)

		ref.ref[ha.RHP] = -0.93 
		ref.ref[ha.RKN] = 1.86 - ((x*0.02)+0.02)
		ref.ref[ha.RAP] = -0.93 + ((x*0.02)+0.02)

		# Write to the feed-forward channel
		r.put(ref)

		# sleep a little
		time.sleep(1)

	#------------------------------------------------------------------------------------
	#---------------------------------------------------------------------
	# SHIFT MASS FORWARD AND TO RIGHT
	#---------------------------------------------------------------------
	
	for x in range(30):	
		
		# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
		s.flush()
		r.flush()
	
		# Get the current feed-forward (state) 
		[statuss, framesizes] = s.get(state, wait=False, last=False)

		#Set Left Shoulder Roll (LSR), Left Elbow Bend (LEB), and Left Shoulder Yaw (LSY)
	
		ref.ref[ha.RHR] = -0.15 + ((x*0.01)+0.01)
		ref.ref[ha.RAR] = 0.15 - ((x*0.01)+0.01)
		
		ref.ref[ha.LHR] = -0.15 + ((x*0.01)+0.01)
		ref.ref[ha.LAR] = 0.15 - ((x*0.01)+0.01)

		ref.ref[ha.LHP] = -.73 + ((x*0.01)+0.01)
		ref.ref[ha.LKN] = 1.46 - ((x*0.01)+0.01)
		ref.ref[ha.LAP] = -.73

		ref.ref[ha.RHP] = -0.93 + ((x*0.01)+0.01)
		ref.ref[ha.RKN] = 1.26
		ref.ref[ha.RAP] = -0.33 - ((x*0.01)+0.01)

		# Write to the feed-forward channel
		r.put(ref)

		# sleep a little
		time.sleep(1)

	#------------------------------------------------------------------------------------
	#---------------------------------------------------------------------
	# PICK UP LEFT LEG
	#---------------------------------------------------------------------
	
	for x in range(30):	
		
		# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
		s.flush()
		r.flush()
	
		# Get the current feed-forward (state) 
		[statuss, framesizes] = s.get(state, wait=False, last=False)

		#Set Left Shoulder Roll (LSR), Left Elbow Bend (LEB), and Left Shoulder Yaw (LSY)
	
		ref.ref[ha.RHR] = 0.15
		ref.ref[ha.RAR] = -0.15
		
		ref.ref[ha.LHR] = 0.15
		ref.ref[ha.LAR] = -0.15

		ref.ref[ha.LHP] = -.43 - ((x*0.01)+0.01)
		ref.ref[ha.LKN] = 1.16 + ((x*0.01)+0.01)
		ref.ref[ha.LAP] = -.73

		ref.ref[ha.RHP] = -0.63
		ref.ref[ha.RKN] = 1.26
		ref.ref[ha.RAP] = -0.63

		# Write to the feed-forward channel
		r.put(ref)

		# sleep a little
		time.sleep(1)

	#------------------------------------------------------------------------------------
	#---------------------------------------------------------------------
	# GET EQUAL BEND
	#---------------------------------------------------------------------
	
	for x in range(40):	
		
		# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
		s.flush()
		r.flush()
	
		# Get the current feed-forward (state) 
		[statuss, framesizes] = s.get(state, wait=False, last=False)

		#Set Left Shoulder Roll (LSR), Left Elbow Bend (LEB), and Left Shoulder Yaw (LSY)
	
		ref.ref[ha.RHR] = 0.15
		ref.ref[ha.RAR] = -0.15
		
		ref.ref[ha.LHR] = 0.15
		ref.ref[ha.LAR] = -0.15

		ref.ref[ha.LHP] = -.73
		ref.ref[ha.LKN] = 1.46
		ref.ref[ha.LAP] = -.73

		rightKneeBend = 1.26 + ((x*0.005)+0.005)

		ref.ref[ha.RHP] = -rightKneeBend/2
		ref.ref[ha.RKN] = rightKneeBend
		ref.ref[ha.RAP] = -rightKneeBend/2

		# Write to the feed-forward channel
		r.put(ref)

		# sleep a little
		time.sleep(1)

	time.sleep(10)

s.close()
r.close()
