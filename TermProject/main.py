import os
import dynamixel
import time
import random
import sys
import subprocess
import optparse
import yaml
import numpy as np
import curses
from DynDefs import *
from ForwardWalk import *
from BackwardsWalk import *
from TurnLeft import *
from TurnRight import *

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
    #set the starting position, standing straight
    for actuator in myActuators:
		if actuator.id==RHY or actuator.id==LHY:
			actuator.goal_position = rad2dyn(-.78)
		else:
			actuator.goal_position = rad2dyn(0)
    net.synchronize()
    time.sleep(3)
    try:

        stdscr = curses.initscr()
        curses.cbreak()
        stdscr.keypad(1)
        stdscr.addstr(0,2,"Here are a list of the keys that can be pressed and what they do:")
        stdscr.addstr(2,2,"w: Walk Forward")
        stdscr.addstr(3,2,"s: Walk Backward")
        stdscr.addstr(4,2,"a: Turn Left")
        stdscr.addstr(5,2,"d: Turn Right")
        stdscr.addstr(6,2,"q: Exit Program")
        stdscr.refresh()
        key = ''

        while key != ord('q'):
            stdscr.addstr(10,2," ")
            curses.flushinp()
            key = stdscr.getch()
            

        #w
            if key == 119:
                stdscr.addstr(8,10,"Walking Forward             ")
                stdscr.refresh()
                WalkForward(net,myActuators)
                stdscr.addstr(8,10,"Finished Walking Forward    ")
        #s
            elif key == 115: 
                stdscr.addstr(8,10,"Walking Backward            ")
                stdscr.refresh()
                WalkBackward(net,myActuators)
                stdscr.addstr(8,10,"Finished Walking Backward   ")

        #a
            elif key == 97: 
                stdscr.addstr(8,10,"Turning Left                ")
                stdscr.refresh()
                TurnLeft(net,myActuators)
                stdscr.addstr(8,10,"Finished Turning Left       ")

        #d
            elif key == 100:
                stdscr.addstr(8,10,"Turning Right               ")
                stdscr.refresh()
                TurnRight(net,myActuators)
                stdscr.addstr(8,10,"Finished Turning Right      ")
            stdscr.addstr(10,2," ")
            stdscr.refresh()
        curses.endwin()   
    except:
        curses.endwin()
        print "error occurred."

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

