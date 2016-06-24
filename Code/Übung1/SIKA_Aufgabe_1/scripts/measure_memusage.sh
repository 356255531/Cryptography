#! /bin/bash

DIRCONF=`dirname $0`
. ${DIRCONF}/config.sh


if [[ $# == 1 ]]
then
	echo "Usage: $0 [-t testruns] [-f ELF filename] [-v] [-d]"
	exit 1
fi

verbose=0
debug=0
testruns=1

while getopts "t:f:vhd" opt; do
	case $opt in
		t)
			testruns="${OPTARG}"
			;;
		f)
			DEFAULT_ELF_FILE="${OPTARG}"
			if [[ "$DEFAULT_ELF_FILE" != *.elf ]]
			then
				echo "Using ${DEFAULT_ELF_FILE}.elf as output elf file"
				DEFAULT_ELF_FILE="${DEFAULT_ELF_FILE}.elf"
			fi
			;;
		v)
			verbose=1
			;;
		d)
			debug=1
			;;
		h)
			echo "Usage: $0 [-t testruns] [-f ELF filename] [-v] [-d]"
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

if [ -e $DEFAULT_ELF_FILE.memtrace ]
then
	rm $DEFAULT_ELF_FILE.memtrace
fi
if [ -e .memusage ]
then
	rm .memusage
fi

command -v java >/dev/null 2>&1 || { echo >&2 "java command not found.  Aborting."; exit 1; }
command -v awk >/dev/null 2>&1 || { echo >&2 "awk command not found.  Aborting."; exit 1; }

if [[ ! -e $AVR_PATH/avr-gdb ]]
then
        echo >&2 "avr-gdb not found.  Aborting.";
        exit 2;
fi

sum_x=0
sum_x2=0

my_path=$(dirname "$0")

for i in $(seq 1 $testruns);
do
	if [ $verbose == 0 ]
	then
		java -jar $PREFIX/bin/avrora-beta-1.7.117.jar -action=simulate -input=elf -monitors=gdb,memory -colors=false $DEFAULT_ELF_FILE > $DEFAULT_ELF_FILE.memtrace &
		$AVR_PATH/avr-gdb --batch-silent $DEFAULT_ELF_FILE --command=$my_path/../utils/getUsedMemory.gdb --directory=$my_path/../utils/ &> /dev/null
	
		if [ $? != 0 ]
		then
			echo "Error while running avr-gdb. Quitting ..."
			exit 1
		fi
	else
		echo "Starting avrora..."
		java -jar $PREFIX/bin/avrora-beta-1.7.117.jar -action=simulate -input=elf -monitors=gdb,memory -colors=false $DEFAULT_ELF_FILE > $DEFAULT_ELF_FILE.memtrace &
	
		echo "Starting gdb..."
		$AVR_PATH/avr-gdb --batch $DEFAULT_ELF_FILE --command=$my_path/../utils/getUsedMemory.gdb --directory=$my_path/../utils/
	
		if [ $? != 0 ]
		then
			echo "Error while running avr-gdb. Quitting ..."
			exit 1
		fi
	fi
	
	if [ $verbose == 1 ]
	then
		echo "Waiting for avrora to quit..."
	fi
	
	wait
	
	if [ $verbose == 1 ]
	then
		echo "Processing memory trace..."
	fi

	awk -f $my_path/../utils/countMemBytes.awk $DEFAULT_ELF_FILE.memtrace

	ret=$(cat MemBytes.txt)
	sum_x=$(echo "$sum_x+$ret" | bc -l)
	sum_x2=$(echo "$sum_x2+$ret^2" | bc -l)

	rm MemBytes.txt

done

if [[ $debug == "1" ]]
then
	mean=$(echo "scale=2; ($sum_x)/($testruns)" | bc -l)	
	echo "Mean value: $mean" > .memusage

	if [[ $testruns > 1 ]]
	then
	    std=$(echo "scale=2; ($sum_x2 - $testruns*(($sum_x/$testruns)^2))/($testruns-1)" | bc -l)
	    echo "Standard deviation: $std" >> .memusage
	fi
fi
exit 0
