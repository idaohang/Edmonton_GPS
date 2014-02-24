Project Description:
This project allows a user to view a map of Edmonton on an Arduino with an lcd and joystick attached. The viewer can select their current location and target destination. This information is then sent back to the server which calculates the ideal route through Edmonton using Dijkstra's algorithm. To route is then sent back and displayed on the screen to the client.

Contributors:
This project was completed by Michael Nicholson and Monir Imamverdi. We collaborated with Cameron Alexander and Chun-Han Lee on the first part of the assignment, but not very much at all on this half of the assignment.

Usage Instructions:
To build the project connect your Arduino (and ensure it is wired as was done in class and specified by the wiring guide) to the computer and go into the 'client' directory. In this directory issue the 'make upload' command in the terminal.

Next, change into the 'server' directory and issue the command:

python3 server.py -s /dev/ttyACM0

At this point you should be able to use the joystick and buttons to maneuver about the map and select points. You can now click the joystick in to select points and the route will be plotted on the map with a thin blue line!

Enjoy your new navigation abilities. Feel free to throw away your GPS! 

Authorship Note:

The code in the server directory was written by myself or my partners; however, a lot of the code within the client directory was written by the Professors and TAs of the course and was modified by myself or my partners to get the project to work.
