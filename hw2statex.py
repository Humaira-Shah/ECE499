#	File: hw2statex.py
#	Student: Humaira Shah
#	Assignment: Robot does leg flexes sinusoidally with peak-to-peak of 0.2 meters
#			at a rate of 1Hz
#
#	Comments: File is modification of hubo-simple-demo-python.py
#		from github.com/hubo 
#
#

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

for x in range(8):	
	
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

	#Set Left Shoulder Roll (LSR), Left Elbow Bend (LEB), and Left Shoulder Yaw (LSY)

	ref.ref[ha.LHR] = -((x*0.02)+0.02)
	ref.ref[ha.LAR] = ((x*0.02)+0.02)
	
	ref.ref[ha.RHR] = -((x*0.02)+0.02)
	ref.ref[ha.RAR] = ((x*0.02)+0.02)

	# Write to the feed-forward channel
	r.put(ref)

	# Close the connection to the channels
	r.close()
	s.close()

	# sleep a little
	time.sleep(1)

#---------------------------------------------------------------------

for x in range(35):	
	
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

	#Set Left Shoulder Roll (LSR), Left Elbow Bend (LEB), and Left Shoulder Yaw (LSY)

	ref.ref[ha.LHR] = -0.15
	ref.ref[ha.LAR] = 0.15
	
	ref.ref[ha.RHR] = -0.15
	ref.ref[ha.RAR] = 0.15


	ref.ref[ha.RHP] = -((x*0.04)+0.04)
	ref.ref[ha.RKN] = ((x*0.04)+0.04)

	# Write to the feed-forward channel
	r.put(ref)

	# Close the connection to the channels
	r.close()
	s.close()

	# sleep a little
	time.sleep(1)

#---------------------------------------------------------------------

for x in range(33):	
	
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

	#Set Left Shoulder Roll (LSR), Left Elbow Bend (LEB), and Left Shoulder Yaw (LSY)

	ref.ref[ha.LHR] = -0.15
	ref.ref[ha.LAR] = 0.15
	
	ref.ref[ha.RHR] = -0.15
	ref.ref[ha.RAR] = 0.15


	ref.ref[ha.RHP] = -1.4
	ref.ref[ha.RKN] = ((x*0.04)+1.44)

	# Write to the feed-forward channel
	r.put(ref)

	# Close the connection to the channels
	r.close()
	s.close()

	# sleep a little
	time.sleep(1)

#---------------------------------------------------------------------

time.sleep(2)

s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)
# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()
	
# feed-back will now be refered to as "ref"
ref = ha.HUBO_REF()


while 1:

	
	for x in range(1000):	
	
		# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
		s.flush()
		r.flush()	


		# Get the current feed-forward (state) 
		[statuss, framesizes] = s.get(state, wait=False, last=False)

		tOne = state.time

	
		#Set Left Shoulder Roll (LSR), Left Elbow Bend (LEB), and Left Shoulder Yaw (LSY)

		ref.ref[ha.LHR] = -0.15
		ref.ref[ha.LAR] = 0.15
	
		ref.ref[ha.RHR] = -0.15
		ref.ref[ha.RAR] = 0.15


		ref.ref[ha.RHP] = -1.4
		ref.ref[ha.RKN] = 2.6

		bend = 0.73 - (0.73*math.cos(((float(x+1))/1000)*2*math.pi))

		print x

		print bend		

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

