import dynamixel
import time
from DynDefs import *



def WalkForward(net,myActuators):

#<PHASE 1>bend our knees first!!!
    setGoal(myActuators,LHP,.42)
    setGoal(myActuators,LKN,.84)
    setGoal(myActuators,LAP,-.42)

    setGoal(myActuators,RHP,-.42)
    setGoal(myActuators,RKN,-.84)
    setGoal(myActuators,RAP,.42)
    net.synchronize()
 #   time.sleep(1)
#<PHASE 2> move over to the right foot
    setGoal(myActuators,LHR,.22)
    setGoal(myActuators,RHR,.22)
    setGoal(myActuators,RAR,.22)
    setGoal(myActuators,LAR,.22)
    net.synchronize()
    time.sleep(1)
#<PHASE 3> move the left leg into the air
    amount=0.42
    while(amount<=.72):
        setGoal(myActuators,LHP,amount)
        setGoal(myActuators,LKN,2*amount)
        setGoal(myActuators,LAP,-amount)
        net.synchronize()		
        time.sleep(0.3)
        amount +=0.1
    #time.sleep(1)
    setGoal(myActuators,RHP,-0.42)
    net.synchronize()
    time.sleep(1)
    
    
#<PHASE 4> Put The left Leg down more forward
    setGoal(myActuators,LKN,1.0)
    setGoal(myActuators,LAP,-.42)
    net.synchronize()		
    time.sleep(1)

#<PHASE 5> move the hips to move the center of mass to middle    
    setGoal(myActuators,LHR,0)
    setGoal(myActuators,RHR,0)
    setGoal(myActuators,RAR,0)
    setGoal(myActuators,LAR,0)
    net.synchronize()
    time.sleep(1)
#<PHASE 6> move the hips to move the center of mass to the left foot    
    setGoal(myActuators,LHR,-.22)
    setGoal(myActuators,RHR,-.22)
    setGoal(myActuators,RAR,-.22)
    setGoal(myActuators,LAR,-.22)
    net.synchronize()
    time.sleep(1)
    #print "Phase 5 fin"
#<PHASE 7> Move the right leg into the air
    amount=0.42
    while(amount<=.82):
        setGoal(myActuators,RHP,-amount)
        if(2*amount>1.1):
            setGoal(myActuators,RKN,-2*amount)
        setGoal(myActuators,RAP,amount)
        net.synchronize()		
        time.sleep(0.3)
        amount +=0.1
  #  time.sleep(1)
    setGoal(myActuators,LHP,0.42)
    setGoal(myActuators,LAP,-0.42)
    net.synchronize()
    time.sleep(1)
    #print "Phase 6 fin"
#<PHASE 8> Put the right leg down more forward then before
    setGoal(myActuators,RKN,-1.2)
    setGoal(myActuators,RAP,0.35)
    net.synchronize()		
    time.sleep(1)
    #print "Phase 7 fin"
#<PHASE 9> move the hips to move the center of mass to middle    
    setGoal(myActuators,LHR,0)
    setGoal(myActuators,RHR,0)
    setGoal(myActuators,RAR,0)
    setGoal(myActuators,LAR,0)
    net.synchronize()
    time.sleep(1)

    amount=0.42;
    while(amount<=.62):
        setGoal(myActuators,LHP,amount)
        if(2*amount>1.1):
            setGoal(myActuators,LKN,2*amount)
        setGoal(myActuators,LAP,-amount)
        net.synchronize()		
        time.sleep(0.3)
        amount +=0.1
    time.sleep(1)
#<PHASE 10> move the hips to move the center of mass to right foot    
    setGoal(myActuators,LHR,.22)
    setGoal(myActuators,RHR,.22)
    setGoal(myActuators,RAR,.22)
    setGoal(myActuators,LAR,.22)
    net.synchronize()
    time.sleep(1)
    #print "Phase 8 fin"
#<PHASE 11> Move the left leg into the air
    amount=0.62;
    while(amount<=.82):
        setGoal(myActuators,LHP,amount)
        if(2*amount>1.1):
            setGoal(myActuators,LKN,2*amount)
        setGoal(myActuators,LAP,-amount)
        net.synchronize()		
        time.sleep(0.3)
        amount +=0.1
 #   time.sleep(1)
    setGoal(myActuators,RHP,-0.42)
    setGoal(myActuators,RAP,0.42)
    net.synchronize()
    time.sleep(1)
    setGoal(myActuators,RHR,0.0)
    #print "Phase 9 fin"
#<PHASE 12> Put the left leg down more forward then before
    setGoal(myActuators,LHP,.42)
    setGoal(myActuators,LKN,1.2)
    setGoal(myActuators,LAP,-0.42)
    net.synchronize()		
    time.sleep(1)

    setGoal(myActuators,LKN,0)
    setGoal(myActuators,RKN,0)
    net.synchronize()	
    time.sleep(1)

    #print "Phase 10 fin"
    for actuator in myActuators:
        if actuator.id==RHY or actuator.id==LHY:
	    actuator.goal_position = rad2dyn(-.78)
        else:
            actuator.goal_position = rad2dyn(0)
    net.synchronize()
    time.sleep(2)


