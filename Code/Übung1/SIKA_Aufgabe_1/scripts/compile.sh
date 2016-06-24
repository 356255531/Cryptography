#! /bin/bash

DIRCONF=`dirname $0`
. ${DIRCONF}/config.sh

if [[ $# == 1 ]]
then
	echo "Usage: $0 [-c student c file] [-e elf output file name] [-H hex output file name]"
	exit 1
fi

while getopts "d:c:e:H:h" opt; do
	case $opt in
		c)
			DEFAULT_C_FILE="${OPTARG}"
			if [[ "$DEFAULT_C_FILE" != *.c ]]
			then
				echo "Using ${DEFAULT_C_FILE}.c as input file"
				DEFAULT_C_FILE="${DEFAULT_C_FILE}.c"
			fi
			;;
		e)
			DEFAULT_ELF_FILE="${OPTARG}"
			if [[ "$DEFAULT_ELF_FILE" != *.elf ]]
			then
				echo "Using ${DEFAULT_ELF_FILE}.elf as output elf file"
				DEFAULT_ELF_FILE="${DEFAULT_ELF_FILE}.elf"
			fi
			;;
		d)
			CODE_DIR="${OPTARG}"
			;;
		H)
			DEFAULT_HEX_FILE="${OPTARG}"
			if [[ "$DEFAULT_HEX_FILE" != *.hex ]]
			then
				echo "Using ${DEFAULT_HEX_FILE}.hex as output hex file"
				DEFAULT_HEX_FILE="${DEFAULT_HEX_FILE}.hex"
			fi
			;;
		h)
			echo "Usage: $0 [-d dir] [-c student c file] [-e elf output file name] [-H hex output file name]"
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

if [[ -z "$CODE_DIR" ]]
then
	CODE_DIR="../code/"
fi

if [[ -e $DEFAULT_ELF_FILE || -e $DEFAULT_HEX_FILE ]]
then
	echo "Warning: compiled files already exist"
	
	if [[ -e $DEFAULT_ELF_FILE ]]
	then
		rm -i $DEFAULT_ELF_FILE
	fi

	if [[ -e $DEFAULT_HEX_FILE ]]
	then
		rm -i $DEFAULT_HEX_FILE
	fi
fi

if [[ ! -e $AVR_PATH/avr-gcc ]]
then
	echo >&2 "avr-gcc not found.  Aborting.";
	exit 2;
fi

options=$(grep OPTIONS $DEFAULT_C_FILE  | cut -d':' -f2)	#The option string should be of the form "//OPTIONS:<option 1>...<option n>", 
															#so we select the line containing "OPTIONS" and remove everything up to and including the colon
if [[ -n "$options" ]]										#If the resulting string is not empty...
then
	echo -n "Compiling AES using student supplied options: $options ... "
	$AVR_PATH/avr-gcc $options -g -mmcu=atmega644 -o $DEFAULT_ELF_FILE -I$CODE_DIR $CODE_DIR/main.c $DEFAULT_C_FILE
	((ret=$?));
	if [[ ${ret} != 0 ]]									#If avr-gcc fails, first assume that the user-specified options were faulty and try with default options
	then
		echo "Invalid options. Using standard compiling options ..."
		echo -n "Compiling AES  with standard options  ... "
		$AVR_PATH/avr-gcc -O2 -std=gnu99 -g -mmcu=atmega644 -o $DEFAULT_ELF_FILE -I$CODE_DIR $CODE_DIR/main.c $DEFAULT_C_FILE
		((ret=$?));
		if [[ ${ret} != 0 ]]								#If avr-gcc still fails, something else went wrong
		then
			echo "ERROR. Exiting..."
			exit 100
		else
			echo "OK"
		fi
	else
		echo "OK"
	fi
else #if [[ -n "$options" ]]
	echo "Warning: no options defined"
	echo -n "Compiling AES with standard options ... "
	$AVR_PATH/avr-gcc -O2 -std=gnu99 -g -mmcu=atmega644 -o $DEFAULT_ELF_FILE -I$CODE_DIR $CODE_DIR/main.c $DEFAULT_C_FILE
	((ret=$?));
	if [[ ${ret} != 0 ]]
	then
		echo "ERROR. Exiting..."
		exit 100
	else
		echo "OK"
	fi
fi

if [[ ! -e $AVR_PATH/avr-objcopy ]]
then
	echo >&2 "avr-objcopy not found. Won't generate hex-file.";
	exit 2;
else
	$AVR_PATH/avr-objcopy -O ihex $DEFAULT_ELF_FILE $DEFAULT_HEX_FILE
fi

echo "Removing intermediate files..."
rm -f $CODE_DIR/*.s
rm -f $CODE_DIR/*.o
rm -f $CODE_DIR/*.i

exit 0
