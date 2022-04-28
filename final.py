from mimetypes import guess_all_extensions
from pdb import runcall
import cv2
import RobotAPI as rapi
import numpy as np
import serial
import time

port = serial.Serial("/dev/ttyS0", baudrate=115200, stopbits=serial.STOPBITS_ONE)
robot = rapi.RobotAPI(flag_serial=False)
robot.set_camera(100, 640, 480)

message = '9999999$'
state = '0'
ii = ''
fps = 0
fps1 = 0
fps_time = 0

xright1, yright1 = 620, 215
xright2, yright2 = 640, 480

xleft1, yleft1 = 0, 215
xleft2, yleft2 = 20, 480

xBl1, yBl1 = 320, 400
xBl2, yBl2 = 360, 440

xOl1, yOl1 = 280, 400
xOl2, yOl2 = 320, 440

xObj1, yObj1 = 50, 220
xObj2, yObj2 = 590, 370

e = 0
count = 0
x1 = 1130
x, y = 300, 200
w, h = 40, 80
a = ''
speed = 25
rul = 2000
deg = 0
sp = 0
kp = 5
kd = 3
per = 0
e_old = 0
sr1 = 0
sr2 = 0
gsr = 0
rsr = 0
yred = 0
ygr = 0
Objsr = 0

tper = time.time()
t_obj =time.time()
t_red = time.time()
t_green = time.time()

lowBl = np.array([93, 64, 21])
upBl = np.array([112, 255, 97]) #Проверить

lowOl = np.array([15, 75, 7])
upOl = np.array([51, 256, 188]) #Проверить

lowObjgreen = np.array([63, 225, 60])
upObjgreen = np.array([79, 256, 98]) #Проверить

lowObjred = np.array([0, 88, 86])
upObjred = np.array([11, 193, 133]) #Проверить

keyboardcontrol = 'None'
direction = 'None'

Flag_line_blue = False
Flag_line_orange = False
Flag_button = False
Flag_obj_green = False
Flag_obj_red = False
Flag_line = False

time_button = time.time()

