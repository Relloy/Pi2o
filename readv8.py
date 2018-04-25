import serial
import time
import csv
import datetime
ser = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_55731323736351C062D0-if00', 9600, 8, 'N', 1, timeout=5)
n = 0
timestamp = "No watering history"
while True:
	line = ser.readline()
	line = line.rstrip()
	try:
		line = line.split("$$")

		if len(line) == 4:
			if int(line[0]) == 1:
				timestamp = datetime.datetime.now().strftime("%I:%M:%S%p on %A, %B %d, %Y")
			print("moisture:" + line[3] + "%")
			print("temperature:" + line[2] + "C")
			print("humidity:" + line[1] + "%")
			print("last time watered: " + timestamp)
			print("------------------------------------------")

			data = [line[3], line[2], line[1], timestamp]
			with open('statistics.csv', 'a') as fp:
				writer = csv.writer(fp, delimiter=',')
				writer.writerow(data)
	except ValueError:
		print ('sensor error')
	except KeyboardInterrupt:
		ser.write('0')
		print ('program shutting down')
