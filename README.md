# Description of the algorithms
![main.py](https://github.com/BogdusUltra/WRO-2022-Future-Engineers/blob/main/main.py) is a separate programme. It resides on the pyboard.
It exchanges data packets with ![qualification.py](https://github.com/BogdusUltra/WRO-2022-Future-Engineers/blob/main/qualification.py) or ![final.py](https://github.com/BogdusUltra/WRO-2022-Future-Engineers/blob/main/final.py) (depending on which program is running on the Raspberry Pi) UART way.
Pyboard processes the received data and depending on the values that were in the data packet, it changes the servo angle and speed.
If the button is pressed it sends information about this.

![RobotAPI.py](https://github.com/BogdusUltra/WRO-2022-Future-Engineers/blob/main/RobotAPI.py) is a special class that creates our robot as an object, it can read out the image from the camera and display it on the laptop screen.

![start_robot.py](https://github.com/BogdusUltra/WRO-2022-Future-Engineers/blob/main/start_robot.py) is a program that creates a separate application that can be used to communicate with the Raspberry Pi via the Wi-Fi network.
To do this, you need to connect to the Raspberry Pi via Wi-Fi (in our case "Car1").
Then launch the application itself and by pressing the "Connect to robot" button select the ip address of our Raspberry Pi.
There are several main functions in the application interface.
1. Load start: allows you to select the software to load and run on your Raspberry Pi.
2. Start: starts the last programme downloaded to the Raspberry Pi.
3. Stop: finishes execution of the program on Raspberry Pi.
4. Video: creates a separate window and displays the camera image there.
The application also reports errors in the program, if any.

![autostart.py](https://github.com/BogdusUltra/WRO-2022-Future-Engineers/blob/main/autostart.py) is a programme that runs automatically as soon as RaspberryPi is switched on. It executes any program whose name appears in the code after import.
For any program (![qualification.py](https://github.com/BogdusUltra/WRO-2022-Future-Engineers/blob/main/qualification.py) and ![final.py](https://github.com/BogdusUltra/WRO-2022-Future-Engineers/blob/main/final.py) in this case) to run when Raspberry Pi is switched on, we need to load it with ![start_robot.py](https://github.com/BogdusUltra/WRO-2022-Future-Engineers/blob/main/start_robot.py) and then load ![autostart.py](https://github.com/BogdusUltra/WRO-2022-Future-Engineers/blob/main/autostart.py).

![qualification.py](https://github.com/BogdusUltra/WRO-2022-Future-Engineers/blob/main/qualification.py) is the program for the qualification stage. It is located on the Raspberry Pi. The program waits until information is received that a button has been pressed.
After that, the basic algorithm is started.
The program processes the camera image using the cv2 library. It detects the black walls of the field and determines how far the robot has strayed from the intended route, identifying the error. Next, we calculate the angle by which the servo motor needs to be rotated using the formulas:
u = e * kp + (e - e_old) * kd
deg = rul - u,     
where deg is required angle of servo motor rotation; rul is the initial angle of servo motor rotation at which wheels are aligned; u is difference between rul and deg; e is error; kp is proportional coefficient; kd is differential coefficient; e_old is past error(e) which is updated with each cycle iteration.
After the mathematical calculations we send the values of the variables deg and speed (speed, it is set at the beginning of the program and does not change further on) to the pyboard via UART. This data is received by main.py.
Also, the program counts how many turns the robot has done and after 12 turns, i.e. 3 laps, it stops. The sensors cannot detect a turn, but they can detect the blue and orange lines, they are on the turns.

![final.py](https://github.com/BogdusUltra/WRO-2022-Future-Engineers/blob/main/final.py) is the final stage program. It resides on the Raspberry Pi.
final.py just like qualification.py waits for the button to be pressed, centres the robot and counts the laps travelled, but it also allows the robot to drive around traffic signs - green and red parallelepipeds. The robot needs to avoid the green objects on the left side and the red ones on the right.
The program uses a sensor to look for red and green objects. If it finds a green object, it recognises it as the right-hand side of the field and hence the robot tries to drive between this area. If the sensor detects a red object, it similarly recognises it as a field wall, only on the left-hand side. Thanks to this algorithm, the robot successfully drives around the objects on the right sides.




# Connecting to the pyboard.
We need to install the main.py file on the pyboard. To do this we need to connect pyboard to a laptop via a miniUSB wire. Open explorer and move the main.py file to pyboard and click "replace".

# Connecting to the Raspberry Pi and loading programs.
First we need to power up the Raspberry Pi and wait for it to fully boot up. The Raspberry Pi will start its Wi-Fi hotspot and we need to connect to it. The Wi-Fi network on our Raspberry Pi is called Car1.

![1](https://github.com/BogdusUltra/WRO-2022-Future-Engineers/blob/main/readme_images/1.jpg)

After connecting to the Wi-Fi, start PyCharm and run the program ![start_robot.py](https://github.com/BogdusUltra/WRO-2022-Future-Engineers/blob/main/start_robot.py).

![2](https://github.com/BogdusUltra/WRO-2022-Future-Engineers/blob/main/readme_images/2.jpg)

The special application opens and in its upper right corner there is a "Connect to robot" button. You need to click on it and select the suggested ip address.

![3](https://github.com/BogdusUltra/WRO-2022-Future-Engineers/blob/main/readme_images/3.jpg)

We have connected to the Raspberry Pi.

![4](https://github.com/BogdusUltra/WRO-2022-Future-Engineers/blob/main/readme_images/4.jpg)

Now we can load the programs there.
To do that we need to click on the "load start" button. A file selection window will open, select the required program file and click on "open". 

![5](https://github.com/BogdusUltra/WRO-2022-Future-Engineers/blob/main/readme_images/5.jpg)

The application file has been uploaded and started automatically.

![6](https://github.com/BogdusUltra/WRO-2022-Future-Engineers/blob/main/readme_images/6.jpg)



# Running a programme on the Raspberry Pi.
The programmes will start as soon as they are downloaded to the Raspberry Pi using the laptop. But if the robot is restarted, the programme will not start.
In order to ensure that the program we need is started automatically after the robot is switched on, the autostart.py program must also be preloaded on the Raspberry Pi.
