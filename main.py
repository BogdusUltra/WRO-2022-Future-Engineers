from pyb import delay, Pin, ADC, Timer, UART
import machine
import time
import pyb

uart = UART(6, 115200, stop=1)
zummer = Pin('Y10', Pin.OUT_PP)
button = Pin('Y9', Pin.IN, Pin.PULL_UP)

Motor = Pin('X10')
M1 = Pin('X8', Pin.OUT_PP)
M2 = Pin('X7', Pin.OUT_PP)

tim = Timer(4, freq=10000)
ms = tim.channel(2, Timer.PWM, pin=Motor)

Servo = Pin('X9')
S2 = Pin('X5', Pin.OUT_PP)
S1 = Pin('X6', Pin.OUT_PP)

timS = Timer(4, freq=10000)
ss = tim.channel(1, Timer.PWM, pin=Servo)

inn = ""
message = '000$'

count = 0

serv_deg = ADC("X1")
ONorOFF = 'off'
speed = 0
rul = 2000

flag_start = True

e_old = 0


def PD_servo(deg):
    global e_old, S2, S1, ss

    if deg > 3300:
        deg = 3300
    if deg < 700:
        deg = 700
    e = deg - serv_deg.read()
    u = e * 0.05 + (e - e_old) * 0.3
    # print(serv_deg.read())
    
    if u < 0:
        S1.low()
        S2.high()
        u = -u
    else:
        S1.high()
        S2.low()
    if u >= 100:
        u = 100
    if u < 30:
        u = 30
    if abs(e) < 50:
        u = 0
        S2.low()
        S1.low()
    ss.pulse_width_percent(u)
    e_old = e


def motor(sp):
    global M1, M2, ms
    if sp < 0:
        M1.low()
        M2.high()
    else:
        M1.high()
        M2.low()
    ms.pulse_width_percent(abs(sp))

t = pyb.millis()
while True:
    # print(serv_deg.read())
    # if t + 2000 > pyb.millis():
    #     PD_servo(400)
    # elif t + 4000 > pyb.millis():
    #     PD_servo(2000)
    # elif t + 6000 > pyb.millis():
    #     PD_servo(3500)
    # elif t + 8000 >pyb.millis():
    #     t = pyb.millis()
    # while serv_deg.read() < 3500:
    #     S1.high()
    #     S2.low()
    #     ss.pulse_width_percent(20)
    #     print(serv_deg.read())
    # while serv_deg.read() > 500:
    #     S2.high()
    #     S1.low()
    #     ss.pulse_width_percent(20)
    #     print(serv_deg.read())
    # S2.high()
    # S1.low()
    # ss.pulse_width_percent(20)
    # pyb.delay(1000)
    # print(serv_deg.read())
    # S1.high()
    # S2.low()
    # ss.pulse_width_percent(20)
    # pyb.delay(1000)
    if flag_start:
        print(serv_deg.read())
        rul = 2000
        motor(0)
        PD_servo(rul)

    if uart.any():
        a = chr(uart.readchar())
        if a != '$':
            inn += a
            if len(inn) > 10:
                inn = ''
        else:
            # print(inn)
            if ONorOFF == 'off':
                if inn == '9999999':
                    ONorOFF = 'on'
                    flag_start = False
                    zummer.high()
                    delay(250)
                    zummer.low()
                    delay(50)
            if ONorOFF == 'on':
                message = 'B=' + str(button.value()) + '$'
                try:
                    if len(inn) == 7 and inn != '9999999':
                        speed = int(inn[:3]) - 200
                        rul = int(inn[3:]) - 1000
                        # print(serv_deg.read())
                        print(speed, ' ', rul)
                        inn = ''
                        motor(speed)
                        PD_servo(rul)
                except ValueError:
                    print('err')

            # print(inn)

            inn = ''
            # uart.write(str(serv_deg.read()) + '$')
            uart.write(message)

# 0 = 1125   100 = 0    -100 = 2815