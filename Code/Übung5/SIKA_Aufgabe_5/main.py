################################################################################
#                Skeleton script for a DFA attack against AES                  #
################################################################################
#                                                                              #
# Sichere Implementierung kryptographischer Verfahren WS 2013-2014             #
# Technische Universitaet Muenchen                                             #
# Institute for Security in Information Technology                             #
# Prof. Dr.-Ing. Georg Sigl                                                    #
#                                                                              #
################################################################################

############################## IMPORT MODULES ##################################

import sys, time, glob, os, csv, student
from numpy import *

############################ DEFINE PARAMETERS #################################

pairs_path = './'

################### LOAD CORRECT AND FAULTY CIPHERTEXTS  #######################

correct_ciphertexts = []
faulty_ciphertexts = []
csv_reader_faulty_pairs = csv.reader(open(os.path.join(pairs_path, 'faulty_pairs.csv'), 'rb'), delimiter=',')
for row in csv_reader_faulty_pairs:
	correct_ciphertexts.append([int(row[1][i:i+2], 16) for i in range(2,len(row[1]), 2)])
	faulty_ciphertexts.append([int(row[2][i:i+2], 16) for i in range(2,len(row[1]), 2)])

print correct_ciphertexts
print faulty_ciphertexts

############################### PERFORM DFA ####################################

key = student.perform_dfa(correct_ciphertexts, faulty_ciphertexts)
  
############################# OUTPUT RESULTS ###################################

key_hex = ["%02X" % key[i] for i in range(len(key)) ]
keyF = open( "./key.txt", "w" )
writer = csv.writer(keyF)
writer.writerow(key_hex)
keyF.close()

