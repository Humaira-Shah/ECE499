import dynamixel
import time
from DynDefs import *

def TurnRight(net,myActuators):
#    #print "#<PHASE 1> Shift weight to left foot." 
    setGoal(myActuators,LHR,-.22)
    setGoal(myActuators,RHR,-.22)
    setGoal(myActuators,RAR,-.22)
    setGoal(myActuators,LAR,-.22)
    net.synchronize()
    time.sleep(1)

#    #print "#<PHASE 2>lift right foot."
    amount=0
    while(amount<=.72):
        setGoal(myActuators,RHP,-amount)
        setGoal(myActuators,RKN,-2*amount)
        setGoal(myActuators,RAP,amount)
        net.synchronize()		
        time.sleep(0.3)
        amount +=0.12
    net.synchronize()
    time.sleep(1)
   
#    #print "#<PHASE 3>turning right leg 30 degrees outward."
    amount=0
    while(amount<=.52):
        setGoal(myActuators,RHY,(-.78+amount))
        net.synchronize()		
        time.sleep(0.3)
        amount +=0.26
    net.synchronize()
    time.sleep(1)
    
 #   #print "#<PHASE 4>Straightening right leg"    
    amount=0
    while(amount<=.72):
        setGoal(myActuators,RHP,(-.72 + amount))
        setGoal(myActuators,RKN,(-1.44 + (2*amount)))
        setGoal(myActuators,RAP,((.72) - amount))
        net.synchronize()		
        time.sleep(0.3)
        amount +=0.12
    time.sleep(.5)
    net.synchronize()
    
#    #print "shifting center of mass "
    setGoal(myActuators,LHR,0)
    setGoal(myActuators,RHR,0)
    setGoal(myActuators,RAR,0)
    setGoal(myActuators,LAR,0)
    net.synchronize()
 #   time.sleep(1)
#    #print "shifting weight to right "
    setGoal(myActuators,LHR,.22)
    setGoal(myActuators,RHR,.22)
    setGoal(myActuators,RAR,.22)
    setGoal(myActuators,LAR,.22)
    net.synchronize()
    time.sleep(1)

#    #print" #<PHASE 6> Lifting left foot"
    amount=0
    while(amount<=.82): 
        setGoal(myActuators,LHP,amount)
        setGoal(myActuators,LKN,2*amount)
        setGoal(myActuators,LAP,-amount)
        net.synchronize()		
        time.sleep(0.4)
        amount +=0.1
    net.synchronize()
    time.sleep(1)

#    #print "#<PHASE 7> straightening right leg yaw"
    amount=0
    while(amount<=.52):
        setGoal(myActuators,RHY,((-.26) - amount))
        net.synchronize()		
        time.sleep(0.3)
        amount +=0.26
    net.synchronize()
    time.sleep(1)
 #   #print "giving some space"
    setGoal(myActuators,LHR,.32)
    net.synchronize()	
#    #print "#<PHASE 8> straightening left leg"
    amount=0
    while(amount<=.82):
        setGoal(myActuators,LHP,0.82 - amount)
        setGoal(myActuators,LKN,1.64 - (2*amount))
        setGoal(myActuators,LAP, -0.82 + amount)
        net.synchronize()		
        time.sleep(0.3)
        amount +=0.1
    net.synchronize()
    time.sleep(1)
    #print "#<PHASE X> Go back to reset position"
    for actuator in myActuators:
        if actuator.id==RHY or actuator.id==LHY:
	    actuator.goal_position = rad2dyn(-.78)
        else:
            actuator.goal_position = rad2dyn(0)
    net.synchronize()
    time.sleep(3)


