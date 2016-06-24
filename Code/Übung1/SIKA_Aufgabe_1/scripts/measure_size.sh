#! /bin/bash

DIRCONF=`dirname $0`
. ${DIRCONF}/config.sh


if [[ $# == 1 ]]
then
	echo "Usage: $0 [-f ELF filename] [-d]"
	exit 1
fi

debug=0

while getopts "f:hd" opt; do
	case $opt in
		f)
			DEFAULT_ELF_FILE="${OPTARG}"
			if [[ "$DEFAULT_ELF_FILE" != *.elf ]]
			then
				echo "Using ${DEFAULT_ELF_FILE}.elf as output elf file"
				DEFAULT_ELF_FILE="${DEFAULT_ELF_FILE}.elf"
			fi
			;;
		h)
			echo "Usage: $0 [-f ELF filename] [-d]"
			exit 1
			;; 
		d)
			debug=1
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

if [[ ! -e $AVR_PATH/avr-size ]]
then
        echo >&2 "avr-size not found.  Aborting.";
        exit 2;
fi

printf "Program Memory Usage: "
size=$($AVR_PATH/avr-size $DEFAULT_ELF_FILE | awk '{if (FNR == 2) print $1 + $2}')
echo "$size"

if [ $debug == "1" ]
then
	echo "$size" > .size
fi

exit 0
