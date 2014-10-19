# FUNCTION getChecksum(buff)
# Takes packet as a list for its parameter.
# Packet must include at least 6 elements in order to have checksum calculated
# last element of packet must be the checksum set to zero, function will return	
# packet with correct checksum value.
def getChecksum(buff):
	n = len(buff)
	
	if(n >= 6):
		# check that first two elements are 255 as required in order to
		# signify the start of an incoming packet
		if((buff[0] != 255) or (buff[1] != 255)):
			print "WARNING: FIRST TWO PARAMETERS OF PACKET MUST BE 255\n"
		# calculate checksum
		checksum = 0
		# consider all elements of buff except checksum element buff[n-1]
		# and except buff[0] and buff[1] for calculation of checksum
		for i in range(n-3):
			# add up all considered elements besides buff[0] and buff[1]
			checksum = checksum + buff[i+2]
		checksum = ~checksum
			
		# get least significant byte after notting
		checksum =  checksum & 0xFF
		buff[n-1] = checksum
	else: 
		# does not contain at least minimum parameters
		# Should have at least the following parameters
		# buff[0] = 0xFF
		# buff[1] = 0xFF
		# buff[2] = ID
		# buff[3] = LENGTH
		# buff[4] = INSTRUCTION
		# buff[n-1] = CHECKSUM
		print "ERROR: YOU FOOL! A PACKET MUST BE AT LEAST OF LENGTH 6\n"
	print buff
	return buff

def setVelocity(ID, vel):

	# make sure ID is valid
	if((ID > 254) or (ID < 0)):	
		print "WARNING: ID is out of acceptable range of values\n"
	ID = ID & 0xFF
	if(ID > 254):
		ID = 254

	# check to see if vel is within range of possible values
	# must have magnitude less than or equal to 0x3FF which is
	# 1023 in decimal
	if((vel > 1023) or (vel < -1023)):
		print "WARNING: User has entered vel outside acceptable range [-1023,1023]\n Behavior will not be as expected...\n"

	# check to see if user specified positive (CW)
	# or negative (CCW) velocity
	velSign = 0x04 # by default, sign bit is raised, meaning CW
	if(vel < 0):
		# vel negative, therefore set sign bit for CCW
		velSign = 0x00
		
		# make vel positive to obtain magnitude
		vel = (~vel) + 0x01

	# get 2 least significant bytes of vel
	vel = vel & 0xFFFF

	# break vel into high byte and lowbyte
	velH = vel & 0xFF00
	velH = velH >> 8
	velL = vel & 0x00FF

	# limit high byte to 0x03 because maximum
	#  velocity is 0x03FF
	velH = velH & 0x03	

	# put sign info in velH
	velH |= velSign

	# make command packet for goal position and moving speed
	packet = [0xFF, 0xFF, ID, 0x04, 0x20, velL, velH, 0]
	packet = getChecksum(packet)


	print packet
	return packet
