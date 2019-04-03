from netmiko import Netmiko
import datetime
import glob
import os.path
import difflib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

iplist = ["10.10.10.2", "10.10.10.3", "10.10.10.4"]

for ip in iplist:

	device = {
		"host": ip,
		"username": "admin",
		"password": "python",
		"device_type" : "arista_eos"
		}
	
	#Connecting to the device via SSH using the netmiko module
	net_connect = Netmiko(**device)
	
	#Checking to see if we've SSHed to the right device.(optional)
	#print(net_connect.find_prompt())
	
	#Entering privileged mode to run command.
	net_connect.enable()
	
	#Running the command to extract the running configuration of the device and storing it.
	output = net_connect.send_command("show run")
	
	d = datetime.datetime.now()
	
	#Storing the configuration file in a new folder labeled with the ip. The config file naming convention is:IP_DATE_TIME
	run_conf_file = "C:\\Users\\SaiDheeraDyuti\\Desktop\\Python Scripts\\Build 5 Network Apps - Udemy\\Networkapp#5 - Config Management_Email Notifications\\Bare Bones\\Logs\\{}\\{}_{}.txt".format(ip,ip, d.strftime("%d.%b.%Y_%I.%M %p"))
	
	#Check to see if separate dir for each devcie exists. If it doesn't, create the folder
	if not os.path.exists(os.path.dirname(run_conf_file)):
		try:
			os.makedirs(os.path.dirname(run_conf_file))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise
	with open(run_conf_file, "w") as f:
		f.write(output)
	
	#Get a list of all the files in the folder and sort based on time of creation
	list_of_files = glob.glob("C:\\Users\\SaiDheeraDyuti\\Desktop\\Python Scripts\\Build 5 Network Apps - Udemy\\Networkapp#5 - Config Management_Email Notifications\\Bare Bones\\Logs\\{}\\*.txt".format(ip)) 
	sorted_files = sorted(list_of_files, key=os.path.getctime)
	
	try:
		tofile = sorted_files[-1]
		fromfile = sorted_files[-2]
		#print (fromfile)
		#print(tofile)

		fromlines = open(fromfile, 'r').readlines()
		tolines = open(tofile, 'r').readlines()

		diff = difflib.HtmlDiff().make_file(fromlines,tolines,fromfile,tofile)

	except:
		pass

	#Sending the differences via email
	#Defining the e-mail parameters
	fromaddr = '******@gmail.com'
	toaddr = '******@gmail.com'

	#More on MIME and multipart: https://en.wikipedia.org/wiki/MIME#Multipart_messages
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = 'Daily Configuration Management Report'
	msg.attach(MIMEText(diff, 'html'))

	#Sending the email via Gmail's SMTP server on port 587
	server = smtplib.SMTP('smtp.gmail.com', 587)

	#SMTP connection is in TLS (Transport Layer Security) mode. All SMTP commands that follow will be encrypted.
	server.starttls()

	#Logging in to Gmail and sending the e-mail. Insert username and password here.
	server.login('*****', '******')
	server.sendmail(fromaddr, toaddr, msg.as_string())
	server.quit()


	#End Of Program
