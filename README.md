# WRO-2022-Future-Engineers
Main.py is a separate program. It exchanges data packets with the qualification.py or final.py program (depending on which program is currently running). Pyboard processes the received data and, depending on the values that were in the data packet, changes the servo angle or speed. If the button is pressed, then it sends information about it.

RobotAPI.py - a special class that creates our robot as an object

start_robot.py is a program that creates a standalone application with which you can interact with the RasberryPi over a Wi-Fi network. To do this, you need to connect to a Wi-Fi network (in our case, "Car1"). Then run the program itself and by clicking on the "Connect to robot" button select the ip address of our RasberryPi. The app's interface has several main features.
1. Load start: Allows you to select a program to download and run on your RasberryPi.
2. Start: Starts the last program loaded on RasberryPi.
3. Stop: Terminates the execution of the program on the RasberryPi.
4. Video: Displays the image from the camera.
The application also reports errors in the program, if any.



