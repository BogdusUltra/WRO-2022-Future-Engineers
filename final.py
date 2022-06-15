from mimetypes import guess_all_extensions
from operator import index
from pdb import runcall
import cv2
import RobotAPI as rapi
import RPi.GPIO as IO
import numpy as np
import serial
import time

port = serial.Serial("/dev/ttyS0", baudrate=115200, stopbits=serial.STOPBITS_ONE)
robot = rapi.RobotAPI(flag_serial=False)
robot.set_camera(100, 640, 480)

IO.setwarnings(False)
IO.setmode (IO.BCM)
IO.setup(18,IO.IN) 

message = '999999999$'
state = '0'
ii = ''
fps = 0
fps1 = 0
fps_time = 0

xright1, yright1 = 620, 170
xright2, yright2 = 640, 480

xleft1, yleft1 = 0, 170
xleft2, yleft2 = 20, 480

xBl1, yBl1 = 290, 340
xBl2, yBl2 = 320, 350

xOl1, yOl1 = 320, 340
xOl2, yOl2 = 350, 350

# xOl1, yOl1 = 540, 420
# xOl2, yOl2 = 570, 440

xObj1, yObj1 = 50, 200
xObj2, yObj2 = 590, 330

e = 0
count = 0
x1 = 1130
x, y = 300, 200
w, h = 40, 80
a = ''  
speed = 30
max_speed = 30
min_speed = 30
t_cube = 0.2

Right_color = 0
Left_color = 0

rul = 0
deg = 0
sp = 0
kp = 0.2
kd = 0.1
kp1 = 0.4
kd1 = 0.4
per = 0
e_old = 0
sr1 = 0
sr2 = 0
gsr = 0
rsr = 0
yred = 0
ygr = 0
Objsr = 0
Object_green = 0
Object_red = 0
temp = 0
t_y = 0
index_section = 0

tper = time.time()
t_obj =time.time()
t_red = time.time()
t_green = time.time()
time_index = time.time()
time_section = time.time()


lowBl = np.array([97, 90, 20])
upBl = np.array([110, 255, 125]) #Проверить

lowOl = np.array([0, 75, 7])
upOl = np.array([51, 255, 188]) #Проверить

lowObjgreen = np.array([57, 145, 53])
upObjgreen = np.array([83, 255, 255]) #Проверить

lowObjyellow = np.array([27, 167, 99])
upObjyellow = np.array([42, 255, 231])

lowObjred = np.array([0, 135, 50])
upObjred = np.array([8, 255, 255]) #Проверить
 
lowObjred1 = np.array([165, 135, 50])
upObjred1 = np.array([180, 255, 255]) #Проверить

# start_section = [0, 0, 0]

# second_section = [0, 0, 0]

# third_section = [0, 0, 0]

# fourth_section =[0, 0, 0]

section = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
time_line_to_line = [0, 0, 0, 0]
time_line_to_obj = [[0, 0], [0, 0], [0, 0], [0, 0]]

index_section = 0
index_time = 0

keyboardcontrol = 'None'
direction = 'None'

Flag_line_blue = False
Flag_line_orange = False
Flag_button = False
Flag_obj_green = False
Flag_obj_red = False
Flag_line = False
Flag_index_red = False
Flag_index_green = False
Flag_time_section = False

time_button = time.time()

