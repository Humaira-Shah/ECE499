HOW TO RUN
-------------------


//connect TTL-USB USB side to computer with TTL connected to actuators of bioloid


//in terminal type the following command but replace /dev/ttyUSB0 with the appropriate name for the USB connector


sudo chmod 777 /dev/ttyUSB0


python main.py



HOW TO USE
-----------------


After running, follow menu direction to move bioloid. Program will not register new commands while the bioloid is in the process of completing an old command.
