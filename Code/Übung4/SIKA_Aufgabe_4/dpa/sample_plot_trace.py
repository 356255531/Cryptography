################################################################################
#                  Example script for plotting power traces                    #
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

import matplotlib.pyplot as plt # Add support for drawing figures
import load_traces              # Loads traces

########################### LOAD DATA AND TRACES ###############################

#open input file (path defined in load_traces)
input_data = load_traces.load_traces()

# Load measured traces into a matrix: trace-number x trace-length
traces = input_data.get_traces()

########################## PLOT FIRST POWER TRACE ##############################

plt.figure(1)
plt.plot(traces[0])
plt.xlabel('Samples')
plt.ylabel('Power Consumption')
plt.grid('on')
plt.title('Power trace')
plt.savefig('power_trace.pdf', format = 'pdf')

plt.show()
