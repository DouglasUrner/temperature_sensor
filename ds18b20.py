import os
import glob
import time

class TempSensor:
    def __init__(self, type, id):
        self.type = type    # Type of the device - driver to use.
        self.id = id        # Serial number of the device, if available.   
        label = ''          # Short description of device.
        info = ''           # Long description of device.
        offset_0 = 0        # Calibration offset from 0 degrees C (ice water).
        offset_100 = 0      # Calibration offset from 100 degrees C (boiling water at sea level).
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_raw = int(lines[1][equals_pos+2:])
        temp_c = float(temp_raw) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_raw, temp_c, temp_f
	
while True:
	raw, deg_c, deg_f = read_temp()
	print(raw, deg_c, deg_f)
	time.sleep(1