def black_line():
    global xright1, yright1, xright2, yright2, sr1, max1, sr2
    datb1 = frame[yleft1:yleft2, xleft1:xleft2]
    dat1 = cv2.GaussianBlur(datb1, (9, 9), cv2.BORDER_DEFAULT)
    gray1 = cv2.cvtColor(dat1, cv2.COLOR_BGR2GRAY)
    _, maskd1 = cv2.threshold(gray1, 60, 255, cv2.THRESH_BINARY_INV)
    gray11 = cv2.cvtColor(maskd1, cv2.COLOR_GRAY2BGR)
    frame[yleft1:yleft2, xleft1:xleft2] = gray11
    imd1, contoursd1, hod1 = cv2.findContours(maskd1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    max1 = 0
    sr1 = 0
    for contorb1 in contoursd1:
        x1, y1, w1, h1 = cv2.boundingRect(contorb1)
        a1 = cv2.contourArea(contorb1)
        if a1 > 400:
            if y1 + h1 > sr1:
                sr1 = y1 + h1
                cv2.rectangle(datb1, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)

    datb2 = frame[yright1:yright2, xright1:xright2]
    dat2 = cv2.GaussianBlur(datb2, (9, 9), cv2.BORDER_DEFAULT)
    gray2 = cv2.cvtColor(dat2, cv2.COLOR_BGR2GRAY)
    _, maskd2 = cv2.threshold(gray2, 60, 255, cv2.THRESH_BINARY_INV)
    gray12 = cv2.cvtColor(maskd2, cv2.COLOR_GRAY2BGR)
    frame[yright1:yright2, xright1:xright2] = gray12
    imd1, contoursd2, hod1 = cv2.findContours(maskd2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    max2 = 0
    sr2 = 0
    for contorb2 in contoursd2:
        x2, y2, w2, h2 = cv2.boundingRect(contorb2)
        a1 = cv2.contourArea(contorb2)
        if a1 > 400:
            if y2 + h2 > sr2:
                sr2 = y2 + h2
                cv2.rectangle(datb2, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 2)

def blue_line():
    global max2, yBl1, yBl2, xBl1, xBl2, t, per, sr, state, direction, Flag_line_blue, Flag_line
    line = frame[yBl1:yBl2, xBl1:xBl2]
    cv2.rectangle(frame, (xBl1, yBl1), (xBl2, yBl2), (0, 0, 255), 2)
    hsv = cv2.cvtColor(line, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lowBl, upBl)
    gray1 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    frame[yBl1:yBl2, xBl1:xBl2] = gray1
    imd, contours, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    max2 = 0
    for contor in contours:
        x1, y1, w1, h1 = cv2.boundingRect(contor)
        a1 = cv2.contourArea(contor)
        if a1 > 100:
            cv2.rectangle(line, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
            Flag_line_blue = True
            Flag_line = True
            direction = 'Blue'

def orange_line():
    global max2, yOl1, yOl2, xOl1, xOl2, t, per, sr, state, direction, Flag_line_orange, Flag_line
    line = frame[yOl1:yOl2, xOl1:xOl2]
    cv2.rectangle(frame, (xOl1, yOl1), (xOl2, yOl2), (0, 0, 255), 2)
    hsv = cv2.cvtColor(line, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lowOl, upOl)
    gray1 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    frame[yOl1:yOl2, xOl1:xOl2] = gray1
    imd, contours, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    max2 = 0
    for contor in contours:
        x1, y1, w1, h1 = cv2.boundingRect(contor)
        a1 = cv2.contourArea(contor)
        if a1 > 100:
            cv2.rectangle(line, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
            Flag_line_orange = True
            Flag_line = True
            direction = "Orange"


def object_():
    global rsr, gsr, xObj1, xObj2, yObj1, yObj2, Flag_obj_green, Flag_obj_red, state, ygr, yred, t_green, t_red
    cube = frame[yObj1:yObj2, xObj1:xObj2]
    Gauss = cv2.GaussianBlur(cube, (5, 5), cv2.BORDER_DEFAULT)
    hsv = cv2.cvtColor(Gauss, cv2.COLOR_BGR2HSV)
    rmask = cv2.inRange(hsv.copy(), lowObjred, upObjred)
    
    # rmask = cv2.inRange(cv2.cvtColor(cv2.GaussianBlur(frame[yObj1:yObj2, xObj1:xObj2]), 1), lowObjred, upObjred)
    max1 = 0
    # frame[yObj1:yObj2, xObj1:xObj2] = hsv
    cv2.rectangle(frame, (xObj1, yObj1), (xObj2, yObj2), (255, 0, 0), 2)
    _, rcnt, h = cv2.findContours(rmask, cv2.RETR_EXTERNAL, cv2.BORDER_DEFAULT)
    if len(rcnt) != 0:
        t_red = time.time()
        for i in rcnt:
            x1, y1, w1, h1 = cv2.boundingRect(i)
            a1 = cv2.contourArea(i)
            if a1 > max1:
                if a1 > 25 and w1 > 40:
                    rsr = x1 + w1
                    Flag_obj_red = True
                    max1 = a1 
                    yred = y1+h1
                    # state = "Object"
                    # cv2.circle(cube, ((x1 + y1) // 2), 5, (0, 0, 255), 2)
                    cv2.rectangle(cube, (x1, y1), (x1 + w1, y1 + h1), (0, 0, 255), 2)
    else:
        if t_red + 0.2 < time.time():
            rsr = 0
            yred = 0
            Flag_obj_red = False

    # gmask = cv2.inRange(cv2.cvtColor(cv2.GaussianBlur(frame[yObj1:yObj2, xObj1:xObj2]), 1), lowObjgreen, upObjred)
    gmask = cv2.inRange(hsv.copy(), lowObjgreen, upObjgreen)
    _, gcnt, h = cv2.findContours(gmask, cv2.RETR_EXTERNAL, cv2.BORDER_DEFAULT)
    max1 = 0
    if len(gcnt) != 0:
        t_green = time.time()
        for i in gcnt:
            x1, y1, w1, h1 = cv2.boundingRect(i)
            a1 = cv2.contourArea(i)
            if a1 > max1:
                if a1 > 30:
                    max1 = a1
                    gsr = x1
                    ygr = y1+h1
                    Flag_obj_green = True
                    # state = "Object"
                    # cv2.circle(cube, ((x1 + y1) // 2), 5, (0, 255, 0), 2)
                    cv2.rectangle(cube, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
    else:       
        if t_green + 0.2 < time.time():
            gsr = 0
            ygr = 0
            Flag_obj_green = False
    
    if Flag_obj_green ==  True and  Flag_obj_red == True:
        if ygr > yred:
            Flag_obj_red = False
        else:
            Flag_obj_green = False

while True:

    frame = robot.get_frame(wait_new_frame=1)

    fps1 += 1
    if time.time() > fps_time + 1:
        fps_time = time.time()
        fps = fps1
        fps1 = 0

    if state == '0':
        if Flag_button == False:
            message = '9999999$'
        else:
            message = str(0 + 200) + str(rul + 1000) + '$'
        if ii == 'B=0' and time_button + 1 < time.time():
            keyboardcontrol = 'Off'
            state = 'Move'
            direction = 'None'
            Flag_button = True
            time_button = time.time()
        if ii == 'B=1':
            pass

    if state != '0' and state != 'Stop':
        if keyboardcontrol == 'On':
            sp += 1
            key = robot.get_key()
            if key != -1:
                sp = 0
                print(key)
                if key == 87:
                    speed = 35
                if key == 83:
                    speed = -35
                if key == 65:
                    deg += 50
                if key == 68:
                    deg -= 50
            if sp > 10:
                speed = 0




        if state == "Move":
            Objsr = 0
            Flag_line = False
            Flag_line_blue = False
            Flag_line_orange = False
            object_()
            black_line()

            if direction == "Blue":
                blue_line()

            elif direction == "Orange":
                orange_line()
            else:
                blue_line()
                orange_line()

            e = sr1 - sr2 - 10
            if -5 < e < 5:
                e = 0


            if Flag_obj_red:
                Objsr  = round(175 - yred * 0.8)
                e = rsr - Objsr
                robot.text_to_frame(frame, "Red", 100, 100)

            if Flag_obj_green:
                Objsr  = round(370 + ygr * 0.8)
                e = gsr - Objsr
                robot.text_to_frame(frame, "Green", 100, 100)

            u = e * kp + (e - e_old)*kd
            deg = int(rul - u)
            if deg < 1100:
                deg = 1100
                
            if deg > 2700:
                deg = 2700

            e_old = e
            if Flag_obj_green == False and Flag_obj_red == False: 
                if sr2 == 0:
                    deg = 1100

                if sr1 == 0:
                    deg = 2600


            if Flag_line and tper + 0.5 < time.time(): 
                    per += 1
                    tper = time.time()


            if per // 4 == 3: 
                state = "Finish"
                t_finish = time.time()
            

        if state == "Finish":
            if t_finish + 2.3 > time.time():
                black_line()
                e = sr1 - sr2-10
                if -5 < e < 5:
                    e = 0
                u = e * kp + (e - e_old)*kd
                deg = rul - u
                
                if deg < 1700:
                    deg = 1700
                
                if deg > 2300:
                    deg = 2300
                e_old = e

                if sr2 == 0:
                    deg = 1700

                if sr1 == 0:
                    deg = 2300
            else:
                speed = 0
                deg = rul            
            



        message = str(speed + 200) + str(deg + 1000) + '$'  
        if ii == 'B=0' and time_button + 1 < time.time():
            state = '0'
            deg = rul
            time_button = time.time()



        # if robot.get_key() == 50:
        #     keyboardcontrol = "On" 
    # if ii == 'B=0' and Flag_start and time_button + 0.5 > time.time():
    #     time_button = time.time()
    #     speed = 0
    #     Flag_start = False
    #     deg = rul
    #     state = 'Stop'
    port.write(message.encode('utf-8'))



    if port.in_waiting > 0:
        ii = ''
        t = time.time()
        while 1:
            a = str(port.read(), 'utf-8')
            if a != '$':
                ii += a
            else:
                break
            if t + 0.02 < time.time():
                break
        port.reset_input_buffer()



    robot.text_to_frame(frame, 'fps = ' + str(fps), 500, 20)
    robot.text_to_frame(frame, 'ii = ' + str(ii) + ' ' + 'state=' + str(state) + ' ' + str(message) + ' ' + str(direction) + ' ' + str(deg), 20, 20)
    robot.text_to_frame(frame, 'e = ' + str(e) + ' ' + 'sr1=' + str(sr1) + ' ' + str(sr2) + ' ' + str(Flag_button) + ' ' + str(per) + ' ' + str(rsr) + ' ' + str(gsr), 20, 40)
    robot.text_to_frame(frame, 'yr = ' + str(yred) + ' ' + 'yg=' + str(ygr) + ' ' + str(Objsr) + ' ' + str(Flag_obj_green) + ' ' + str(Flag_obj_red), 20, 60)
    robot.set_frame(frame, 40)