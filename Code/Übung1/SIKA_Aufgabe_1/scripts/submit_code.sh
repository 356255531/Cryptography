#! /bin/bash

DIRCONF=`dirname $0`
. ${DIRCONF}/config.sh


if [[ $# == 1 ]]
then
	echo "Usage: $0 [-u username] [-f c filename] [-p pdf filename]"
	exit 1
fi

username=""

while getopts "u:f:p:" opt; do
	case $opt in
		f)
			DEFAULT_C_FILE="${OPTARG}"
			if [[ "$DEFAULT_C_FILE" != *.c ]]
			then
				echo "Using ${DEFAULT_C_FILE}.c as input c file"
				DEFAULT_C_FILE="${DEFAULT_C_FILE}.c"
			exit 1
			fi
			;;
		p)
			DEFAULT_REPORT_FILE="${OPTARG}"
			if [[ "$DEFAULT_REPORT_FILE" != *.pdf ]]
			then
				echo "Using ${DEFAULT_REPORT_FILE}.pdf as input pdf file"
				DEFAULT_REPORT_FILE="${DEFAULT_REPORT_FILE}.pdf"
			exit 1
			fi
			;;
		u)
			username="${OPTARG}"
			;;
		h)
			echo "Usage: $0 [-u username] [-f c filename] [-p pdf filename]"
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

command -v curl >/dev/null 2>&1 || { echo >&2 "curl command not found.  Aborting."; exit 1; }

if [[ ! -e $DEFAULT_C_FILE ]]
then
	echo "$DEFAULT_C_FILE does not exist! Please check if the filename is correct. Exiting ..."
	exit 1
fi

if [[ ! -e $DEFAULT_REPORT_FILE ]]
then
	echo "$DEFAULT_REPORT_FILE does not exist! Please check if the filename is correct. Exiting ..."
	exit 1
fi

if [[ "$username" == "" ]]
then
	read -p "User name: " username
fi

curl -f -F exercise_no=1 -F exercise_file=@"$DEFAULT_C_FILE" -u "$username" --insecure https://tueisec-sica.sec.ei.tum.de/handin/ > /dev/null
ret=$?

if [[ $ret != 0 ]]
then
	echo "Error submitting $DEFAULT_C_FILE. Exiting ..."
	exit $ret
else
	echo "$DEFAULT_C_FILE succesfully submitted. md5sum:"
	md5sum "$DEFAULT_C_FILE"
fi

curl -f -F exercise_no=2 -F exercise_file=@"$DEFAULT_REPORT_FILE" -u "$username" --insecure https://tueisec-sica.sec.ei.tum.de/handin/ > /dev/null
ret=$?

if [[ $ret != 0 ]]
then
	echo "Error submitting $DEFAULT_REPORT_FILE. Exiting ..."
	exit $ret
else
	echo "$DEFAULT_REPORT_FILE succesfully submitted. md5sum:"
	md5sum "$DEFAULT_REPORT_FILE"
fi

exit 0

