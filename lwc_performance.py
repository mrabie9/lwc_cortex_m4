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

# Get current directory
wdir = os.getcwd()

# App name 
rebuild = 0
board = "m4"
algorithm = ''
#algorithms = ["ascon128", "ascon128a", "elephant160v2", "giftcofb128v1", "grain128aeadv2", "isapa128av20", "isapa128v20", "photonbeetleaead128rate128v1", "romulusn", "schwaemm256128v2", "schwaemm256256v2", "tinyjambu", "xoodyak"]
algorithms = ["ascon128"]
data_size = "12kB"

# Serial port
serial_port =  "COM6"
	
#set the number of runs
number_of_runs = 3

countdown_to_reset = 50

# Application runtime timeout
apprun = 120

def start_board():
	global countdown_to_reset
	prog_log = subprocess.run(wdir + "\openocd_" + board + ".sh " + algorithm, shell=True, capture_output=True, text=True) # TODO: review
	if "Error" in prog_log.stdout or "Error" in prog_log.stderr or "Failed" in prog_log.stdout or "Failed" in prog_log.stderr:
		print(prog_log.stdout, '\n', prog_log.stderr)
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

def clearBuffer():
	max_n_attempts = 50
	n_attempts = 1

	while (n_attempts <= max_n_attempts):
		a = nucleo.read(4)
		print("Attempting to clear buffer:")
		print(a)
		if (a == b''):
			print("Serial buffer is clean")
			break
		n_attempts += 1

	max_n_attempts += 1

	if n_attempts == max_n_attempts:
		print("Serial buffer is still not clean after attempt: ", n_attempts)
		print(quit)
		os._exit(17)


def sync():
	# print("Sending zero")
	nucleo.write(float_to_hex(0.0)) # Send 0
	val = nucleo.read(4)			# Receive 0 if successful

	# Check received value
	if(val == b''):
		print("Error: Sent 0 but received null")
		return 1
	elif(hex_to_float(val) != 0.0):
		print("Error: Sent 0 but received ", hex_to_float(val))
		return 1
	else:
		return 0
	

try:
	nucleo = serial.Serial(serial_port, 115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout = 5)
except:
	print("Problem opening serial port")
	os._exit(16)



rebuild_output_filename = wdir + r"\rebuild_output_" + data_size
if rebuild:
	print("Rebuilding All. Please wait...")
	rebuild_log = subprocess.run(wdir + r"\rebuild_all.sh " + rebuild_output_filename, shell=True, capture_output=True, text=True) # TODO: review
	if "Error" in rebuild_log.stdout or "Error" in rebuild_log.stderr or "Failed" in rebuild_log.stdout or "Failed" in rebuild_log.stderr:
		print(rebuild_log.stdout, '\n', rebuild_log.stderr)
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
	start_board()

	print("Starting experiment")
	campaign_start_time = time.time()

	print(algorithm + " Runs: 0") #, end='\r')

	# Main loop
	crash = 0

	try:
		if countdown_to_reset == 0:
			os._exit(10)

		# Sync with app
		if sync() == 1:
			continue
		
		# # Wait app run
		nucleo.timeout = apprun
		# time.sleep(.5)
		nucleo.read(4)
		print("rec")
		nucleo.timeout = 2

		runtime_py = round(time.time() - campaign_start_time, 6)
		nucleo.read(4)
		if sync() == 1: # Sync with send_app_runtime
			continue
		
		# nucleo.write(float_to_hex(0.0)) # Sync
		runtime_e = nucleo.read(4)
		if runtime_e == b'':
			print("Comm error: Did not receive application runtime ", 1)
			crash += 1
			start_board()
			continue
		runtime_e = hex_to_float(runtime_e)
		print("Runtime E: %f s" % runtime_e)
		f.write(algorithm)
		f.write(": \n")
		f.write("\tRuntime E:\t\t%f s\n\t" % runtime_e)

		if sync() == 1:
			continue
		
		# nucleo.write(float_to_hex(0.0)) # Sync
		runtime_d = nucleo.read(4)
		runtime_d = hex_to_float(runtime_d)
		print("Runtime D: %f s" % runtime_d)
		f.write("Runtime D:\t\t%f s\n\t" % runtime_d)
		
		# Get ouptput results
		# ~ time.sleep(.05)
		if sync() == 1: # Sync with send_app_runtime (D)
			continue
		output_e = hex_to_double(nucleo.read(8))

		if sync() == 1: # Sync with send_app_runtime (D)
			continue
		output_d = hex_to_double(nucleo.read(8))

		if sync() == 1: # Sync with send_output
			continue
		sum = hex_to_uint32(nucleo.read(4))
				
		print("Output E: ", output_e)
		print("Output D: ", output_d)
		print("Err Cnt: ", sum)
		f.write("Output:\t\t\t%.1f\n\t" % output_e)
		f.write("Err Cnt:\t\t%.1f\n\t" % sum)
		countdown_to_reset = 5

		time.sleep(.05)

	except Exception as e:
		print("Shouldnt be here->", e)
		start_board()
		continue
	
	print("Runtime Py: ", runtime_py , " s")
	f.write("Runtime Py:\t\t")
	f.write(str(runtime_py))
	f.write(" s")
	f.write("\n\n")
# ~ time.sleep(2)
f.close()