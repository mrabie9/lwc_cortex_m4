import serial
import struct
import sys
import subprocess
import os
import time
import signal
import random
import re
from datetime import datetime
import platform
import logging
import traceback


# App name 
algorithm = ''
#algorithms = ["ascon128", "ascon128a", "elephant160v2", "giftcofb128v1", "grain128aeadv2", "isapa128av20", "isapa128v20", "photonbeetleaead128rate128v1", "romulusn", "schwaemm256128v2", "schwaemm256256v2", "tinyjambu", "xoodyak"]
algorithms = ["ascon128"]
rebuild = 0
data_size = "12kB"
wdir = r"C:\WSD030\m7_board\m4_board"

# executable name, output size
# exec_name,n_results = ("AES.elf", 1)'

# Serial number and port
# sn, serial_port = ("066AFF574887534867083435", "/dev/tty.usbmodem11303") # TODO: Check
sn, serial_port = ("0669FF555187534867152037", "COM8") # TODO: Check

board = "m4"
	
#set the number of runs
number_of_runs = 3

countdown_to_reset = 5

# Application runtime timeout
apprun = 300

def start_board():
	global countdown_to_reset
	prog_log = subprocess.run(wdir + "\openocd_" + board + ".sh " + algorithm, shell=True, capture_output=True, text=True) # TODO: review
	if "Error" in prog_log.stdout or "Error" in prog_log.stderr or "Failed" in prog_log.stdout or "Failed" in prog_log.stderr:
		print(prog_log.stdout, '\n', prog_log.stderr)
		log_clean("Board error detected!", 1)
		register_log_full.close()
		register_log_clean.close()
		os._exit(10)
	print(prog_log.stdout, '\n', prog_log.stderr)
	clearBuffer()
	countdown_to_reset -= 1
	time.sleep(.1)

def signal_handler(signum, frame):
	print("Catched Ctrl+c")
	nucleo.close()
	global p
	try:
		os.waitpid(p.pid, os.WNOHANG)
	except:
		print("Nevermind...")
	print("Closed serial port")
	user_annotation = input("Anything to anotate?\n Defaults: \n (1) No debug probe detected \n (2) wrong serial number \n (3) No STM32Target found \n (4) No STM32Target found but kept running \nOption (or custom text): ")
	if(user_annotation == "1"):
		log_clean("User annotation: No debug probe")
	elif(user_annotation == "2"):
		log_clean("User annotation: Wrong serial number")
	elif(user_annotation == "3"):
		log_clean("User annotation: No STM32 target found")
	elif(user_annotation == "4"):
		log_clean("No probe detected but kept running")
	else:
		log_clean("User annotation: " + user_annotation)

	register_log_full.close()
	register_log_clean.close()
	print(quit)
	os._exit(9)

signal.signal(signal.SIGINT, signal_handler)

def float_to_hex(f):
    return struct.pack('<f', f)

def int_to_byte(f):
    return struct.pack('<B', f)

def uint64_to_hex(f):
    return struct.pack('<Q', f)

def int_to_hex(f):
    return struct.pack('<i', f)

def byte_to_int(f):
	if len(f) == 1:
		return struct.unpack('<B', f)[0]
	return -1 

def hex_to_ushort(f):
	if len(f) == 2:
		return struct.unpack('<H', f)[0]
	return -1 

def hex_to_float(f):
	# check if data has 4 bytes, needed by unpack
	if len(f) == 4:
		return struct.unpack("<f" ,f)[0]
	return -1 

def hex_to_double(f):
	if len(f) == 8:
		return struct.unpack("<d" ,f)[0]
	return -1 

def hex_to_uint64(f):
	if len(f) == 8:
		return struct.unpack("<Q" ,f)[0]
	return -1 

def hex_to_uint32(f):
	if len(f) == 4:
		return struct.unpack("<I" ,f)[0]
	return -1 

def hex_to_int(f):
	if len(f) == 4:
		return struct.unpack("<i" ,f)[0]
	return -1 

def hex_xor(f1, f2):
    return bytearray([a^b for a,b in zip(f1, f2)])

def log_full(message, ident_level=0):
	register_log_full.write(ident_level*"\t" + "[" + str(datetime.now()) + " -> " + message + "]\n")

def log_clean(message, ident_level=0):
	# ~ print(ident_level*"\t" + "[" + str(datetime.now()) + " -> ", message, "]\r", end=("\n" if "Error" in message else ""))
	log_full(message, ident_level)
	register_log_clean.write(ident_level*"\t" + "[" + str(datetime.now()) + " -> " + message + "]\n")

	
def clearBuffer():
	#Radiation tests at the ILL from August 26 at 15h37:
	#max_n_attempts = 50
	#Radiation tests at the ILL from August 27 at 08h42:
	#max_n_attempts = 500
	#Radiation tests at the ILL from August 27 at 09h11:
	max_n_attempts = 50

	n_attempts = 1

	while (n_attempts <= max_n_attempts):
		a = nucleo.read(4)
		print(a)
		if (a == b''):
			print("Serial buffer is clean")
			break
		n_attempts += 1

	max_n_attempts += 1

	if n_attempts == max_n_attempts:
		print("Serial buffer is still not clean")
		register_log_full.close()
		register_log_clean.close()
		print(quit)
		os._exit(17)

	nucleo.flushInput()
	nucleo.flushOutput()

