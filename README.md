# WRO-2022-Future-Engineers
Main.py is a separate program. It exchanges data packets with the qualification.py or final.py program (depending on which program is currently running). Pyboard processes the received data and, depending on the values that were in the data packet, changes the servo angle or speed. If the button is pressed, then it sends information about it.

RobotAPI.py - a special class that creates our robot as an object



