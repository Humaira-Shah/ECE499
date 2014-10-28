directory contains the file necessary to make distance calculation, distance result is printed to the terminal that the process of the distance calculation file is running in, the program file is name template-qStereoCam-Shah.py


also included is necessary files to include with hw3 code in order to properly send velocity packets to robot


hw3 controller is at the following link: https://github.com/Humaira-Shah/ECE499/tree/master/hw3


Note that the distance calculation result is only calculated when object is between the pinhole cameras horiizontally and is visible by both pinhole cameras. When the object is not between both pinhole cameras, for example it is to the left of both pinholes horizontally or to the right of both pinholes horiizontally, the distance is not calculated. I did not go over this case because I was unsure of how to deal with the object being fully visible in one pinhole image and only partially visible in the other pinhole image, this would mean that the center of the object, calculated using color, would not actually map to the same physical point on the object, which would lead to false calculations.
