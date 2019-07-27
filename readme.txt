This folder contains the code and documentation to use the MPU-6050

Initial setup on RPI3:

1) Enable I2C interface:
	-Open terminal window
	-type sudo raspi-config
	-Go to 'Interfacing Options', select 'I2C' and enable it
	-Close the raspi-config screen
2)Now edit the modules file:
	-Open terminal window
	-type 'sudo nano /etc/modules'
	-If not present add, the following to the file:
		i2c-bcm2708
		i2c-dev
3)Reboot the pi (sudo reboot)

4)Now make the following connections:
	
RPI		MPU-6050
Pin 1*-5v	VCC
Pin 3-SDA	SDA
Pin 5-SCL	SCL
Pin 6-GND	GND

*According to the datasheet of MPU-6050 it should work on the 3.3V Pin 2, however we found that the RPI doesn't detect the 
MPU-6050 when connected to the 3.3V pin and hence we connected it to the 5V pin. In future a resistor could be connected
between the 5V and the MPU-6050

6)If not present install python tools:
	-In terminal type sudo apt-get install i2c-tools python-smbus

7)Test the RPI detects the device:
	-In terminal type sudo i2cdetect -y 1
	-Output should look like:
	pi@raspberrypi ~ $ sudo i2cdetect -y 1
 	0 1 2 3 4 5 6 7 8 9 a b c d e f
	00: -- -- -- -- -- -- -- -- -- -- -- -- --
	10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
	20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
	30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
	40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
	50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
	60: -- -- -- -- -- -- -- -- 68 -- -- -- -- -- -- --
	70: -- -- -- -- -- -- -- --
	If 68 (hex address of MPU-6050) is not shown it means RPI doesn't detect it.


8)Open terminal and type:
	-chmod +x gyro.sh
	-./gyro.sh
9)The MPU should start working and values should be displayed every 1 sec (can be changed in gyro.sh->sleep function)

10) The python code to read the gyro and accl converts the chip's raw data into 'g' values i.e 0.5g or 1/5g etc. Hence on a completely horizontal table,
the readings would be close to 0g. However since the chip is sentive, it wont probably read 0g (the gyroscope sensor is more sensitive than accl).


Links:
Code: https://tutorials-raspberrypi.com/measuring-rotation-and-acceleration-raspberry-pi/
Code: https://circuitdigest.com/microcontroller-projects/mpu6050-gyro-sensor-interfacing-with-raspberry-pi/0000000000000000
Datasheet: https://www.invensense.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf
https://raspberrypi.stackexchange.com/questions/12632/mpu-6050-is-not-being-detected-by-raspberry-pi