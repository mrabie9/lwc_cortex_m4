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
algorithm = "ascon128"
#algorithms = ["AES", "ascon128", "ascon128a", "elephant160v2", "giftcofb128v1", "grain128aeadv2", "isapa128av20", "isapa128v20", "photonbeetleaead128rate128v1", "romulusn", "schwaemm256128v2", "schwaemm256256v2", "tinyjambu", "xoodyak"]
data_size = "12kB"
wdir = r"C:\WSD030\m7_board\m4_board"

# executable name, output size
# exec_name,n_results = ("AES.elf", 1)

# Serial number and port
# sn, serial_port = ("066AFF574887534867083435", "/dev/tty.usbmodem11303") # TODO: Check
#sn, serial_port = ("0669FF555187534867152037", "COM8") # TODO: Check

serial_port = "COM13"

	
#set the number of runs
number_of_runs = 3

countdown_to_reset = 5

# Application runtime timeout
apprun = 300

def start_board():
	global countdown_to_reset
	prog_log = subprocess.run(wdir + "\openocd_m4" + ".sh " + algorithm, shell=True, capture_output=True, text=True) # TODO: review
	if "Error" in prog_log.stdout or "Error" in prog_log.stderr or "Failed" in prog_log.stdout or "Failed" in prog_log.stderr:
		print(prog_log.stdout, '\n', prog_log.stderr)
		os._exit(10)
	print(prog_log.stdout, '\n', prog_log.stderr)
	countdown_to_reset -= 1
	time.sleep(.1)

# try:
# 	nucleo = serial.Serial(serial_port, 115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout = 5)
# except:
# 	print("quit")
# 	nucleo = serial.Serial(serial_port, 115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout = 5)
# 	os._exit(16)


rebuild = 0
rebuild_output_filename = wdir + r"\rebuild_output_" + data_size
if rebuild:
	print("Rebuilding. Please wait...")
	clean = "make clean -C " + wdir + r"\Software\\" + algorithm
	make = "make -C " + wdir + r"\Software\\" + algorithm
	#make clean -C $wdir/"$app"
	rebuild_log = subprocess.run(clean, shell=True, capture_output=True, text=True) # TODO: review
	rebuild_log = subprocess.run(make, shell=True, capture_output=True, text=True) # TODO: review
	if "Error" in rebuild_log.stdout or "Error" in rebuild_log.stderr or "Failed" in rebuild_log.stdout or "Failed" in rebuild_log.stderr:
		print(rebuild_log.stdout, '\n', rebuild_log.stderr)
		os._exit(10)
		
start_board()
# ~ time.sleep(2)
print("Done")