
import os
import dynamixel
import time
import random
import sys
import subprocess
import optparse
import yaml
import numpy as np
import ach

RAR=2
RAP=3
RKN=4
RHP=5
RHR=6
RHY=7

LAR=8
LAP=9
LKN=10
LHP=11
LHR=12
LHY=13

IDNAMES=["","","RAR","RAP","RKN","RHP","RHR","RHY","LAR","LAP","LKN","LHP","LHR","LHY"]

def rad2dyn(rad):
    return np.int(np.floor( (rad + (np.pi*300/360))/(2.0 * np.pi * 300/360) * 1024 ))

def dyn2rad(en):
    return (en / 1024.0 * 2.0 * np.pi - np.pi) * 300/360
def setGoal(myActuators,ID,val):
	for actuator in myActuators:
		if actuator.id==ID:
			actuator.goal_position = rad2dyn(val)
def getGoal(myActuators,ID):
	for actuator in myActuators:
		if actuator.id==ID:
			return dyn2rad(actuator.goal_position)

def main(settings):
    portName = settings['port']
    baudRate = settings['baudRate']
    highestServoId = settings['highestServoId']

    # Establish a serial connection to the dynamixel network.
    # This usually requires a USB2Dynamixel
    serial = dynamixel.SerialStream(port=portName, baudrate=baudRate, timeout=1)
    net = dynamixel.DynamixelNetwork(serial)
    
    # Ping the range of servos that are attached
    print "Scanning for Dynamixels..."
    net.scan(1, highestServoId)
    
    myActuators = []
    
    for dyn in net.get_dynamixels():
        print dyn.id
        myActuators.append(net[dyn.id])
    
    if not myActuators:
      print 'No Dynamixels Found!'
      sys.exit(0)
    else:
      print "...Done"
    
    for actuator in myActuators:
        actuator.moving_speed = 50
        actuator.synchronized = True
        actuator.torque_enable = True
        actuator.torque_limit = 1023
        actuator.max_torque = 1023
    
    # Randomly vary servo position within a small range

    enc = 0.0;
    angleToMove = -0.1
 	#set the starting position, standing straight
    for actuator in myActuators:
		if actuator.id==RHY or actuator.id==LHY:
			actuator.goal_position = rad2dyn(-.78)
		else:
			actuator.goal_position = rad2dyn(0)
    net.synchronize()
    time.sleep(3)

#<PHASE 1>MOVE CENTER OF MASS OVER RIGHT FOOT
    setGoal(myActuators,LHR,.25)
    setGoal(myActuators,RHR,.25)
    setGoal(myActuators,RAR,.25)
    setGoal(myActuators,LAR,.25)
    net.synchronize()
    time.sleep(1)

#<PHASE 2>PICK UP LEFT LEG AND CHANGE RHP TO STEP BACK
    amount=0
    while(amount<=.72):
        setGoal(myActuators,LHP,amount)
        setGoal(myActuators,LKN,2*amount)
        setGoal(myActuators,LAP,-amount)
        net.synchronize()		
        time.sleep(0.4)
        amount +=0.12
    setGoal(myActuators,RHP,-0.32)
    net.synchronize()
    time.sleep(1)

#<PHASE 3>LAND LEFT FOOT ON GROUND AND SHIFT CENTER OF MASS BACK
    amount=0
    while(amount<=.32):
        setGoal(myActuators,LHP,0.72 - amount)
        setGoal(myActuators,RKN, -2*amount)
        setGoal(myActuators,RAP, amount)
        net.synchronize()		
        time.sleep(0.4)
        amount +=0.08
    net.synchronize()
    time.sleep(1)

#<PHASE 4>BEND RIGHT LEG
    amount=0.32
    while(amount<=.72):
        setGoal(myActuators,RHP,-amount)
        setGoal(myActuators,RKN, -2*amount)
        setGoal(myActuators,RAP, amount)
        net.synchronize()		
        time.sleep(0.4)
        amount +=0.08
    net.synchronize()
    time.sleep(1)

