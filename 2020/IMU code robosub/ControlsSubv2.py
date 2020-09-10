

# Run with sudo

import sys, math, time, serial, re, numpy as np



port = '/dev/ttyUSB0' # Intel Nuc
baud = 115200

ser = serial.Serial(port, baud)
ser.flush()

pitch = 0
roll = 0
yaw = 0
pitchold = 0
rollold = 0
yawold = 0
depthold = 0
depth = 0
def quaternion_to_euler(data):
    yz2 = 1 - (2 * (data[2]**2 + data[3]**2))
    pitch_p = 2 * (data[1] * data[2] - data[1] * data[3])
    roll_p = (2 * (data[0] * data[1] + data[2] * data[3])) / yz2
    yaw_p = (2 * (data[0] * data[3] + data[1] * data[2])) / yz2

    pitch_p = 1 if pitch_p > 1 else pitch_p
    pitch_p = -1 if pitch_p < -1 else pitch_p

    roll = math.atan(roll_p) / math.pi
    pitch = math.asin(pitch_p)  / math.pi
    yaw = math.atan(yaw_p) / math.pi

    #print("Roll: %s" % roll)
    #print("Pitch: %s" % pitch)
    #print("Yaw: %s" % yaw)

    return [roll, pitch, yaw]



def get_imu_data(command):
    global ser

    ser.write(command)
    data = ser.readline()
    values = np.array(re.findall('([-\d.]+)', data)).astype(np.float)
    return values




def updateSensors():
    mag = [] # w, x, y, z
    magnetometer = get_imu_data("$PSPA,QUAT\r\n")
    mag = [magnetometer[i] for i in range(4)]
    global pitch,roll,yaw,yawold,pitchold,rollold
    rollold = roll
    pitchold = pitch
    yawold = yaw
    roll, pitch, yaw = quaternion_to_euler(mag)
    return roll,pitch,yaw


    




yawin = input("Enter your Yaw: ") 
depthin = input("Enter your Depth: ") 


DELTA = input("Enter your DELTA: ")
deptherrorold = depthin - depthold
deptherror = depthin - depth








def depthFunc():
    result = (.25286*((deptherror - deptherrorold)/DELTA) + 1.178*deptherror)
    if(result > 1):
        result = 1
    elif(result < -1):
        result = -1
    else:
        result = result
    return result

print(depthFunc())



def pitchFunc():
    pitcherrorold = 0 - pitchold
    pitcherror = 0 - pitch
    result = (.3309*pitcherror + .15406*((pitcherror - pitcherrorold)/DELTA))
    if(result > 1):
        result = 1
    elif(result < -1):
        result = -1
    else:
        result = result
    return result

print(pitchFunc())

rollerrorold = 0 - rollold
pitcherror = 0 - roll

def rollFunc():
    rollerrorold = 0 - rollold
    rollerror = 0 - roll
    result = (.3309*rollerror + .15406*((rollerror - rollerrorold)/DELTA))
    if(result > 1):
        result = 1
    elif(result < -1):
        result = -1
    else:
        result = result
    return result

print(rollFunc())



def yawFunc():
    yawerrorold = yawin - yawold
    yawerror = yawin - yaw
    result = (.25684*((yawerror - yawerrorold)/DELTA) + .58395*yawerror)
    if(result > 1):
        result = 1
    elif(result < -1):
        result = -1
    else:
        result = result
    return result

print(yawFunc())


#Rudimentary Throttle Control
#Thrusters Dont Match Arduino Thruster Numbers
def ThrottleOut():
    T1 = depthFunc() + rollFunc() + pitchFunc()
    T2 = depthFunc() + rollFunc() - pitchFunc()
    T3 = depthFunc() - rollFunc() + pitchFunc()
    T4 = depthFunc() - rollFunc() - pitchFunc()
    T5 = -1*yawFunc()
    T6 = yawFunc()
    T7 = 1500
    T8 = 1500
    if (T1 > 1):
        T1 = 1900
    elif(T1 < -1):
        T1 = 1100
    else:
        T1 = Round(400*T1 + 1500)

    if (T2 > 1):
        T2 = 1900
    elif(T2 < -1):
        T2 = 1100
    else:
        T2 = Round(400*T2 + 1500)

    if (T3 > 1):
        T3 = 1900
    elif(T3 < -1):
        T3 = 1100
    else:
        T3 = Round(400*T3 + 1500)        

    if (T4 > 1):
        T4 = 1900
    elif(T4 < -1):
        T4 = 1100
    else:
        T4 = Round(400*T4 + 1500)
    return T1,T2,T3,T4,T5,T6,T7,T8

print(ThrottleOut())



if __name__ == "__main__":
    t = 0
    while 1:
        updateSensors()
        print(ThrottleOut())



        t += 1
        time.sleep(DELTA)     
