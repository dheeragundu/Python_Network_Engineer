import paramiko
import time
import re
import sys
import datetime
import matplotlib.pyplot as plt


def SSH_connection():

	session = paramiko.SSHClient()
	session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	session.connect("10.10.10.2", username = "admin", password = "python")

	selected_file = open("C:\\Users\\SaiDheeraDyuti\\Desktop\\Python Scripts\\Network App#3\\test\\commands.txt" , "r")
	commands = selected_file.readlines()
	print(commands)

	session.exec_command("enable\n terminal length 0\n configure terminal\n")
	
	time_file = "C:\\Users\\SaiDheeraDyuti\\Desktop\\Python Scripts\\Network App#3\\test\\time.txt"
	currentDT = datetime.datetime.now()
	with open(time_file, "a") as f:
		f.write(currentDT.strftime("%I:%M") + "\n")
		
	for each_command in commands:
		stdin, stdout, stderr = session.exec_command(each_command + "\n")
		
		
	selected_file.seek(0)
	selected_file.close()
	
	router_output = stdout.read()
	
	if re.search(b"% Invalid input", router_output):
		print("* There was at least one IOS syntax error on device :(")
	else:
		print("\nDONE for device :)\n")
	
	cpu_utilization = re.findall("\d\.\d us", str(router_output))
	print(cpu_utilization)
	
	cpu_ut_file = "C:\\Users\\SaiDheeraDyuti\\Desktop\\Python Scripts\\Network App#3\\test\\cpu_utlization.txt" 
	for ut in cpu_utilization:
		print(ut)
		with open(cpu_ut_file, "a") as f:
			f.write(ut + "\n")
	
	session.close()

while True:
	try:
		SSH_connection()
		i = 0
		while i < 5:
			time.sleep(60)
			i += 1
		
	except KeyboardInterrupt:
		x = open("C:\\Users\\SaiDheeraDyuti\\Desktop\\Python Scripts\\Network App#3\\test\\time.txt", "r")
		x.seek(0)
		time_stamp = [time_stamp.rstrip("\n") for time_stamp in x.readlines()]
		
		y = open("C:\\Users\\SaiDheeraDyuti\\Desktop\\Python Scripts\\Network App#3\\test\\cpu_utlization.txt", "r")
		y.seek(0)
		utilization = [ut.rstrip(" us\n") for ut in y.readlines()]
		plt.plot(time_stamp, utilization)
		plt.xlabel('Time(HH:MM)')
		plt.ylabel('Cpu Utilization')
		plt.show()
		
	