#<PHASE 5>MOVE CENTER OF MASS TO MIDDLE    
    setGoal(myActuators,LHR,0)
    setGoal(myActuators,RHR,0)
    setGoal(myActuators,RAR,0)
    setGoal(myActuators,LAR,0)
    net.synchronize()
    time.sleep(1)

#<PHASE 6>MOVE CENTER OF MASS OVER LEFT FOOT    
    setGoal(myActuators,LHR,-.25)
    setGoal(myActuators,RHR,-.25)
    setGoal(myActuators,RAR,-.25)
    setGoal(myActuators,LAR,-.25)
    net.synchronize()
    time.sleep(1)

#<PHASE 7>STRAIGHTEN UP LEFT LEG
    amount=0.1
    while(amount<=.72):
        setGoal(myActuators,LKN,1.44 - 2*amount)
        setGoal(myActuators,LAP,-0.72 + amount)
        net.synchronize()		
        time.sleep(0.4)
        amount +=0.12
    net.synchronize()
    time.sleep(1)

#<PHASE 8>LAND RIGHT FOOT ON GROUND AND SHIFT CENTER OF MASS BACK
    amount=0
    while(amount<=.32):
        setGoal(myActuators,RHP,(-0.72) + amount)
        setGoal(myActuators,LKN, 2*amount)
        setGoal(myActuators,LAP, -amount)
        net.synchronize()		
        time.sleep(0.4)
        amount +=0.08
    net.synchronize()
    time.sleep(1)

#<PHASE 9>BEND LEFT LEG
    amount=0.32
    while(amount<=.72):
        setGoal(myActuators,LHP,amount)
        setGoal(myActuators,LKN, 2*amount)
        setGoal(myActuators,LAP, -amount)
        net.synchronize()		
        time.sleep(0.4)
        amount +=0.08
    net.synchronize()
    time.sleep(1)

#<PHASE 10>MOVE CENTER OF MASS TO MIDDLE    
    setGoal(myActuators,LHR,0)
    setGoal(myActuators,RHR,0)
    setGoal(myActuators,RAR,0)
    setGoal(myActuators,LAR,0)
    net.synchronize()
    time.sleep(1)

#<PHASE 11>MOVE CENTER OF MASS OVER RIGHT FOOT    
    setGoal(myActuators,LHR,.25)
    setGoal(myActuators,RHR,.25)
    setGoal(myActuators,RAR,.25)
    setGoal(myActuators,LAR,.25)
    net.synchronize()
    time.sleep(1)

#<PHASE 12>STRAIGHTEN UP RIGHT LEG
    amount=0.1
    while(amount<=.72):
        setGoal(myActuators,RKN,-1.44 + 2*amount)
        setGoal(myActuators,RAP,0.72 - amount)
        net.synchronize()		
        time.sleep(0.5)
        amount +=0.12
    net.synchronize()
    time.sleep(1)

#<PHASE 13>INCREASE SPACING BETWEEN LEGS TO AVOID LEFT LEG
#	  GETTING CAUGHT ON TOP OF RIGHT FOOT. THIS IS A
#	  WORK AROUND THAT IS PARTICULAR TO A REAL-WORLD
#	  IMPERFECTION OF OUR BIOLOID LEGS
    setGoal(myActuators,RHR,0)
    net.synchronize()		
    time.sleep(1)

#<PHASE 14>MAKE RIGHT LEG COMPLETELY STRAIGHT
    amount=0
    while(amount<=.4):
        setGoal(myActuators,RHP,-0.4 + amount)
        net.synchronize()		
        time.sleep(0.5)
        amount +=0.1
    net.synchronize()
    time.sleep(1)

#<PHASE 15>STRAIGHTEN LEFT LEG
    amount=0
    while(amount<=.36):
       setGoal(myActuators,LHP,0.72 - amount)
       setGoal(myActuators, LKN, 1.44 - 2*amount)
       setGoal(myActuators, LAP, -0.72 + amount)
       net.synchronize()		
       time.sleep(0.4)
       amount +=0.12
    net.synchronize()
    time.sleep(1)

