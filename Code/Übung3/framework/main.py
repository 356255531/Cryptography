########################### IMPORT MODULES ############################

import sys, time, glob, os, csv, student

######################### DEFINE PARAMETERS ###########################

timings_csv_file      = './timings.csv'
inputs_csv_file       = './inputs.csv'
testing_pair_csv_file = './testing_pair.csv'

############## LOAD TIMINGS INFORMATION AND TEST PAIR #################

csv_reader = csv.reader(open(timings_csv_file, 'rb'), delimiter=',')
timings = [int(element) for element in csv_reader.next()]

csv_reader = csv.reader(open(testing_pair_csv_file, 'rb'), delimiter=',')
testing_pair = [long(element) for element in csv_reader.next()]

csv_reader = csv.reader(open(inputs_csv_file, 'rb'), delimiter=',')
inputs = [long(element) for element in csv_reader.next()]

##################### PERFORM TIMING ATTACK ###########################

key = student.perform_timing_attack(inputs, timings, testing_pair)

######################## OUTPUT RESULTS ###############################

keyhex = ",".join(["%02X" % (key >> 64 - (8 * (i + 1)) & 0x00000000000000FF) for i in range(64 / 8)])
print keyhex

################### WRITE RESULTS TO A FILE ###########################
keyF = open("./key.txt", "w")
keyF.write(keyhex)
keyF.close()