def sync():
	#Send 0
	log_full("Sending zero", 1)
	nucleo.write(float_to_hex(0.0))
	log_full("Trying to read a zero", 1)
	
	#reads 0 back
	zero = nucleo.read(4)
	if(zero == b''):
		log_clean("Error: Sent 0 but didn't get an aswer. Restarting board", 1)
		start_board()
		return 1
	elif(hex_to_float(zero) != 0.0):
		log_clean("Error: Sent 0 to start com but got "+ str(zero) + " back while starting com. Restarting com", 1)
		start_board()
		return 1
	else:
		log_full("Got zero", 1)
		return 0
	

# Create log folder
subprocess.run(r"mkdir " + wdir + "\logs", shell=True)
register_log_full  = open(wdir + "\logs/"+ str(algorithm) + "_" + str(sn) + "_log_" + str(datetime.now()).replace(" ", "__").replace(":", "-") + "_full.txt", "w")
register_log_clean = open(wdir + "\logs/"+ str(algorithm) + "_" + str(sn) + "_log_" + str(datetime.now()).replace(" ", "__").replace(":", "-") + "_clean.txt", "w")

try:
	nucleo = serial.Serial(serial_port, 115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout = 5)
except:
	log_clean("Problem opening serial port")
	register_log_full.close()
	register_log_clean.close()
	print("quit")
	os._exit(16)



rebuild_output_filename = wdir + r"\rebuild_output_" + data_size
if rebuild:
	print("Rebuilding All. Please wait...")
	rebuild_log = subprocess.run(wdir + r"\rebuild_all.sh " + rebuild_output_filename, shell=True, capture_output=True, text=True) # TODO: review
	if "Error" in rebuild_log.stdout or "Error" in rebuild_log.stderr or "Failed" in rebuild_log.stdout or "Failed" in rebuild_log.stderr:
		print(rebuild_log.stdout, '\n', rebuild_log.stderr)
		log_clean("Compliation Error Detected!", 1)
		register_log_full.close()
		register_log_clean.close()
		os._exit(10)

filename = wdir + "\output_ver_" + board + "_" + data_size + ".txt"
print(filename)
f = open(filename, "w") # clear file first
f.close()
f = open(filename, "a")
if f.closed:
	print("File not open!!")

for x in algorithms:
	algorithm = x
	register_log_full  = open(wdir + "\logs/"+ str(algorithm) + "_" + str(sn) + "_log_" + str(datetime.now()).replace(" ", "__").replace(":", "-") + "_full.txt", "w")
	register_log_clean = open(wdir + "\logs/"+ str(algorithm) + "_" + str(sn) + "_log_" + str(datetime.now()).replace(" ", "__").replace(":", "-") + "_clean.txt", "w")
	start_board()

	print("Starting experiment")
	campaign_start_time = time.time()

	print(algorithm + " Runs: 0") #, end='\r')

	# Main loop
	j = 0
	crash = 0
	for k in range(1):
		j += 1

		try:
			if countdown_to_reset == 0:
				os._exit(10)

			# Sync with app
			#print("\n\tSyncing with {0} - Run {1}".format(algorithm, j))
			log_full("Starting application", 1)

			if sync() == 1:
				continue
					
			#print("App running")
	#		time.sleep(apprun)
			nucleo.timeout = apprun
			# Wait app run
			nucleo.read(4)
			nucleo.timeout = 5

			# Sync with app
			#print("Syncing to get case-study runtime")
			log_full("Syncing to get case-study runtime",1)
			
			if sync() == 1:
				continue
			
			nucleo.write(float_to_hex(0.0)) # Sync
			runtime_e = nucleo.read(4)
			if runtime_e == b'':
				log_clean("Comm error: Did not receive application runtime ", 1)
				print("Comm err")
				crash += 1
				start_board()
				continue
			runtime_e = hex_to_float(runtime_e)
			print("Runtime E: %f s" % runtime_e)
			f.write(algorithm)
			f.write(": \n")
			f.write("\tRuntime E:\t\t%f s\n\t" % runtime_e)
			log_clean("Runtime E: %.2fs" % runtime_e, 1)

			if sync() == 1:
				continue
			
			nucleo.write(float_to_hex(0.0)) # Sync
			runtime_d = nucleo.read(4)
			runtime_d = hex_to_float(runtime_d)
			print("Runtime D: %f s" % runtime_d)
			f.write("Runtime D:\t\t%f s\n\t" % runtime_d)
			log_clean("Runtime D: %.2fs" % runtime_d, 1)
			
			# Get ouptput results
			# ~ time.sleep(.05)
			if sync() == 1:
				continue
			
			nucleo.write(float_to_hex(0.0)) # Sync
			output = hex_to_double(nucleo.read(8))

			if sync() == 1:
				continue

			nucleo.write(float_to_hex(0.0)) # Sync
			sum = nucleo.read(1).hex()
					
			print("Output: ", output)
			f.write("Output:\t\t\t%.1f\n\t" % output)
			f.write("Checksum:\t\t%.1f\n\t" % int(sum))
			print("Checksum: ", sum)
			log_clean("Output: " + str(output), 1)
			countdown_to_reset = 5

			# ~ print(algorithm + " Runs: " + str(j), end='\r')

			time.sleep(.05)

	#		print("---------------------------------------------------")
		except Exception as e:
			print("Shouldnt be here->", e)
			start_board()
			continue

	print("Experiment end")
	campagin_time = round(time.time() - campaign_start_time,2)
	print("Campaign Time: ", campagin_time , " s")
	f.write("Campaign Time:  ")
	f.write(str(campagin_time))
	f.write(" s")
	f.write("\n\n")
	print("\n" + algorithm + " Runs: " + str(j))
# ~ time.sleep(2)
f.close()