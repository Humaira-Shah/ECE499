# QUESTION 4f
# Implement the Jacobian IK method for the manipulator. You may use python or matlab.
# Your function must take in a goal x,y position and output the joint space solution.
# The kinematic values are listed below.

# Kinematic values
# L1 = 0.3m
# L2 = 0.2m

import JIK2DOF as JIK

# x,y

# Set1
# 0.1,0.1
answer = JIK.getJointSpace(0.1,0.1)
print "Set 1 Theta 1: "+str(answer[0])
print "Set 1 Theta 2: "+str(answer[1])
print "\n"

meow = input("NEXT SET?")

# Set2
# 0.2,0.2
answer = JIK.getJointSpace(0.2,0.2)
print "Set 2 Theta 1: "+str(answer[0])
print "Set 2 Theta 2: "+str(answer[1])
print "\n"

meow = input("NEXT SET?")

# Set3
# 0.3,0.3
answer = JIK.getJointSpace(0.3,0.3)
print "Set 3 Theta 1: "+str(answer[0])
print "Set 3 Theta 2: "+str(answer[1])
print "\n"

meow = input("NEXT SET?")

# Set4
# 0.0,0.3
answer = JIK.getJointSpace(0.0,0.3)
print "Set 4 Theta 1: "+str(answer[0])
print "Set 4 Theta 2: "+str(answer[1])
print "\n"

meow = input("NEXT SET?")

# Set5
# -0.1,0.1
answer = JIK.getJointSpace(-0.1,0.1)
print "Set 5 Theta 1: "+str(answer[0])
print "Set 5 Theta 2: "+str(answer[1])
print "\n"

meow = input("NEXT SET?")

# Set6
# -0.2,0.2
answer = JIK.getJointSpace(-0.2,0.2)
print "Set 6 Theta 1: "+str(answer[0])
print "Set 6 Theta 2: "+str(answer[1])
print "\n"

meow = input("NEXT SET?")

# Set7
# 0.3,-0.2
answer = JIK.getJointSpace(0.3,-0.2)
print "Set 7 Theta 1: "+str(answer[0])
print "Set 7 Theta 2: "+str(answer[1])
print "\n"

meow = input("NEXT SET?")

# Set8
# 0.3,0.8
answer = JIK.getJointSpace(0.3,0.8)
print "Set 8 Theta 1: "+str(answer[0])
print "Set 8 Theta 2: "+str(answer[1])
print "\n"
