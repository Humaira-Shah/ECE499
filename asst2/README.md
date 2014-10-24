//HOW TO RUN:
--------------------------------------------------


	//COMMANDS


	$ python asst2.py


	$ python PID.py


//HOW TO CLOSE:
--------------------------------------------------


	//click on 'img' cv window


	//press and hold escape key


//DEFINE YOUR UPDATE RATE AND WHY YOU CHOSE IT
---------------------------------------------------


// asst2.py reads the camera feed and shows the 'img' window, it also gets the errorFound and prints a red dot and coordinates at the center of the blue box in the cv window.


// asst2.py updates as fast as it can and therefore there is no limit on the update rate. I did this so that the process would get a new error value as soon as possible so that PID.py could have new data as fast as possible.


// PID.py is the controller which gets the errorFound from asst2.py and uses a P controller to command the robot to turn clockwise or counterclockwise at some velocity, this process has an update rate of 20HZ that utilizes the sim time in order to mandate the update rate. I chose the 20HZ update rate because it was the fastest one I could get that was stable, with higher update rates the sim time was lagging behind what it should be at every loop due to the rate being too fast in comparison to how fast the code could execute.


// I wanted to choose the fastest update rate that was stable in order to have the robot react as quickly as possible while still maintaining an appropriate delay for the robot actuators to actually do what was requested of them that is why I chose the 20HZ update rate for PID.py 


//YOUTUBE VIDEO LINKS
-----------------------------------------------------


PART(1/2) https://www.youtube.com/watch?v=BV4rsIRDE2I


PART(2/2) https://www.youtube.com/watch?v=QXHPq0jpe-U
