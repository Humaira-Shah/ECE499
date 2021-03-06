import numpy as np
import math

def getJointSpace(goalX, goalY):

	#Arm piece lengths
	L1 = 0.3
	L2 = 0.2

	#initial calculation
	xinitial = 0.3 + 0.2 #arm lies on x axis
	yinitial = 0
	thetaInitial1 = 0
	thetaInitial2 = 0

	iterations = 0
	tolerance = 0.05
	Beta = 0.1 #fraction of delta e to get to goal position
	angleChange = 0.05

	goalminX = goalX - tolerance
	goalminY = goalY - tolerance
	goalmaxX = goalX + tolerance
	goalmaxY = goalY + tolerance

	currentX = xinitial # current end effector x coord
	currentY = yinitial # current end effector y coord
	currentTheta1 = thetaInitial1
	currentTheta2 = thetaInitial2

	# keep iterating until we are in tolerance range of goal position
	while(not((currentX>=goalminX) and (currentX<=goalmaxX) and (currentY>=goalminY) and (currentY<=goalmaxY))):
		Jparam1 = currentX/angleChange #end effector coord x
		Jparam2 = (currentX - L1*math.cos(currentTheta1))/angleChange #end effector coord x minus coord x of joint where L1 and L2 connect
		Jparam3 = currentY/angleChange #end effector coord y
		Jparam4 = (currentY - L1*math.sin(currentTheta1))/angleChange #end effector coord y minus coord y of joint where L1 and L2 connect

		Jmatrix = np.array([[Jparam1,Jparam2],[Jparam3,Jparam4]]) #Jacobian matrix J(e,theta)

		dex = Beta * (goalX - currentX) #small change in ee coord to get to goal x
		dey = Beta * (goalY - currentY) #small change in ee coord to get to goal y

		de = np.array([[dex],[dey]]) #delta e matrix

		# get dtheta = transpose(Jmatrix) * de
		# where * means dot matrix product
		# We are actually supposed to invert the Jmatrix but the transpose
		# can work with less quality
		dtheta = np.dot((Jmatrix.T),de) # where top parameter is dtheta1 and bottom parameter is dtheta2
		
		currentTheta1 = currentTheta1 + dtheta.item(0)
		currentTheta2 = currentTheta2 + dtheta.item(1)
		iterations = iterations + 1

		# use forward kinematics to update current end effector position
		currentX = (L1*math.cos(currentTheta1))+(L2*math.cos(currentTheta1+currentTheta2))
		currentY = (L1*math.sin(currentTheta1))+(L2*math.sin(currentTheta1+currentTheta2))

		print str(currentX) + "\n"
		print currentY

	return [currentTheta1,currentTheta2]	





