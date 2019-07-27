#!/bin/bash

if [ "$1" == "start" ]; then
	chmod +x /home/pi/gyro_sensor/gyro1.py
	echo "Starting MPU6050!..."
	if [ "$2" == "new" ]; then
		echo "Deleting old data from plotData1.dat..."
		rm plotData1.dat
	else 
		echo "Adding to existing data in plotData1.dat"
	fi
	while true; do
	#nohup python /home/pi/gyro_sensor/gyro1.py &
	python gyro1.py
	sleep 0.05
	done
	ps ax | grep gyro.py
	echo "Use cat /home/pi/gyro_sensor/nohup.out to read output"

elif [ "$1" == "stop" ]; then
	gyroPID="$(pgrep gyro.py -f)"
	echo "Stopping gyro.py, PID: $gyroPID ..."
	kill "$gyroPID"
else 
	echo "Usage: ./gyro.sh start new (or) ./gyro.sh start (or) ./gyro.sh stop"
fi 