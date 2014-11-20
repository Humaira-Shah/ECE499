% MIDTERM 2 QUESTION 3E
% Using the transformation matrix method find the resulting transformation
% matrix  for the robot arm in part 3c using the values in "Set 2." Calculate
% and circle the following:
%				1) the resulting transformation matrix
%				2) the x,y location of the end effector
%				3) [extra credit] the rotation about x,y, and z in rad.

l1 = 0.1
l2 = 0.1
l3 = 0.1
l4 = 0.1
l5 = 0.1
l6 = 0.1
l7 = 0.1
l8 = 0.1
l9 = 0.1

DX01 = [1 0 0 l1; 0 1 0 0; 0 0 1 0; 0 0 0 1]
DX12 = [1 0 0 l2; 0 1 0 0; 0 0 1 0; 0 0 0 1]
DX23 = [1 0 0 l3; 0 1 0 0; 0 0 1 0; 0 0 0 1]
DX34 = [1 0 0 l4; 0 1 0 0; 0 0 1 0; 0 0 0 1]
DX45 = [1 0 0 l5; 0 1 0 0; 0 0 1 0; 0 0 0 1]
DX56 = [1 0 0 l6; 0 1 0 0; 0 0 1 0; 0 0 0 1]
DX67 = [1 0 0 l7; 0 1 0 0; 0 0 1 0; 0 0 0 1]
DX78 = [1 0 0 l8; 0 1 0 0; 0 0 1 0; 0 0 0 1]
DX89 = [1 0 0 l9; 0 1 0 0; 0 0 1 0; 0 0 0 1]



%toRadians = 0.0174532925

theta1 = 0.1
theta2 = 0.1
theta3 = 0.1
theta4 = 0.1
theta5 = 0.1
theta6 = 0.1
theta7 = 0.1
theta8 = 0.1
theta9 = 0.1

RZ01 = [cos(theta1) -sin(theta1) 0 0; 
        sin(theta1) cos(theta1)  0 0;
        0           0            1 0;
        0           0            0 1]

RZ12 = [cos(theta2) -sin(theta2) 0 0; 
        sin(theta2) cos(theta2)  0 0;
        0           0            1 0;
        0           0            0 1]

RZ23 = [cos(theta3) -sin(theta3) 0 0; 
        sin(theta3) cos(theta3)  0 0;
        0           0            1 0;
        0           0            0 1]

RZ34 = [cos(theta4) -sin(theta4) 0 0; 
        sin(theta4) cos(theta4)  0 0;
        0           0            1 0;
        0           0            0 1]

RZ45 = [cos(theta5) -sin(theta5) 0 0; 
        sin(theta5) cos(theta5)  0 0;
        0           0            1 0;
        0           0            0 1]

RZ56 = [cos(theta6) -sin(theta6) 0 0; 
        sin(theta6) cos(theta6)  0 0;
        0           0            1 0;
        0           0            0 1]

RZ67 = [cos(theta7) -sin(theta7) 0 0; 
        sin(theta7) cos(theta7)  0 0;
        0           0            1 0;
        0           0            0 1]

RZ78 = [cos(theta8) -sin(theta8) 0 0; 
        sin(theta8) cos(theta8)  0 0;
        0           0            1 0;
        0           0            0 1]

RZ89 = [cos(theta9) -sin(theta9) 0 0; 
        sin(theta9) cos(theta9)  0 0;
        0           0            1 0;
        0           0            0 1]

T01 = RZ01 * DX01

T12 = RZ12 * DX12

T23 = RZ23 * DX23

T34 = RZ34 * DX34

T45 = RZ45 * DX45

T56 = RZ56 * DX56

T67 = RZ67 * DX67

T78 = RZ78 * DX78

T89 = RZ89 * DX89

T = T01 * T12 * T23 * T34 * T45 * T56 * T67 * T78 * T89
