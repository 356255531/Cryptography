# Measurement script v2

# The output is a hdf5 file with three datasets (plaintext, ciphertext and traces)
# Each value is stored as an UINT8-value

#PicoScope configuration:
    # -CH A is the Data input
    # -EXT is the trigger input

# Please note that matlab transposes the matrices while loading them


import picoscope as ps
from pshelper import psc

import time
import signal
import sys
import os
import random
import thread

from numpy import *

import h5py
import csv

from array import array
import numpy as np

from smartcard.util import toHexString, toBytes, toASCIIString, bs2hl, hl2bs
from smartcard.CardType import ATRCardType
from smartcard.ATR import ATR
from smartcard.CardConnection import CardConnection
from smartcard.CardRequest import CardRequest
import Crypto.Cipher.AES

verbose = True
	
def sc_connect():
	global cardservice	
	# detect the smart card based on the content of the ATR (card-centric approach)
	print('Initializing card connection...')
	try:
		cardtype = ATRCardType( toBytes( "3B 90 11 00" ) )
		cardrequest = CardRequest( timeout=5, cardType=cardtype )
		cardservice = cardrequest.waitforcard()
		print('Card connection established correctly')
	except:
		print('ERROR: Timeout exceeded')
		sys.exit(0)
	# connect to the card using T0 protocol.
	cardservice.connection.connect( CardConnection.T0_protocol )
	
	
def handler(signum, frame):
	raise Exception("Timeout")
	
def sc_decrypt( key ):
	global cardservice	
	# format the command to be sent to the card:
	DECRYPT_KEY = [0x88, 0x10, 0, 0, len( key )] + key + [0x10]
	GET_RESPONSE = [0x88, 0xc0, 0x00, 0x00, 0x10]
	# send the commands and retrieve the responses
	# detecting a transmission error
	#signal.alarm(2)
	try:
	    time.sleep(0.01)    # this can prevent the transmission error
	    response, sw1, sw2 = cardservice.connection.transmit( DECRYPT_KEY )    # This function doesn't terminate sometimes
	#wait and try again after a transmission error
	except Exception, exc:
	    print exc
	    response, sw1, sw2 = cardservice.connection.transmit( DECRYPT_KEY )
	response, sw1, sw2 = cardservice.connection.transmit( GET_RESPONSE )
	return hl2bs( response )
	
	
def scope_init(sample_rate, n_samples):
	print('Initializing oscilloscope...')
	global trace
	try:
		#if(verbose): print ("Open unit:")
		output = ps.open_unit()
		#if(verbose): print(output)
		#if(verbose): print("Set timebase:")
		output = ps.set_timebase(sample_rate, n_samples)
		#if(verbose): print(output)
		#if(verbose): print("CH enable:")
		trace = ps.ch_enable(psc.CH_A, psc.AC, psc.UINT8_T)
		#if(verbose): print(trace)
		#if(verbose): print("CH range:")
		output = ps.ch_range(psc.CH_A, psc.V_100M)
		#if(verbose): print(output)
		#if(verbose): print("Set simple trigger:")
		ps.set_simple_trigger(4, 125)    #Ch external as trigger
		#if(verbose): print(output)
		print('Scope correctly initialized')
	except :
		print('ERROR: Problem initializing scope: ', sys.exc_info()[0])
		sys.exit(0)
	
	
def scope_close():
	ps.close_unit()
	
	
def scope_run():
	ps.run_block()
	
	
def scope_get_trace():
	while(ps.get_data_ready() == False):
	    pass
	ps.get_values()
	
	
