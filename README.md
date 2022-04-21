# WRO-2022-Future-Engineers
main.py is a separate program. It is on pyboard.
It exchanges data packets with the qualification.py or final.py program (depending on which program is currently running).
Pyboard processes the received data and, depending on the values ​​that were in the data packet, changes the servo angle and speed.
If the button is pressed, then it sends information about it.

RobotAPI.py - a special class that creates our robot as an object, allows you to read the image from the camera and display it on the laptop screen.

start_robot.py is a program that creates a standalone application with which you can interact with the RasberryPi over a Wi-Fi network.
To do this, you need to connect to a Wi-Fi network (in our case, "Car1").
Then run the program itself and by clicking on the "Connect to robot" button select the ip address of our RasberryPi.
The app's interface has several main features.
1. Load start: Allows you to select a program to download and run on your RasberryPi.
2. Start: Starts the last program loaded on RasberryPi.
3. Stop: Terminates the execution of the program on the RasberryPi.
4. Video: Displays the image from the camera.
The application also reports errors in the program, if any.

autostart.py is a program that starts automatically after turning on the RasberryPi. It launches any program whose name is written in the code after import.
In order for any program (in our case, qualification.py and final.py) to start after turning on the RasberryPi, you need to load this program through the start_robot.py application and then load the autostart.py program.

qualification.py is the program for the qualification stage. It is on Rasberry Pi. The program processes the image from the camera using the cv2 library. It recognizes the black walls of the field and determines how much the robot deviated from the intended route, determines the error. Next, we calculate the angle by which the servo motor needs to be rotated using the formulas:
u = e * kp + (e - e_old) * kd
deg = rul - u,
where deg - desired angle of rotation of the servomotor; rul - the initial angle of rotation of the servo motor, at which the wheels are aligned; u - difference between rul and deg; e - error; kp - coefficient of proportional regulation; kd - coefficient of differential regulation; e_old - past error(e) which is updated with each iteration of the loop.
After mathematical calculations, we send deg and speed (speed, we have it constant) to the pyboard via UART. This data is received by the main.py program.
Also, the program counts how many turns the robot has passed, and after 12 turns, that is, 3 laps, it stops. The sensors cannot recognize the turn, but they can recognize the blue and orange lines, they are on the turns.

final.py is the final stage program. It is on Rasberry Pi. final.py, like qualification.py, aligns the robot to the center and counts the laps it has completed, but also allows the robot to avoid traffic signs - green and red boxes. The robot circles the green ones on the left side and the red ones on the right side.
The program recognizes objects using a sensor, and if it notices a box, it adjusts its route so as to bypass the road sign on the right side.















