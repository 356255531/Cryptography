#! /bin/bash

DIRCONF=`dirname $0`
. ${DIRCONF}/config.sh


if [[ $# == 1 ]]
then
	echo "Usage: $0 [-f ELF filename]"
	exit 1
fi

while getopts "f:h" opt; do
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
			echo "Usage: $0 [-f ELF filename]"
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

$AVR_PATH/avr-objdump -D $DEFAULT_ELF_FILE > $DEFAULT_ASM_FILE

if [ $? != 0 ]
then
	echo "Error during disassembly of $DEFAULT_ELF_FILE. Exiting..."
	exit 1
fi

numLoad=$(grep -o '\(ld[dsi]\?\|e\?lpm\)' $DEFAULT_ASM_FILE | wc -l)
echo -e "Number of load instructions (ld, ldi, ldd, lds, lpm, elpm):\t\t\t$numLoad"

numStore=$(grep -o '\<st[ds]\?\>' $DEFAULT_ASM_FILE | wc -l)
echo -e "Number of store instructions (st, std, sts):\t\t\t\t\t$numStore"

numAdd=$(grep -o '\<ad\([dc]\|iw\)\>' $DEFAULT_ASM_FILE | wc -l)
echo -e "Number of addition instructions (add, adc, adiw):\t\t\t\t$numAdd"

numSub=$(grep -o '\<\(sub[i]\?\|sb\(c\|ci\|iw\)\)\>' $DEFAULT_ASM_FILE | wc -l)
echo -e "Number of subtraction instructions (sub, subi, sbc, sbiw, sbci):\t\t$numSub"

numMul=$(grep -o '\<f\?mul\(su\?\)\?\>' $DEFAULT_ASM_FILE | wc -l)
echo -e "Number of multiplication instructions ((f)mul, (f)muls, (f)mulsu):\t\t$numMul"

numShift=$(grep -o '\<\(ls[lr]\|ro[lr]\|asr\)\>' $DEFAULT_ASM_FILE | wc -l)
echo -e "Number of shift instructions (lsl, lsr, rol, ror, asr):\t\t\t\t$numShift"

numLogic=$(grep -o '\<\(andi\?\|or\?\|eor\|com\|neg\)\>' $DEFAULT_ASM_FILE | wc -l)
echo -e "Number of logical instructions (and(i), or(i), eor, com, neg):\t\t\t$numLogic"

numVar=$(grep -o '\<\([sc]\?br\|inc\|dec\|tst\|clr\|ser\)\>' $DEFAULT_ASM_FILE | wc -l)
echo -e "Number of var. arithmetic instructions (sbr, cbr, inc, dec, tst, clr, ser):\t$numVar"

numComp=$(grep -o '\<cp\(c\|i\|se\)\>' $DEFAULT_ASM_FILE | wc -l)
echo -e "Number of compare instructions (cp, cpc, cpi, cpse):\t\t\t\t$numComp"

numBranch=$(grep -o '\<\(\(r\|i\)\?\(jmp\|call\)\|ret[i]\?\|sb[a-z]\{2\}\)\>' $DEFAULT_ASM_FILE | wc -l)
echo -e "Number of branch / jump instructions:\t\t\t\t\t\t$numBranch"