#<PHASE 16>MAKE RHR MATCH LHR AGAIN NOW THAT LEGS HAVE BEEN
#	  SUCCESSFULLY STRAIGHTENED
    setGoal(myActuators,RHR,0.25)
    net.synchronize()		
    time.sleep(1)

#<PHASE 15>STRAIGHTEN LEFT LEG
    amount=0
    while(amount<=.36):
       setGoal(myActuators,LHP,0.36 - amount)
       setGoal(myActuators, LKN, 0.72 - 2*amount)
       setGoal(myActuators, LAP, -0.36 + amount)
       net.synchronize()		
       time.sleep(0.4)
       amount +=0.12
    net.synchronize()
    time.sleep(1)

#<PHASE 17>MOVE CENTER OF MASS TO MIDDLE    
    setGoal(myActuators,LHR,0)
    setGoal(myActuators,RHR,0)
    setGoal(myActuators,RAR,0)
    setGoal(myActuators,LAR,0)
    net.synchronize()
    time.sleep(1)



def validateInput(userInput, rangeMin, rangeMax):
    '''
    Returns valid user input or None
    '''
    try:
        inTest = int(userInput)
        if inTest < rangeMin or inTest > rangeMax:
            print "ERROR: Value out of range [" + str(rangeMin) + '-' + str(rangeMax) + "]"
            return None
    except ValueError:
        print("ERROR: Please enter an integer")
        return None
    
    return inTest

if __name__ == '__main__':
    
    parser = optparse.OptionParser()
    parser.add_option("-c", "--clean",
                      action="store_true", dest="clean", default=False,
                      help="Ignore the settings.yaml file if it exists and \
                      prompt for new settings.")
    
    (options, args) = parser.parse_args()
    
    # Look for a settings.yaml file
    settingsFile = 'settings.yaml'
    if not options.clean and os.path.exists(settingsFile):
        with open(settingsFile, 'r') as fh:
            settings = yaml.load(fh)
    # If we were asked to bypass, or don't have settings
    else:
        settings = {}
        if os.name == "posix":
            portPrompt = "Which port corresponds to your USB2Dynamixel? \n"
            # Get a list of ports that mention USB
            try:
                possiblePorts = subprocess.check_output('ls /dev/ | grep -i usb',
                                                        shell=True).split()
                possiblePorts = ['/dev/' + port for port in possiblePorts]
            except subprocess.CalledProcessError:
                sys.exit("USB2Dynamixel not found. Please connect one.")
                
            counter = 1
            portCount = len(possiblePorts)
            for port in possiblePorts:
                portPrompt += "\t" + str(counter) + " - " + port + "\n"
                counter += 1
            portPrompt += "Enter Choice: "
            portChoice = None
            while not portChoice:                
                portTest = raw_input(portPrompt)
                portTest = validateInput(portTest, 1, portCount)
                if portTest:
                    portChoice = possiblePorts[portTest - 1]

        else:
            portPrompt = "Please enter the port name to which the USB2Dynamixel is connected: "
            portChoice = raw_input(portPrompt)
    
        settings['port'] = portChoice
        
        # Baud rate
        baudRate = None
        while not baudRate:
            brTest = raw_input("Enter baud rate [Default: 1000000 bps]:")
            if not brTest:
                baudRate = 1000000
            else:
                baudRate = validateInput(brTest, 9600, 1000000)
                    
        settings['baudRate'] = baudRate
        
        # Servo ID
        highestServoId = None
        while not highestServoId:
            hsiTest = raw_input("Please enter the highest ID of the connected servos: ")
            highestServoId = validateInput(hsiTest, 1, 255)
        
        settings['highestServoId'] = highestServoId
        
        # Save the output settings to a yaml file
        with open(settingsFile, 'w') as fh:
            yaml.dump(settings, fh)
            print("Your settings have been saved to 'settings.yaml'. \nTo " +
                   "change them in the future either edit that file or run " +
                   "this example with -c.")
    
    main(settings)

