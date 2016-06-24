#! /bin/bash

DIRCONF=`dirname $0`
. ${DIRCONF}/config.sh


if [[ $# == 1 ]]
then
	echo "Usage: $0 [-f ELF filename] [-v] [-d]"
	exit 1
fi

TIMEOUT=0
verbose=0
debug=0

while getopts "f:t:vhd" opt; do
	case $opt in
		f)
			DEFAULT_ELF_FILE="${OPTARG}"
			if [[ "$DEFAULT_ELF_FILE" != *.elf ]]
			then
				echo "Using ${DEFAULT_ELF_FILE}.elf as output elf file"
				DEFAULT_ELF_FILE="${DEFAULT_ELF_FILE}.elf"
			fi
			;;
		t)
			TIMEOUT="${OPTARG}"
			;;
		v)
			verbose=1
			;;
		d)
			debug=1
			;;
		h)
			echo "Usage: $0 [-f ELF filename] [-t Timeout in cycles] [-v] [-d]"
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

command -v java >/dev/null 2>&1 || { echo >&2 "java command not found.  Aborting."; exit 1; }
command -v awk >/dev/null 2>&1 || { echo >&2 "awk command not found.  Aborting."; exit 1; }

if [[ ! -e $AVR_PATH/avr-readelf ]]
then
        echo >&2 "avr-readelf not found.  Aborting.";
        exit 2;
fi

if [[ ! -e $AVR_PATH/avr-gdb ]]
then
        echo >&2 "avr-gdb not found.  Aborting.";
        exit 2;
fi

my_path=$(dirname "$0")

if [ $verbose == 1 ]
then
	echo "Finding Start and End PC of aes128_encrypt in .elf file"
fi

encryptLine=$($AVR_PATH/avr-readelf -s $DEFAULT_ELF_FILE | grep aes128_encrypt)
startPC=$(echo $encryptLine | awk '{print $2 }' | sed 's/0*//')
#funcLen=$(echo $encryptLine | awk '{ print $3 }')
startPCuc=$(echo $startPC | tr '[a-z]' '[A-Z]')
startPCDec=$(echo "ibase=16; $startPCuc" | bc)
#endPCDec=$(expr $startPCDec + $funcLen - 2)
#endPC=$(echo "obase=16; $endPCDec" | bc)
#endPC=$(echo $endPC | tr '[A-Z]' '[a-z]')
encryptRetPC=$($AVR_PATH/avr-objdump -D $DEFAULT_ELF_FILE | grep -A 1 '<aes128_encrypt>' | tail -1)    #Get the PC of the instruction in main AFTER calling aes128_encrypt
endPC=$(echo $encryptRetPC | awk '{print $1 }' | cut -f1 -d":")

if [ $verbose == 1 ]
then
	echo "Found aes128_encrypt at 0x$startPC to 0x$endPC"
fi

if [ -e $DEFAULT_ELF_FILE.trace ]
then
	rm $DEFAULT_ELF_FILE.trace
fi

if [ $verbose == 1 ]
then
	echo "Starting avrora..."
fi

java -jar $PREFIX/bin/avrora-beta-1.7.117.jar -action=simulate -input=elf -monitors=gdb,trace -cycle-break=$TIMEOUT -trace-from=0x$startPC:0x$endPC -colors=false $DEFAULT_ELF_FILE > $DEFAULT_ELF_FILE.trace &
#java avrora.Main -action=simulate -input=elf -monitors=gdb,trace -trace-from=0x$startPC:0x$endPC -cycle-break=$TIMEOUT -colors=false $DEFAULT_ELF_FILE > $DEFAULT_ELF_FILE.trace &

if [ $verbose == 0 ]
then
	$AVR_PATH/avr-gdb --batch-silent $DEFAULT_ELF_FILE --command=$my_path/../utils/calculateRunTime.gdb --directory=$my_path/../utils/ &> /dev/null

	if [ $? != 0 ]
	then
		wait
		exit 1
	fi

	wait

	awk -v debug=$debug -f $my_path/../utils/calculateRunTime.awk $DEFAULT_ELF_FILE.trace

	if [ $? != 0 ]
	then
		exit 1
	fi
else
	$AVR_PATH/avr-gdb --batch $DEFAULT_ELF_FILE --command=$my_path/../utils/calculateRunTime.gdb

	if [ $? != 0 ]
	then
		wait
		exit 1
	fi

	echo "Waiting for avrora to quit..."

	wait

	echo "Processing trace..."

	awk -v verbose=yes -v debug=$debug -f $my_path/../utils/calculateRunTime.awk $DEFAULT_ELF_FILE.trace

	if [ $? != 0 ]
	then
		exit 1
	fi

fi

grep 'Cycle timeout reached!' ../code/student.elf.trace

if [ $? == 0 ]
then
    exit 2
fi

exit 0
