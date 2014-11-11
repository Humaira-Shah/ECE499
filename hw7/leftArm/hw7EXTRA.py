#	File: hw7EXTRA.py
#	Student: Humaira Shah
#	Assignment: IK square
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
import supplyPositionDataType as ci
from ctypes import *

time.sleep(10)


s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)
# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()
	
# feed-back will now be refered to as "ref"
ref = ha.HUBO_REF()

# channel for getting position data
c = ach.Channel(ci.CONTROLLER_REF_NAME)
# feed-forward will now be refered to as "pos"
pos = ci.CONTROLLER_REF()
c.flush()

# x value of midshoulder with resp to neck
xshoulder = 214.0 #mm

# arm part lengths
d2 = 181.59 #mm
d1 = 179.14 #mm

# angle radians where arm is completely parallel to torso
alpha = 0.25

# get most recent new pos or wait until we have a new pos available
[status, framesize] = c.get(pos, wait=True, last=True)

# position to get to with resp to neck
x = float(pos.x) #mm
y = float(pos.y) #mm
z = float(pos.z) #mm
print x

# first take care of shoulder roll angle
LSRwanted = math.atan((x-xshoulder)/z) - alpha

# get elbow bend
LEBwanted = (math.acos(((z*z) + (y*y) - (d1*d1) - (d2*d2))/(2*d1*d2)))

# get shoulder pitch
# add 1.57079633 radians to have angle be offset from when the arm is pointed
#	outward away from hubo (LSP of 90 degrees or 1.57 rad means arm is straight out
#	along the zaxis
yoverz = y/z
theta3 = (d2*math.sin(LEBwanted))/(d1+(d2*math.cos(LEBwanted)))
LSPwanted = (-(math.atan((yoverz-theta3)/(1+(yoverz*theta3)))) - 1.570796)

print "LEBwanted: ",LEBwanted
print "LSPwanted: ",LSPwanted
print "LSRwanted: ",LSRwanted

LEBprevious = 0
LSPprevious = 0
LSRprevious = 0

LEB = 0
LSP = 0
LSR = 0

for i in range(50):	
	
	# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
	s.flush()
	r.flush()	

	# Get the current feed-forward (state) 
	[statuss, framesizes] = s.get(state, wait=False, last=False)

	tOne = state.time

	
	# get angles to apply
	LEB = ((((-LEBwanted)-LEBprevious)/50)*(i+1)) + LEBprevious
	LSR = ((((LSRwanted)-LSRprevious)/50)*(i+1)) + LSRprevious
	LSP = ((((LSPwanted)-LSPprevious)/50)*(i+1)) + LSPprevious

	# apply angles
	ref.ref[ha.LEB] = LEB
	ref.ref[ha.LSR] = LSR
	ref.ref[ha.LSP] = LSP


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

LEBprevious = LEB
LSPprevious = LSP
LSRprevious = LSR

while(1):
	# get most recent new pos or wait until we have a new pos available
	[status, framesize] = c.get(pos, wait=True, last=True)

	# position to get to with resp to neck
	x = float(pos.x) #mm
	y = float(pos.y) #mm
	z = float(pos.z) #mm

	# first take care of shoulder roll angle
	LSRwanted = math.atan((x-xshoulder)/z) - alpha

	# get elbow bend
	LEBwanted = (math.acos(((z*z) + (y*y) - (d1*d1) - (d2*d2))/(2*d1*d2)))

	# get shoulder pitch
	# add 1.57079633 radians to have angle be offset from when the arm is pointed
	#	outward away from hubo (LSP of 90 degrees or 1.57 rad means arm is straight out
	#	along the zaxis
	yoverz = y/z
	theta3 = (d2*math.sin(LEBwanted))/(d1+(d2*math.cos(LEBwanted)))
	LSPwanted = (-(math.atan((yoverz-theta3)/(1+(yoverz*theta3)))) - 1.570796)

	print "LEBwanted: ",LEBwanted
	print "LSPwanted: ",LSPwanted
	print "LSRwanted: ",LSRwanted

	for i in range(50):	
	
		# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
		s.flush()
		r.flush()	

		# Get the current feed-forward (state) 
		[statuss, framesizes] = s.get(state, wait=False, last=False)

		tOne = state.time

	
		# get angles to apply
		LEB = ((((-LEBwanted)-LEBprevious)/50)*(i+1)) + LEBprevious
		LSR = ((((LSRwanted)-LSRprevious)/50)*(i+1)) + LSRprevious
		LSP = ((((LSPwanted)-LSPprevious)/50)*(i+1)) + LSPprevious

		# apply angles
		ref.ref[ha.LEB] = LEB
		ref.ref[ha.LSR] = LSR
		ref.ref[ha.LSP] = LSP


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

	LEBprevious = LEB
	LSPprevious = LSP
	LSRprevious = LSR



# Close the connection to the channels
r.close()
s.close()
c.close()
