import serial
import csv
import datetime
#sets up the serial connection
ser = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_55731323736351C062D0-if00', 9600, 8, 'N', 1, timeout=5)

timestamp = "No watering history"
while True:
	#reads the entire line sent from the arduino until it hits a \n character
	line = ser.readline()
	#gets rid of any whitespace characters
	line = line.rstrip()
	try:
		#splits the data into a list from a predefined delimiter
		line = line.split("$$")
		#if the length of the list is 4, if all the data is collected
		if len(line) == 4:
			#checks if the arduino is starting the watering process
			if int(line[0]) == 1:
				#sets up timestamp for website
				timestamp = datetime.datetime.now().strftime("%I:%M:%S%p on %A, %B %d, %Y")
			#prints out the value, debugging purposes
			print("moisture:" + line[3] + "%")
			print("temperature:" + line[2] + "C")
			print("humidity:" + line[1] + "%")
			print("last time watered: " + timestamp)
			print("------------------------------------------")
			#sets up a list for csv file, for the website
			data = [line[3], line[2], line[1], timestamp]
			#appends to a csv file that the website uses
			with open('statistics.csv', 'a') as fp:
				writer = csv.writer(fp, delimiter=',')
				writer.writerow(data)
	except ValueError:
		print ('sensor error')
	except KeyboardInterrupt:
		ser.write('0')
		print ('program shutting down')