def black_line():
    global xright1, yright1, xright2, yright2, sr1, sr2
    datb1 = frame[yleft1:yleft2, xleft1:xleft2]
    dat1 = cv2.GaussianBlur(datb1, (9, 9), cv2.BORDER_DEFAULT)
    hsv1 = cv2.cvtColor(dat1.copy(), cv2.COLOR_BGR2HSV)
    gmask1 = cv2.inRange(hsv1, lowObjgreen, upObjgreen)
    maskb1 = cv2.inRange(hsv1, lowBl, upBl)
    rmask = cv2.inRange(hsv1, lowObjred, upObjred)
    gray1 = cv2.cvtColor(dat1, cv2.COLOR_BGR2GRAY)
    _, maskd1 = cv2.threshold(gray1, 40, 255, cv2.THRESH_BINARY_INV)
    maskd11 = cv2.bitwise_and(cv2.bitwise_and(cv2.bitwise_and(maskd1, cv2.bitwise_not(gmask1)),cv2.bitwise_not(maskb1)), cv2.bitwise_not(rmask))
    gray11 = cv2.cvtColor(maskd11.copy(), cv2.COLOR_GRAY2BGR)
    frame[yleft1:yleft2, xleft1:xleft2] = gray11
    imd1, contoursd1, hod1 = cv2.findContours(maskd11, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
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
    hsv2 = cv2.cvtColor(dat2.copy(), cv2.COLOR_BGR2HSV)
    gmask2 = cv2.inRange(hsv2, lowObjgreen, upObjgreen)
    maskb2 = cv2.inRange(hsv2, lowBl, upBl)
    gray2 = cv2.cvtColor(dat2.copy(), cv2.COLOR_BGR2GRAY)
    rmask = cv2.inRange(hsv2, lowObjred, upObjred)
    _, maskd2 = cv2.threshold(gray2, 40, 255, cv2.THRESH_BINARY_INV)
    maskd22 = cv2.bitwise_and(cv2.bitwise_and(cv2.bitwise_and(maskd2, cv2.bitwise_not(gmask2)),cv2.bitwise_not(maskb2)), cv2.bitwise_not(rmask))
    gray12 = cv2.cvtColor(maskd22, cv2.COLOR_GRAY2BGR)
    frame[yright1:yright2, xright1:xright2] = gray12
    imd1, contoursd2, hod1 = cv2.findContours(maskd22, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    sr2 = 0
    for contorb2 in contoursd2:
        x2, y2, w2, h2 = cv2.boundingRect(contorb2)
        a1 = cv2.contourArea(contorb2)
        if a1 > 400:
            if y2 + h2 > sr2:
                sr2 = y2 + h2
                cv2.rectangle(datb2, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 2)

    if sr2 > 150:
        sr2 = 150

    if sr1 > 150:
        sr1 = 150
    
    

def blue_line():
    global max2, yBl1, yBl2, xBl1, xBl2, t, per, sr, state, direction, Flag_line_blue, Flag_line, index_section, time_index, Right_color, Left_color, Flag_time_section, index_time, time_section
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

            if Flag_time_section:
                Flag_time_section = False
                time_line_to_line[per % 4] = round(time.time() - time_section, 2)

            if Flag_time_section == False:
                Flag_time_section = True

            time_section = time.time()
            Flag_line_blue = True
            Flag_line = True
            direction = 'Blue'
            time_index = time.time()
            Right_color = 3
            Left_color = 3
            index_time = 0
            index_section = 0




def orange_line():
    global max2, yOl1, yOl2, xOl1, xOl2, t, per, sr, state, direction, Flag_line_orange, Flag_line, index_section, time_index, Right_color, Left_color, index_time, time_section, Flag_time_section
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

            if Flag_time_section:
                Flag_time_section = False
                time_line_to_line[per % 4] = round(time.time() - time_section, 2)

            if Flag_time_section == False:
                Flag_time_section = True

            time_section = time.time()
            Flag_line_orange = True
            Flag_line = True
            direction = "Orange"
            time_index = time.time()
            Right_color = 4
            Left_color = 4
            index_time = 0
            index_section = 0


def object_():
    global Flag_index_green, section, rsr, gsr, xObj1, xObj2, yObj1, yObj2, Flag_obj_green, Flag_obj_red, state, ygr, yred, t_green, t_red, t_cube, Object_red, Object_green, t_y, per, index_section, Flag_index_red, Right_color, Left_color, index_time, time_section
    cube = frame[yObj1:yObj2, xObj1:xObj2]
    Gauss = cv2.GaussianBlur(cube, (3, 3), cv2.BORDER_DEFAULT)
    hsv = cv2.cvtColor(Gauss, cv2.COLOR_BGR2HSV)
    rmask = cv2.inRange(hsv.copy(), lowObjred, upObjred)
    rmask2 = cv2.inRange(hsv.copy(), lowObjred1, upObjred1)
    rmask3 = cv2.bitwise_or(rmask, rmask2)
    # rmask = cv2.inRange(cv2.cvtColor(cv2.GaussianBlur(frame[yObj1:yObj2, xObj1:xObj2]), 1), lowObjred, upObjred)
    max1 = 0
    # hsv1 = cv2.cvtColor(rmask3.copy(), cv2.COLOR_GRAY2BGR)  
    # frame[yObj1:yObj2, xObj1:xObj2] = hsv1
    cv2.rectangle(frame, (xObj1, yObj1), (xObj2, yObj2), (255, 0, 0), 2)
    _, rcnt, h = cv2.findContours(rmask3, cv2.RETR_EXTERNAL, cv2.BORDER_DEFAULT)
    if len(rcnt) != 0:      
        for i in rcnt:
            x1, y1, w1, h1 = cv2.boundingRect(i)
            a1 = cv2.contourArea(i)
            if a1 > max1:
                if a1 > 200 and a1 / (h1 * w1) > 0.5 and w1 < 270:
                    rsr = x1 + w1
                    Flag_obj_red = True
                    max1 = a1 
                    yred = y1+h1
                    Flag_index_red = True
                    Right_color = 1
                    Left_color = 1
                    t_red = time.time()
                    t_y = time.time()
                    # state = "Object"
                    # cv2.circle(cube, ((x1 + y1) // 2), 5, (0, 0, 255), 2)
                    
                    cv2.rectangle(cube, (x1, y1), (x1 + w1, y1 + h1), (0, 0, 255), 2)
                else:
                     if t_red + 0.1 < time.time():
                        rsr = 0
                        yred = 0
                        Flag_obj_red = False
                        
    else:
        
        if t_red + 0.1 < time.time():
            rsr = 0
            yred = 0
            Flag_obj_red = False
              
                 
        # if t_red + 0.1 < time.time(): 
            if Flag_index_red:
                section[per % 4][index_section] = 5
                time_line_to_obj[per % 4][index_section] = round(time.time() - time_section, 2)
                index_section = 1
                index_time = 1
                Flag_index_red = False
                Object_red += 1 
                

    # gmask = cv2.inRange(cv2.cvtColor(cv2.GaussianBlur(frame[yObj1:yObj2, xObj1:xObj2]), 1), lowObjgreen, upObjred)
    gmask = cv2.inRange(hsv.copy(), lowObjgreen, upObjgreen)
    _, gcnt, h = cv2.findContours(gmask, cv2.RETR_EXTERNAL, cv2.BORDER_DEFAULT)
    max1 = 0
    if len(gcnt) != 0:
        for i in gcnt:
            x1, y1, w1, h1 = cv2.boundingRect(i)
            a1 = cv2.contourArea(i)
            if a1 > max1:
                if a1 > 250 and a1 // (h1 * w1) < 0.6:
                    max1 = a1
                    gsr = x1
                    ygr = y1+h1
                    Flag_obj_green = True
                    Flag_index_green = True
                    Right_color = 2
                    Left_color = 2
                    t_green = time.time()
                    t_y = time.time()
                    # state = "Object"
                    # cv2.circle(cube, ((x1 + y1) // 2), 5, (0, 255, 0), 2)
                    cv2.rectangle(cube, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
                else:
                     if t_green + 0.1 < time.time():
                        gsr = 0 
                        ygr = 0
                        Flag_obj_green = False         
                    
    else: 
             
        if t_green + 0.1 < time.time():
            gsr = 0 
            ygr = 0
            Flag_obj_green = False
                  

            
        # if t_green + 0.1 < time.time():   
            if Flag_index_green:
                section[per % 4][index_section] = 3
                time_line_to_obj[per % 4][index_time] = round(time.time() - time_section, 2)
                Flag_index_green = False
                index_time = 1
                index_section = 1
                Object_green += 1
            
    
    if Flag_obj_green ==  True and  Flag_obj_red == True:
        if ygr > yred:
            Flag_obj_red = False
        else:
            Flag_obj_green = False    
 
def index():
    global index_section, time_section, index_time

    for ind in range(4):

        if section[ind][0] != 0 and section[ind][1]:
            section[ind][2] = section[ind][1]
            section[ind][1] = 0

        elif section[ind][0] != 0 and section[ind][1] == 0:
            if time_line_to_obj[ind][0] / time_line_to_line[ind] > 0.9:
                section[ind][2] = section[ind][0]
                section[ind][0] = 0
            elif time_line_to_obj[ind][0] / time_line_to_line[ind] < 0.8 and time_line_to_obj[ind][0] / time_line_to_line[ind] > 0.5:
                section[ind][1] = section[ind][0]
                section[ind][0] = 0

            

while True:
    Button = (IO.input(18))
    key = robot.get_key()
    # if key != -1:
    #     print(key)

    frame = robot.get_frame(wait_new_frame=1)

    fps1 += 1
    if time.time() > fps_time + 1:
        fps_time = time.time()
        fps = fps1
        fps1 = 0

    if state == '0':
        if Flag_button == False:
            message = '999999999$'
        else:
            message = str(speed + 200) + str(deg + 2000) + str(Right_color) + str(Left_color) + '$'
        if Button == False and time_button + 1 < time.time():
            keyboardcontrol = 'Off'
            state = 'Move'
            direction = 'None'
            Flag_button = True
            Right_color = 2
            Left_color = 2
            speed = 30
            max_speed = 30
            min_speed = 30
            time_button = time.time()
        if Button:
            pass

    if state != '0' and state != 'Stop':
        if keyboardcontrol == 'On':
            sp += 1
            key = robot.get_key()
            if key != -1:
                sp = 0
                # print(key)
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
                if key == 76:
                    keyboardcontrol = "Off"
                    state = "Move"




        if state == "Move":
            # if key == 32:
            #     keyboardcontrol = "On"
            #     state = "keyboard"
            Objsr = 0
            Flag_line = False
            Flag_line_blue = False
            Flag_line_orange = False

            if direction == "Blue":
                blue_line()

            elif direction == "Orange":
                orange_line()
            else:   
                blue_line()
                orange_line()

            # index()
            object_()
            black_line()
            robot.text_to_frame(frame, str(section[per % 4][index_section]), 100, 200)

            e = sr1 - sr2 - 40 + temp
            if -5 < e < 5:
                e = 0
            u = e * kp + (e - e_old)*kd

            if Flag_obj_red:
                if direction == "Orange":
                    yright1 = 260 
                    temp = 10
                else:
                    yleft1 = 260
                    temp = 10
                Objsr  = round(300 - yred * 1.8)
                if Objsr < 50:
                    Objsr = 50
                e = rsr - Objsr
                if -5 < e < 5:
                    e = 0
                u = e * kp1 + (e - e_old)*kd1
                robot.text_to_frame(frame, "Red", 100, 100)

            if Flag_obj_green:
                if direction == "Orange":
                    yright1 = 260 
                    temp = 10
                else:
                    yleft1 = 260
                    temp = 10
                Objsr  = round(240 + ygr * 1.8)
                if Objsr > 490:
                    Objsr = 490
                e = gsr - Objsr
                if -5 < e < 5:
                    e = 0
                u = e * kp1 + (e - e_old)*kd1
                robot.text_to_frame(frame, "Green", 100, 100)

            if t_y + 0.1 < time.time():
                yleft1 = 170 
                temp = 0
                yright1 = 170

            deg = int(rul - u)
            if deg < -50:
                deg = -50
                
            if deg > 50:
                deg = 50

            e_old = e

            if Flag_obj_green == False and Flag_obj_red == False: 
                Right_color = 0
                Left_color = 0 
                if sr2 == 0:
                    deg = -50
                    speed = min_speed

                if sr1 == 0:
                    deg = 50
                    speed = min_speed

                if sr1 == 0 and sr2 == 0:
                    speed = min_speed
                    if direction == 'None':
                        deg = 0
                    elif direction == 'Orange':
                        deg = -50
                    else:
                        deg = 50
                
            
            if Flag_line and tper + 0.5 < time.time(): 
                    per += 1
                    
                    tper = time.time()


            if per // 4 == 3: 
                state = "Finish"
                t_finish = time.time()
            

        if state == "Finish":
            if t_finish + time_line_to_line[0] / 2 > time.time():
                Objsr = 0
                object_()
                black_line()

                e = sr1 - sr2 - 40
                if -5 < e < 5:
                    e = 0
                u = e * kp + (e - e_old)*kd

                if Flag_obj_red:
                    Objsr  = round(300 - yred * 1.6)
                    e = rsr - Objsr
                    if -5 < e < 5:
                        e = 0
                    u = e * kp1 + (e - e_old)*kd1
                    robot.text_to_frame(frame, "Red", 100, 100)

                if Flag_obj_green:
                    Objsr  = round(240 + ygr * 1.6)
                    e = gsr - Objsr
                    if -5 < e < 5:
                        e = 0
                    u = e * kp1 + (e - e_old)*kd1
                    robot.text_to_frame(frame, "Green", 100, 100)

                deg = int(rul - u)
                if deg < -50:
                    deg = -50
                    
                if deg > 50:
                    deg = 50

                e_old = e

                if Flag_obj_green == False and Flag_obj_red == False: 
                    if sr2 == 0:
                        deg = -50

                    if sr1 == 0:
                        deg = 50

                    if sr1 == 0 and sr2 == 0:
                        if direction == 'None':
                            deg = 0
                        elif direction == 'Orange':
                            deg = -50
                        else:
                            deg = 50
                    
                
            else:
                speed = 0
                max_speed = 0
                min_speed = 0
                deg = rul            
            
        deg = -(deg + 13)
        message = str(speed + 200) + str(deg + 2000) + str(Right_color) + str(Left_color) + '$'
        speed = max_speed  
        if Button == False and time_button + 1 < time.time():
            state = '0'
            deg = rul
            time_button = time.time()
            Right_color = 1
            speed = 0
            max_speed = 0
            min_speed = 0
            Left_color = 1
            print(section)
            print(time_line_to_line)
            print(time_line_to_obj)
            print("  ")
            index()
            print("  ")
            print(section)
            print(time_line_to_line)
            print(time_line_to_obj)

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
    robot.text_to_frame(frame, 'ii = ' + str(ii) + ' ' + 'state=' + str(state) + ' ' + str(message) + ' ' + str(direction), 20, 20)
    robot.text_to_frame(frame, 'e = ' + str(e) + ' ' + 'sr1=' + str(sr1) + ' ' + str(sr2) + ' ' + str(Flag_button) + ' ' + str(per) + ' ' + str(rsr) + ' ' + str(gsr), 20, 40)
    robot.text_to_frame(frame, 'yr = ' + str(yred) + ' ' + 'yg=' + str(ygr) + ' ' + str(Objsr) + ' ' + str(Flag_obj_green) + ' ' + str(Flag_obj_red) + ' ' + str(index_section) + ' ' + str(deg) + ' ' + str(Object_red) + ' ' + str(Object_green), 20, 60)
    robot.set_frame(frame, 40)
