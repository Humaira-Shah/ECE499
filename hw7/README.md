YOUTUBE LINKS
----------------


RIGHT ARM FRONT VIEW: https://www.youtube.com/watch?v=sn-dmY5FBHo

RIGHT ARM SIDE VIEW: https://www.youtube.com/watch?v=r9Sa5mQjVgQ

RIGHT ARM CARTESIAN VIEW: https://www.youtube.com/watch?v=EQrUS1ZTui8


LEFT ARM (EXTRA CREDIT) FRONT VIEW: https://www.youtube.com/watch?v=Z-I-2gBTG4I

LEFT ARM (EXTRA CREDIT) SIDE VIEW: https://www.youtube.com/watch?v=AHNXUJZXevw

LEFT ARM (EXTRA CREDIT) CARTESIAN VIEW: https://www.youtube.com/watch?v=q5GcZqJf0RI


DISCUSS (5-10 sentences) WHY YOU CHOSE THIS METHOD AND THE PROCESS YOU DID TO IMPLEMENT THIS
----------------------------------


In order to accomplish the task of having the arm of hubo move to the coordinates specified in the text file given, I used inverse kinematics, but I only worked with two dimensions at a time. I did this by first working just with the x,z plane. I determined the distance from hubo's neck (the origin) to the midshoulder of hubo using the kinematic structure for hubo pdf. I found that the midshoulder of the right arm was at x = -214 millimeters from the origin. Then for a given point, I determined the angle shoulder roll necessary to get the arm of hubo pointing such that it was in the appropriate z,y plane for the next computation. I got the shoulder roll angle by using trigonometry, arctan((xpoint - xmidshoulder)/zpoint) + alpha. The alpha added was the necessary RSR to be applied in order to get the arm parallel to the torso. Alpha was found using the hubo-ach console to straighten the arm out.

After applying the shoulder roll angle, I dealt with the shoulder pitch and elbow bend angles by working in the z,y plane. I used the following equations derived in class: 


elbowBend = -(math.acos(((z*z) + (y*y) - (d1*d1) - (d2*d2))/(2*d1*d2)))


and


shoulderPitch = (-(math.atan((yoverz-theta3)/(1+(yoverz*theta3)))) - 1.570796)


for elbow bend, you must have noticed that the formula derived in class is negated, this was found necessary in order to have the hubo elbow bend in the proper direction. For shoulderPitch as well this was also necessary, but not only that, 90 degrees (1.570796 radians) had to be subtracted from the formula derived in order to have the arm aligned with the z axis in the z,y plane. This is because at startup the hubo arm is pointed downward along the y-axis, therefore the need to offset the pitch by 90 degrees. We are subtracting instead of adding the 90 degrees because the arm lifts in front of hubo when negative angles are applied to the shoulder pitch, and backwards when positive angles are applied to the shoulder pitch.


Alternatively, for the extra credit, the process was the same except the x coordinates of the text file had to be negated and the angle applied to shoulder roll LSR was positive. 
