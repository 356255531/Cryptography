#! /bin/bash

DIRCONF=`dirname $0`
. ${DIRCONF}/config.sh


testruns=3
verbose=0
timeout=0

while getopts "t:f:s:vh" opt; do
	case $opt in
		t)
			testruns="${OPTARG}"
			if [[ $testruns -lt 1 ]]
			then
				echo "Number of test runs must be greater than 0! Setting to default of 3 ..."
				testruns=3
			fi
			;;
		f)
			DEFAULT_ELF_FILE="${OPTARG}"
			if [[ "$DEFAULT_ELF_FILE" != *.elf ]]
			then
				echo "Using ${DEFAULT_ELF_FILE}.elf as output elf file"
				DEFAULT_ELF_FILE="${DEFAULT_ELF_FILE}.elf"
			fi
			;;
		s)
			timeout="${OPTARG}"
			if [[ $timeout -lt 1 ]]
			then
				echo "Timeout must be greater than 0! Disabling timeout ..."
				timeout=0
			fi
			;;
		v)
			verbose=1
			;;
		h)
			echo "Usage: $0 [-t Number of testruns] [-f ELF filename] [-v] [-s Timeout value (in seconds!)]"
			exit 1
			;; 
		:)
			echo "Option -$OPTARG requires an argument." >&2
			exit 1
			;;
		\?)
			echo "Invalid option: -$OPTARG" >&2
			exit 1
			;;
	esac
done

if [[ -e gdb.log ]]
then
	rm gdb.log
fi
if [[ -e AESTestResult.txt ]]
then
	rm AESTestResult.txt
fi
if [[ ! -e $DEFAULT_ELF_FILE ]]
then
	echo "ERROR: $DEFAULT_ELF_FILE not found"
	exit 1
fi

if [[ ! -e $AVR_PATH/simulavr ]]
then
        echo >&2 "simulavr not found.  Aborting.";
        exit 2;
fi

if [[ ! -e $AVR_PATH/avr-gdb ]]
then
        echo >&2 "avr-gdb not found.  Aborting.";
        exit 2;
fi

my_path=$(dirname "$0")

for i in $(seq 1 $testruns);
do
	printf "\nTrial %d\n\n" $i >> gdb.log
	if [[ $verbose == 0 ]]
	then
	        $AVR_PATH/simulavr --device atmega644a -f $DEFAULT_ELF_FILE -T exit -g &> /dev/null &

		SIMULAVR_PID=$!

		timeout $timeout $AVR_PATH/avr-gdb $DEFAULT_ELF_FILE --batch-silent --command=$my_path/../utils/testAESAlgo.gdb --directory=$my_path/../utils/ &> /dev/null
		GDB_RET=$?

		kill -9 $SIMULAVR_PID
		wait $SIMULAVR_PID 2>/dev/null

		if [[ $GDB_RET != 0 ]]
                then
                    if [[ $GDB_RET == 124 ]]
                    then
                        echo "Timeout occured in avr-gdb!"
                        exit 124
                    fi
                        echo "Error running avr-gdb!"
                        exit 1
                fi

	else
		echo "Starting simulavr..."

		$AVR_PATH/simulavr --device atmega644a -f $DEFAULT_ELF_FILE -T exit -g &

		SIMULAVR_PID=$!

		echo "Starting gdb..."
		timeout $timeout $AVR_PATH/avr-gdb $DEFAULT_ELF_FILE --batch --command=$my_path/../utils/testAESAlgo.gdb --directory=$my_path/../utils/
		GDB_RET=$?

		echo "Stopping simulavr..."
		kill -9 $SIMULAVR_PID
		wait $SIMULAVR_PID 2>/dev/null

		if [[ $GDB_RET != 0 ]]
                then
                    if [[ $GDB_RET == 124 ]]
                    then
                        echo "Timeout occured in avr-gdb!"
                        exit 124
                    fi
                        echo "Error running avr-gdb!"
                        exit 1
                fi
	fi

	ret=$(cat AESTestResult.txt)
	if [[ $ret != 0 ]]
	then
		cat gdb.log
		rm AESTestResult.txt
		rm gdb.log
		exit 100
	fi
done

if [[ $verbose == 0 ]]
then
	cat gdb.log
fi

if [[ -e AESTestResult.txt ]]
then
	rm AESTestResult.txt
fi
if [[ -e gdb.log ]]
then
	rm gdb.log
fi

exit 0

