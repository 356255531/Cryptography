################################################################################
#                Skeleton script for DPA attacks on AES                        #
################################################################################
#                                                                              #
# Sichere Implementierung kryptographischer Verfahren WS 2015-2016             #
#                                                                              #
# Technische Universitaet Muenchen                                             #
# Institute for Security in Information Technology                             #
# Prof. Dr.-Ing. Georg Sigl                                                    #
#                                                                              #
################################################################################

############################## IMPORT MODULES ##################################

import student          # Student DPA implementation
import test_key         # Tests derived key
import load_traces      # Loads traces

import csv              # Add support for comma separated value (CSV) files
##import numpy as np      # Add support for matrix manipulations

########################### LOAD DATA AND TRACES ###############################

#open input file (path defined in load_traces)
input_data = load_traces.load_traces()

# Load measured traces into a matrix: trace-number x trace-length
traces = input_data.get_traces()
# Load ciphertexts into a matrix: trace-number x 16 bytes ciphertext
ciphertexts = input_data.get_ciphertexts()
# Load plaintexts into a matrix: trace-number x 16 bytes plaintext
plaintexts = input_data.get_plaintexts()

############################### PERFORM DPA ####################################

last_round_key = student.perform_dpa(ciphertexts, traces)

############################# TEST RESULTS ###################################

if test_key.test_key(last_round_key, plaintexts[0], ciphertexts[0]):
    print "Congratulations! Your key is right."
else:
    print "Your key is wrong :-("

############################# OUTPUT RESULTS ###################################

last_round_key_hex = ["%02X" % last_round_key[i] for i in range(len(last_round_key)) ]
keyF = open( "./key.txt", "w" )
writer = csv.writer(keyF)
writer.writerow(last_round_key_hex)
keyF.close()
