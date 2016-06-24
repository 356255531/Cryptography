################################################################################
#                             DPA attack on AES                                #
################################################################################
#                                                                              #
# Sichere Implementierung kryptographischer Verfahren WS 2015-2016             #
#                                                                              #
# Technische Universitaet Muenchen                                             #
# Institute for Security in Information Technology                             #
# Prof. Dr.-Ing. Georg Sigl                                                    #
#                                                                              #
################################################################################

It is structured in three folders:

dpa:
    Contains the scripts needed to attack your AES once the measurement is done.
    The script that you need to modify is student.py

    dpa/load_traces.py:
        Class that allows loading of the traces.
        It is used as a module by main.py

    dpa/main.py
        Main attack script.
        Loads traces and then runs your perform_dpa in student.py
        Afterwards verifies your output with test_key.py
        and saves the key to key.txt

    dpa/sample_plot_trace.py
        Helper script to plot the first power trace of your measurent.

    dpa/student.py
        Your implementation goes here.
        This file has to contain a function perform_dpa(ciphertexts, traces)
        It should return the last round key of the attacked AES.

    dpa/test_key.py
        Module to test the key with the recorded data for validity.

measure:
    Contains the measuring scripts.

    measure/pshelper.py
        Available settings of the picoscope. Should not be modified.

    measure/trace_measurement_v2.py
        Measuring script that records the traces of your AES.
        Please modify the settings in the configuration settings of the main
        function to match the length of you AES encryption.

aes:
    Contains the files needed to program the smartcard with your AES.

    aes/student.hex
        Your AES implementation as machinecode with a unknown key should be placed here.

    aes/program_smart_card.sh
        Shell script used to flash your code onto the microcontroller.
