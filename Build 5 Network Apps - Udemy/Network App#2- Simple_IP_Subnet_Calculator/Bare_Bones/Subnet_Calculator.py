import re
import random

def subnet_calculator():
	#Requesting ip address and subnet mask from user. split returns a list is strings split at the mentioned argument.
	ip_address = input("Please provide the ip address: ").split(".") 
	subnet_mask = input("Please provide the subnet mask: ").split(".")

	#expressing the subnet mask in binary
	bin_subnet_mask = ["{0:08b}".format(int(x)) for x in subnet_mask]
	print("The subnet mask expressed in binary is: " + ".".join(bin_subnet_mask))
	bin_subnet_mask = "".join(bin_subnet_mask)
	
	
	#Wildcard mask
	bin_wild_card_mask = ["0" if bit == "1" else "1" for octet in bin_subnet_mask for bit in octet]
	joint_bin_wild_card_mask = "".join(bin_wild_card_mask[0:8]) + "." + "".join(bin_wild_card_mask[8:16]) + "." + "".join(bin_wild_card_mask[16:24]) + "." + "".join(bin_wild_card_mask[24:])
	print("Your binary wild card mask is " + joint_bin_wild_card_mask)
	wild_card_mask = (joint_bin_wild_card_mask).split(".")
	wild_card_mask = [str(int(x,2)) for x in wild_card_mask]
	print("Your wild card mask in dotted decimal representation is " + ".".join(wild_card_mask))
	
	#zip() maps similar index of multiple containers so that they can be used just using as single entity.
	network_address = [str(int(x) & int(y)) for x,y in zip(ip_address, subnet_mask)]
	broadcast_address = [str(int(x) | int(y)) for x,y in zip(ip_address, wild_card_mask)]
	
	print("The Network Address is: " + ".".join(network_address))
	print("The Broadcast Address is: " + ".".join(broadcast_address))
	
	#Calculating the number of valid hosts in network
	host_bits = re.search(r'0+$',bin_subnet_mask)
	num_host_bits = len(host_bits.group())
	valid_hosts = str((2**num_host_bits) - 2)
	print("You can have " + valid_hosts + " hosts in this subnet")
	
	#Number of mask bits in CIDR notation
	num_mask_bits = 32 - (num_host_bits)
	print("The CIDR notation for your subnet mask is /" + str(num_mask_bits))
	
	#Generating a random ip address
	while True:
		generate = input("Generate random IP address from this subnet?(y/n)")
		if generate == "y":
			random_ip = [x if x==y else str(random.randint(int(x), int(y))) for x,y in zip(network_address,broadcast_address)]
			print(".".join(random_ip))
		else:
			print("Ok,Bye!")
			break
	
subnet_calculator()
