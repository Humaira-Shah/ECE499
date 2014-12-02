
import dynamixel
import time
from DynDefs import *

def WalkBackward(net,myActuators):
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


