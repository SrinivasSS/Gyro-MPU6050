#!/usr/bin/python
import smbus
import math
import time
import datetime
import numpy


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

#Define calibration function
#print "Gyroscope"
#print "--------"

#Read initial values
gyroscope_xout = [read_word_2c(0x43)]
gyroscope_yout = [read_word_2c(0x45)]
gyroscope_zout = [read_word_2c(0x47)]
	
#print gyroscope_xout
#print gyroscope_yout
#print gyroscope_zout
	
#print
#print "Accelerometer"
#print "---------------------"
	       
accelerometer_xout = read_word_2c(0x3b)
accelerometer_yout = read_word_2c(0x3d)
accelerometer_zout = read_word_2c(0x3f)
	
acceleration_xout_scaled = [accelerometer_xout / 16384.0]
acceleration_yout_scaled = [accelerometer_yout / 16384.0]
acceleration_zout_scaled = [accelerometer_zout / 16384.0]
	
#print acceleration_xout_scaled
#print acceleration_yout_scaled
#print acceleration_zout_scaled
	
#Get temperature readings
temperature = read_word_2c(0x41)
tempInC = temperature/340 + 36.53

#Take initial mean values of gyro
mean_gxout = numpy.mean(gyroscope_xout)
mean_gyout = numpy.mean(gyroscope_yout)
mean_gzout = numpy.mean(gyroscope_zout)
	
#print "\nMean of gyro"
#print "-----------"
#print mean_gxout
#print mean_gyout
#print mean_gzout
	
calibrate_gxout = mean_gxout - gyroscope_xout
calibrate_gyout = mean_gyout - gyroscope_yout
calibrate_gzout = mean_gzout - gyroscope_zout

#Take initial mean values of accl	
mean_axout = numpy.mean(acceleration_xout_scaled)
mean_ayout = numpy.mean(acceleration_yout_scaled)
mean_azout = numpy.mean(acceleration_zout_scaled)
	
#print "\nMean of accl"
#print "-----------"
#print mean_axout
#print mean_ayout
#print mean_azout
	
#Start calibration loop
print "Calibrating..."
count=1
calibrateAcc = 1
calibrateGyro = 1

while (calibrateAcc != 0) or (calibrateGyro != 0):

	gyroscope_xout.append(read_word_2c(0x43)/131)
	gyroscope_yout.append(read_word_2c(0x45)/131)
	gyroscope_zout.append(read_word_2c(0x47)/131)
	
#	print gyroscope_xout
#	print gyroscope_yout
#	print gyroscope_zout
	
#	print
#	print "Accelerometer"
#	print "---------------------"
	       
	accelerometer_xout = read_word_2c(0x3b)
	accelerometer_yout = read_word_2c(0x3d)
	accelerometer_zout = read_word_2c(0x3f)
	
	acceleration_xout_scaled.append(accelerometer_xout / 16384.0)
	acceleration_yout_scaled.append(accelerometer_yout / 16384.0)
	acceleration_zout_scaled.append(accelerometer_zout / 16384.0)
	
#	print acceleration_xout_scaled
#	print acceleration_yout_scaled
#	print acceleration_zout_scaled
	
	#Get temperature readings
	temperature = read_word_2c(0x41)
	tempInC = temperature/340 + 36.53


	mean_gxout = numpy.mean(gyroscope_xout)
	mean_gyout = numpy.mean(gyroscope_yout)
	mean_gzout = numpy.mean(gyroscope_zout)
	
#	print "\nMean of gyro"
#	print "-----------"
#	print mean_gxout
#	print mean_gyout
#	print mean_gzout
	
	calibrate_gxout = round(mean_gxout - gyroscope_xout[count])
	calibrate_gyout = round(mean_gyout - gyroscope_yout[count])
	calibrate_gzout = round(mean_gzout - gyroscope_zout[count])
	
	mean_axout = numpy.mean(acceleration_xout_scaled)
	mean_ayout = numpy.mean(acceleration_yout_scaled)
	mean_azout = numpy.mean(acceleration_zout_scaled)
	
#	print "\nMean of accl"
#	print "-----------"
#	print mean_axout
#	print mean_ayout
#	print mean_azout
	
	calibrate_axout = round(mean_axout - acceleration_xout_scaled[count],3)
	calibrate_ayout = round(mean_ayout - acceleration_yout_scaled[count],3)
	calibrate_azout = round(mean_azout - acceleration_zout_scaled[count],3)
	
#	print "calibrate_axout:",calibrate_axout
#	print "calibrate_ayout:",calibrate_ayout
#	print "calibrate_azout:",calibrate_azout
	calibrateAcc = calibrate_axout + calibrate_ayout + calibrate_azout
#	print "calibrateAcc: ",calibrateAcc,"\n"

#	print "calibrate_gxout:",calibrate_gxout
#	print "calibrate_gyout:",calibrate_gyout
#	print "calibrate_gzout:",calibrate_gzout
	calibrateGyro = calibrate_gxout + calibrate_gyout + calibrate_gzout
#	print "calibrateGyro: ",calibrateGyro,"\n"
	
#	if 	calibrateAcc == 0:
#		print "Accelerometer calibrated!"
#	elif calibrateGyro == 0:
#		print "Gyroscope calibrated!"

	count = count + 1

else:
	print "\nCalibration done!"

	print "\nCurrent Gyroscope readings:"
	print "\tGX=", gyroscope_xout[count-1],"g"
	print "\tGy=", gyroscope_yout[count-1],"g"
	print "\tGz=", gyroscope_zout[count-1],"g"
	
	print "\nCurrent Acclerometer eadings:"
	print "\tGX=", acceleration_xout_scaled[count-1],"g"
	print "\tGy=", acceleration_yout_scaled[count-1],"g"
	print "\tGz=", acceleration_zout_scaled[count-1],"g"
	


















