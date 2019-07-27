#!/bin/bash
if [ "$1" == "start" ]; then
	chmod +x /home/pi/gyro_sensor/gyro.py
	echo "Starting MPU6050!..."
	#nohup python /home/pi/gyro_sensor/gyro1.py &
	python gyro.py
	ps ax | grep gyro.py
	echo "Use cat /home/pi/gyro_sensor/nohup.out to read output"
elif [ "$1" == "stop" ]; then
	gyroPID="$(pgrep gyro.py -f)"
	echo "Stopping gyro.py, PID: $gyroPID ..."
	kill "$gyroPID"
else 
	echo "Usage: ./gyro.sh start (or) ./gyro.sh stop"
fi 