# MIDTERM 2 QUESTION 3C
# Make a Python function that takes in the joint lengths and angles
# and outputs the x,y location (each input should be two vectors,
# one if the joint lengths and one of the joint angle). Use it to
# find the x,y location for the following sets of kinematic and
# joint space values. Write the answer for each set below the
# corresponding table (in the x=,y= area). Post code on
# GitHub and submit on blackboard.

from math import *

def q3c(L,THETA):

	x = (L[0]*cos(THETA[0])) + (L[1]*cos(THETA[0]+THETA[1])) + (L[2]*cos(THETA[0]+THETA[1]+THETA[2])) + (L[3]*cos(THETA[0]+THETA[1]+THETA[2]+THETA[3])) + (L[4]*cos(THETA[0]+THETA[1]+THETA[2]+THETA[3]+THETA[4])) + (L[5]*cos(THETA[0]+THETA[1]+THETA[2]+THETA[3]+THETA[4]+THETA[5])) + (L[6]*cos(THETA[0]+THETA[1]+THETA[2]+THETA[3]+THETA[4]+THETA[5]+THETA[6]))+ (L[7]*cos(THETA[0]+THETA[1]+THETA[2]+THETA[3]+THETA[4]+THETA[5]+THETA[6]+THETA[7]))+ (L[8]*cos(THETA[0]+THETA[1]+THETA[2]+THETA[3]+THETA[4]+THETA[5]+THETA[6]+THETA[7]+THETA[8]))

	y = (L[0]*sin(THETA[0])) + (L[1]*sin(THETA[0]+THETA[1])) + (L[2]*sin(THETA[0]+THETA[1]+THETA[2])) + (L[3]*sin(THETA[0]+THETA[1]+THETA[2]+THETA[3])) + (L[4]*sin(THETA[0]+THETA[1]+THETA[2]+THETA[3]+THETA[4])) + (L[5]*sin(THETA[0]+THETA[1]+THETA[2]+THETA[3]+THETA[4]+THETA[5])) + (L[6]*sin(THETA[0]+THETA[1]+THETA[2]+THETA[3]+THETA[4]+THETA[5]+THETA[6]))+ (L[7]*sin(THETA[0]+THETA[1]+THETA[2]+THETA[3]+THETA[4]+THETA[5]+THETA[6]+THETA[7]))+ (L[8]*sin(THETA[0]+THETA[1]+THETA[2]+THETA[3]+THETA[4]+THETA[5]+THETA[6]+THETA[7]+THETA[8]))

	print x
	print y

	return [x,y]

