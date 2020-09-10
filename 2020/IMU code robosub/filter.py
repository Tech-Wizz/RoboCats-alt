
import numpy as np
from scipy.signal import butter,filtfilt# Filter requirements.
import sys, math, time, serial, re, numpy as np
import csv
#port = '/dev/ttyS5' #Kirby's Mac
port = '/dev/ttyUSB0' # Intel Nuc
baud = 115200
fs = 100.0       # sample rate, Hz
T = 1/fs
cutoff = fs/2      # desired cutoff frequency of the filter, Hz ,      slightly higher than actual 1.2 Hznyq = 0.5 * fs  # Nyquist Frequencyorder = 2       # sin wave can be approx represented as quadratic
nyq = 0.5*fs
n = int(T * fs) # total number of samples

ser = serial.Serial(port, baud)
ser.flush()

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


if __name__ == "__main__":    
    
    gyro = [] # x, y, z - angular velocity
    accel = [] # x, y, z - linear acceleration
    mag = [] # w, x, y, z

    t = 0
    with open('IMU_DATA.csv', 'w') as IMU_DATA:
    	IMU_writer = csv.writer(IMU_DATA, delimiter = ',', quotechar='"',quoting=csv.QUOTE_MINIMAL)   
    	while t <= 60.1:
        	magnetometer = get_imu_data("$PSPA,QUAT\r\n")
        	gyrometer = get_imu_data("$PSPA,G\r\n")
        	accelerometer = get_imu_data("$PSPA,A\r\n")
        	temp = get_imu_data("$PSPA,TEMP\r\n")
        
        	mag = [magnetometer[i] for i in range(4)]
        	gyro = [gyrometer[i] * math.pi / 180 / 1000 for i in range(3)]
        	accel = [accelerometer[i] * 9.80665 / 1000 for i in range(3)]
		
		Giro0= gyrometer[0] * math.pi / 180 / 1000
		Giro1= gyrometer[1] * math.pi / 180 / 1000
		Giro2= gyrometer[2] * math.pi / 180 / 1000
		Accel0 = accelerometer[0] * 9.80665 / 1000
		Accel1 = accelerometer[1] * 9.80665 / 1000
		Accel2 = accelerometer[2] * 9.80665 / 1000
# sin wave
                data = (t, Accel0)
                def butter_lowpass_filter(data, cutoff, fs, order):
                    normal_cutoff = cutoff / nyq
                    # Get the filter coefficients 
                    b, a = butter(order, normal_cutoff, btype='low', analog=False)
                    y = filtfilt(b, a, data)
                    return y	

        	#compass0 = quaternion_to_euler(magnetometer[0])
		#compass1 = quaternion_to_euler(magnetometer[1])
		#compass2 = quaternion_to_euler(magnetometer[2])
		#compass3 = quaternion_to_euler(magnetometer[3])
		compass = quaternion_to_euler(mag)

    
        	#print("Data at Time: %s" % t)
        	#print("Magnetometer Quaternion Data: %s" % mag)
        	#print("Magnetometer Euler Data: %s" % compass)
        	#print("Gyrometer Data: %s" % gyro)
        	#print("Accelerometer Data: %s" % accel)
        	#print("Temperature Data: %s\n" % temp)

        	#IMU_writer.writerow([t, magnetometer[0], magnetometer[1], magnetometer[2], magnetometer[3], compass[0], compass[1], compass[2], Giro0, Giro1, Giro2, Accel0, Accel1, Accel2, temp[0], temp[1]])
        	IMU_DATA.flush()
            
        	t += 0.1
        	time.sleep(0.1)



fig = go.Figure()
fig.add_trace(go.Scatter(
            y = data,
            line =  dict(shape =  'spline' ),
            name = 'signal with noise'
            ))
fig.add_trace(go.Scatter(
            y = y,
            line =  dict(shape =  'spline' ),
            name = 'filtered signal'
            ))
fig.show()
