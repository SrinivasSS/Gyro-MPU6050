#!/usr/bin/python
import smbus
import math
import time

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(reg):
    return bus.read_byte_data(address, reg)
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
  
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
	return -((65535 - val) + 1)
    else:
        return val
     
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
     
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
  
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)
     
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
   
#Activate to be able to address the module
bus.write_byte_data(address, power_mgmt_1, 0)

#Create dat file to save data
f = open("plotData.dat","w")
f.write("#MPU6050 Gyro and Accl Reading \n")
f.write( "#count \t"  )
f.write( "g_xout \t"  )
f.write( "g_yout \t"  )
f.write( "g_zout \t"  )
f.write( "a_xout \t"  )
f.write( "a_yout \t"  )
f.write( "a_zout \t"  )
f.write( "Temp   \n"  )
count=2
dataCount=1
while count>1:
	f.write(str(dataCount) + "\t")
	print "Gyroscope"
	print "--------"
    	
	gyroscope_xout = read_word_2c(0x43)
	gyroscope_yout = read_word_2c(0x45)
	gyroscope_zout = read_word_2c(0x47)
         
	print "gyroscope_xout: ", ("%5d" % gyroscope_xout), " scaled: ", (gyroscope_xout / 131)
	print "gyroscope_yout: ", ("%5d" % gyroscope_yout), " scaled: ", (gyroscope_yout / 131)
	print "gyroscope_zout: ", ("%5d" % gyroscope_zout), " scaled: ", (gyroscope_zout / 131)
	
	f.write( str(gyroscope_xout / 131) + "\t"  )
	f.write( str(gyroscope_yout / 131) + "\t"  )
	f.write( str(gyroscope_zout / 131) + "\t"  )
	
	print
	print "Accelerometer"
	print "---------------------"
        
	accelerometer_xout = read_word_2c(0x3b)
	accelerometer_yout = read_word_2c(0x3d)
	accelerometer_zout = read_word_2c(0x3f)
         
	acceleration_xout_scaled = accelerometer_xout / 16384.0
	acceleration_yout_scaled = accelerometer_yout / 16384.0
	acceleration_zout_scaled = accelerometer_zout / 16384.0
         
	print "accelerometer_xout: ", ("%6d" % accelerometer_xout), " scaled: ", acceleration_xout_scaled
	print "accelerometer_yout: ", ("%6d" % accelerometer_yout), " scaled: ", acceleration_yout_scaled
	print "accelerometer_zout: ", ("%6d" % accelerometer_zout), " scaled: ", acceleration_zout_scaled
	
	f.write( str(acceleration_xout_scaled) + "\t"  )
	f.write( str(acceleration_yout_scaled) + "\t"  )
	f.write( str(acceleration_zout_scaled) + "\t"  )
         
	print "X Rotation: " , get_x_rotation(acceleration_xout_scaled, acceleration_yout_scaled, acceleration_zout_scaled)
	print "Y Rotation: " , get_y_rotation(acceleration_xout_scaled, acceleration_yout_scaled, acceleration_zout_scaled)
	
	#Get temperature readings
	temperature = read_word_2c(0x41)
	tempInC = temperature/340 + 36.53
	print
	print "Temperature in Celsius: ", tempInC
	print "-----------------"
	f.write( str(tempInC) + "\n"  )
	dataCount=dataCount+1
	time.sleep(1)
else:
    print "Not inside while loop"