def hdf5_file_init(o_file, n_traces, n_samples, chunksize_plaintext, chunksize_ciphertext, chunksize_traces):
	if os.path.isfile(o_file):
		print ("WARNING: File " + o_file + " already exists, overwriting...")		
		os.remove(o_file)
	filehandle = h5py.File(o_file)
	
	FHplaintext = filehandle.create_dataset("plaintext", (n_traces, 16), chunks=chunksize_plaintext, dtype = uint8)
	FHciphertext = filehandle.create_dataset("ciphertext", (n_traces, 16), chunks=chunksize_ciphertext, dtype = uint8)
	FHtraces = filehandle.create_dataset("traces", (n_traces, n_samples), chunks=chunksize_traces, dtype = uint8)
	
	return(filehandle, FHplaintext, FHciphertext, FHtraces)
	
def hdf5_file_close(filehandle):
	filehandle.close()
	
	
def hdf5_add_data(plaintext, ciphertext, trace_number, FHplaintext, FHciphertext, FHtraces):
	global trace
	
	FHplaintext[trace_number, :] = plaintext;
	FHciphertext[trace_number, :] = ciphertext;
	FHtraces[trace_number, :] = trace;


def get_traces(n_traces, n_samples, FHplaintext, FHciphertext, FHtraces, direction):
	global verbose
	print ("Starting capture... ")
	for i in range(0, n_traces):
		# start the scope
		scope_run()
		if(i==0): # wait five seconds the first time to prevent unusable measurements
			time.sleep(5)
		if(verbose):print ("Trace number: %8d/%d" %(i+1,n_traces))
		# generate a new random data vector
		data = [random.randint(0,255) for x in range(16)]
		ciphertext_data = hl2bs(data)
		# send data to the card to be decrypted
		plaintext_data = sc_decrypt(data)
		# get the power trace
		scope_get_trace()
		# save trace, plain-text and cipher-text into an hdf5 file
		if(direction == 0):
			hdf5_add_data(bs2hl(ciphertext_data), bs2hl(plaintext_data), i, FHplaintext, FHciphertext, FHtraces)
		else:
			hdf5_add_data(bs2hl(plaintext_data), bs2hl(ciphertext_data), i, FHplaintext, FHciphertext, FHtraces)
	print ('Done!')


def signal_handler(signal, frame):	
	print('\nClosing connections...')
	scope_close()
	hdf5_file_close()
	print('Done!')
	sys.exit(0)
	
	
def main():
	global verbose
	####################################################################
	# configuration start
	
	direction	= 0		# 0 = encryption, 1 = decryption
	
	n_traces    = 250      # number of traces to capture
	n_samples   = 1000000  # number of samples per trace (visual inspection !)
	sample_rate = psc.F_125_MHZ		# sample rate [S/sec]
	o_directory = './'       # output directory (has to exist!)
	o_file_name = 'traces.h5'       # output file name
	
	chunksize_plaintext = (n_traces, 16)    # defines the chunksize of the plaintext dataset in the hdf5 file
	chunksize_ciphertext = (n_traces, 16)    # defines the chunksize of the ciphertext dataset in the hdf5 file
	chunksize_traces = (n_traces, n_samples)    # defines the chunksize of the traces dataset in the hdf5 file
	
	# configuration end
	####################################################################
	
	start_time = time.time()
	# verbose mode
	if (len(sys.argv) == 2):
		if ('-ver' in sys.argv[1]):
			verbose = True
	# connect signal handler
	signal.signal(signal.SIGINT, signal_handler)
	# establish connection with the card
	sc_connect()
	# initialize the scope
	scope_init(sample_rate, n_samples)
	# open output file
	o_file = o_directory + o_file_name
	filehandle, FHplaintext, FHciphertext, FHtraces = hdf5_file_init(o_file, n_traces, n_samples, chunksize_plaintext, chunksize_ciphertext, chunksize_traces)
	# start collecting power traces
	get_traces(n_traces, n_samples, FHplaintext, FHciphertext, FHtraces, direction)
	# close and exit
	scope_close()
	hdf5_file_close(filehandle)	
	end_time = time.time()	
	print "Elapsed time: ", end_time - start_time
	sys.exit(0)


if __name__ == "__main__":
	main()
